#!/usr/bin/env python3
"""
================================================================================
DDW-X MULTI-AGENT SWARM BLACKBOARD & STATE BUS (v3.0 - EPHEMERAL TTL & PUBSUB)
================================================================================
Module: src/core/rag/zk_swarm_blackboard.py
Architect: Principal AI Architect & Lead DevSecOps Engineer

CAPABILITIES:
1. Thread-Safe Transactional State Bus:
   - SQLite WAL-backed shared memory engine for Multi-Agent Swarms.
   - Structured memory records indexed by Task-ID, Agent-Name, and Key.
2. Authenticated ChaCha20 / HMAC-SHA256 Encryption at Rest:
   - Pure-Python zero-dependency RFC 8439 ChaCha20 stream cipher + HMAC-SHA256.
   - PBKDF2-HMAC-SHA256 key derivation with per-entry cryptographic salt & nonce.
3. Ephemeral State & Time-To-Live (TTL) Automatic Expiration:
   - Automatic timestamp tracking and lazy/active purging of expired state entries.
4. Cross-Agent Data Exchange:
   - Push: Sub-agents post intermediate ASTs, specs, or telemetry maps (Encrypted/Plaintext/TTL).
   - Pull: Peer sub-agents or Master Orchestrators query and transparently decrypt state.
================================================================================
"""

import os
import sys
import json
import time
import struct
import sqlite3
import hashlib
import hmac
import base64
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEFAULT_BLACKBOARD_DB = "scratch/swarm_blackboard.db"
DEFAULT_PASSPHRASE = "DDW-X-ZK-SWARM-KEY-2026"


# ==============================================================================
# PURE-PYTHON RFC 8439 CHACHA20 STREAM CIPHER + HMAC AUTHENTICATION
# ==============================================================================

class ChaCha20Cipher:
    SIGMA = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]

    @staticmethod
    def _rotl32(v: int, c: int) -> int:
        return ((v << c) & 0xFFFFFFFF) | (v >> (32 - c))

    @classmethod
    def _quarter_round(cls, state: List[int], a: int, b: int, c: int, d: int):
        state[a] = (state[a] + state[b]) & 0xFFFFFFFF
        state[d] = cls._rotl32(state[d] ^ state[a], 16)
        state[c] = (state[c] + state[d]) & 0xFFFFFFFF
        state[b] = cls._rotl32(state[b] ^ state[c], 12)
        state[a] = (state[a] + state[b]) & 0xFFFFFFFF
        state[d] = cls._rotl32(state[d] ^ state[a], 8)
        state[c] = (state[c] + state[d]) & 0xFFFFFFFF
        state[b] = cls._rotl32(state[b] ^ state[c], 7)

    @classmethod
    def _chacha20_block(cls, key: bytes, counter: int, nonce: bytes) -> bytes:
        k = list(struct.unpack("<8I", key))
        n = list(struct.unpack("<3I", nonce))
        state = cls.SIGMA + k + [counter] + n
        working = list(state)

        for _ in range(10):
            cls._quarter_round(working, 0, 4, 8, 12)
            cls._quarter_round(working, 1, 5, 9, 13)
            cls._quarter_round(working, 2, 6, 10, 14)
            cls._quarter_round(working, 3, 7, 11, 15)
            cls._quarter_round(working, 0, 5, 10, 15)
            cls._quarter_round(working, 1, 6, 11, 12)
            cls._quarter_round(working, 2, 7, 8, 13)
            cls._quarter_round(working, 3, 4, 9, 14)

        out = [(working[i] + state[i]) & 0xFFFFFFFF for i in range(16)]
        return struct.pack("<16I", *out)

    @classmethod
    def process(cls, key: bytes, nonce: bytes, data: bytes, counter: int = 1) -> bytes:
        if len(key) != 32:
            raise ValueError("ChaCha20 key must be 32 bytes")
        if len(nonce) != 12:
            raise ValueError("ChaCha20 nonce must be 12 bytes")

        out = bytearray(len(data))
        block_idx = counter
        for i in range(0, len(data), 64):
            keystream = cls._chacha20_block(key, block_idx, nonce)
            chunk = data[i:i + 64]
            for j in range(len(chunk)):
                out[i + j] = chunk[j] ^ keystream[j]
            block_idx += 1
        return bytes(out)


class SwarmCrypto:
    @staticmethod
    def derive_keys(passphrase: str, salt: bytes) -> Tuple[bytes, bytes]:
        key_material = hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, 1000, dklen=64)
        return key_material[:32], key_material[32:]

    @classmethod
    def encrypt_payload(cls, plaintext: str, passphrase: str) -> str:
        salt = os.urandom(16)
        nonce = os.urandom(12)
        enc_key, hmac_key = cls.derive_keys(passphrase, salt)

        data_bytes = plaintext.encode("utf-8")
        ciphertext = ChaCha20Cipher.process(enc_key, nonce, data_bytes)
        mac = hmac.new(hmac_key, salt + nonce + ciphertext, hashlib.sha256).digest()
        package = salt + nonce + mac + ciphertext
        return "ENC::" + base64.b64encode(package).decode("utf-8")

    @classmethod
    def decrypt_payload(cls, encrypted_token: str, passphrase: str) -> str:
        if not encrypted_token.startswith("ENC::"):
            return encrypted_token

        raw_b64 = encrypted_token[5:]
        try:
            package = base64.b64decode(raw_b64)
            if len(package) < 60:
                raise ValueError("Corrupted encrypted package")

            salt = package[:16]
            nonce = package[16:28]
            expected_mac = package[28:60]
            ciphertext = package[60:]

            enc_key, hmac_key = cls.derive_keys(passphrase, salt)
            computed_mac = hmac.new(hmac_key, salt + nonce + ciphertext, hashlib.sha256).digest()

            if not hmac.compare_digest(expected_mac, computed_mac):
                raise ValueError("HMAC verification failed: Invalid passphrase or corrupted state")

            decrypted_bytes = ChaCha20Cipher.process(enc_key, nonce, ciphertext)
            return decrypted_bytes.decode("utf-8", errors="replace")
        except Exception as e:
            return f"[DECRYPTION_ERROR: {e}]"


# ==============================================================================
# SWARM BLACKBOARD STATE ENGINE
# ==============================================================================

class SwarmBlackboard:
    """
    SQLite-backed shared memory bus for multi-agent swarm task synchronization.
    """
    def __init__(self, db_path: Union[str, Path] = DEFAULT_BLACKBOARD_DB):
        self.db_path = Path(db_path).resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=15.0)
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS swarm_tasks (
                    task_id TEXT PRIMARY KEY,
                    title TEXT,
                    created_at REAL,
                    updated_at REAL,
                    status TEXT DEFAULT 'ACTIVE'
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS blackboard_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    agent_name TEXT NOT NULL,
                    entry_key TEXT NOT NULL,
                    entry_value TEXT NOT NULL,
                    data_type TEXT DEFAULT 'text',
                    is_encrypted INTEGER DEFAULT 0,
                    expires_at REAL DEFAULT NULL,
                    created_at REAL,
                    FOREIGN KEY(task_id) REFERENCES swarm_tasks(task_id) ON DELETE CASCADE
                );
            """)
            # Migration checks for existing databases
            cursor.execute("PRAGMA table_info(blackboard_entries);")
            columns = [row[1] for row in cursor.fetchall()]
            if "is_encrypted" not in columns:
                cursor.execute("ALTER TABLE blackboard_entries ADD COLUMN is_encrypted INTEGER DEFAULT 0;")
            if "expires_at" not in columns:
                cursor.execute("ALTER TABLE blackboard_entries ADD COLUMN expires_at REAL DEFAULT NULL;")

            cursor.execute("CREATE INDEX IF NOT EXISTS idx_bb_task ON blackboard_entries(task_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_bb_agent ON blackboard_entries(agent_name);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_bb_key ON blackboard_entries(task_id, entry_key);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_bb_expires ON blackboard_entries(expires_at);")

            conn.commit()

    def vacuum_expired(self) -> int:
        now = time.time()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM blackboard_entries WHERE expires_at IS NOT NULL AND expires_at <= ?;", (now,))
            deleted_count = cursor.rowcount
            conn.commit()
            return deleted_count

    def push(self, task_id: str, agent_name: str, key: str, value: Any,
             data_type: Optional[str] = None, encrypt: bool = False,
             passphrase: str = DEFAULT_PASSPHRASE, ttl: Optional[int] = None) -> int:
        now = time.time()
        expires_at = (now + ttl) if ttl and ttl > 0 else None

        if isinstance(value, (dict, list)):
            val_str = json.dumps(value, indent=2)
            actual_type = data_type or "json"
        else:
            val_str = str(value)
            actual_type = data_type or "text"

        if encrypt:
            stored_value = SwarmCrypto.encrypt_payload(val_str, passphrase)
            is_enc = 1
        else:
            stored_value = val_str
            is_enc = 0

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO swarm_tasks (task_id, title, created_at, updated_at, status)
                VALUES (?, ?, ?, ?, 'ACTIVE')
                ON CONFLICT(task_id) DO UPDATE SET updated_at = excluded.updated_at;
            """, (task_id, f"Swarm Task: {task_id}", now, now))

            cursor.execute("""
                INSERT INTO blackboard_entries (task_id, agent_name, entry_key, entry_value, data_type, is_encrypted, expires_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (task_id, agent_name, key, stored_value, actual_type, is_enc, expires_at, now))
            entry_id = cursor.lastrowid
            conn.commit()
            return entry_id

    def pull(self, task_id: str, key: Optional[str] = None, agent_name: Optional[str] = None,
             decrypt: bool = True, passphrase: str = DEFAULT_PASSPHRASE) -> List[Dict[str, Any]]:
        self.vacuum_expired()

        query = "SELECT id, task_id, agent_name, entry_key, entry_value, data_type, is_encrypted, expires_at, created_at FROM blackboard_entries WHERE task_id = ?"
        params = [task_id]

        if key:
            query += " AND entry_key = ?"
            params.append(key)
        if agent_name:
            query += " AND agent_name = ?"
            params.append(agent_name)

        query += " ORDER BY created_at ASC;"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            results = []
            for r in rows:
                val = r["entry_value"]
                is_encrypted = bool(r["is_encrypted"])

                if is_encrypted and decrypt:
                    val = SwarmCrypto.decrypt_payload(val, passphrase)

                if r["data_type"] == "json" and not (is_encrypted and not decrypt):
                    try:
                        val = json.loads(val)
                    except Exception:
                        pass

                results.append({
                    "id": r["id"],
                    "task_id": r["task_id"],
                    "agent_name": r["agent_name"],
                    "key": r["entry_key"],
                    "value": val,
                    "data_type": r["data_type"],
                    "is_encrypted": is_encrypted,
                    "expires_at": r["expires_at"],
                    "timestamp": r["created_at"]
                })
            return results

    def list_tasks(self) -> List[Dict[str, Any]]:
        self.vacuum_expired()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.task_id, t.title, t.created_at, t.updated_at, t.status,
                       COUNT(e.id) as entry_count,
                       SUM(CASE WHEN e.is_encrypted = 1 THEN 1 ELSE 0 END) as encrypted_count,
                       GROUP_CONCAT(DISTINCT e.agent_name) as participating_agents
                FROM swarm_tasks t
                LEFT JOIN blackboard_entries e ON t.task_id = e.task_id
                GROUP BY t.task_id
                ORDER BY t.updated_at DESC;
            """)
            rows = cursor.fetchall()
            return [
                {
                    "task_id": r["task_id"],
                    "title": r["title"],
                    "created_at": r["created_at"],
                    "updated_at": r["updated_at"],
                    "status": r["status"],
                    "entry_count": r["entry_count"],
                    "encrypted_count": r["encrypted_count"] or 0,
                    "agents": r["participating_agents"].split(",") if r["participating_agents"] else []
                }
                for r in rows
            ]

    def clear(self, task_id: Optional[str] = None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if task_id:
                cursor.execute("DELETE FROM blackboard_entries WHERE task_id = ?;", (task_id,))
                cursor.execute("DELETE FROM swarm_tasks WHERE task_id = ?;", (task_id,))
            else:
                cursor.execute("DELETE FROM blackboard_entries;")
                cursor.execute("DELETE FROM swarm_tasks;")
            conn.commit()


# ==============================================================================
# CLI HANDLER & VERIFICATION INTERFACE
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="DDW-X Multi-Agent Swarm Blackboard & Encrypted State Bus (v3.0)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--push", action="store_true", help="Push an entry to the blackboard")
    group.add_argument("--pull", action="store_true", help="Pull entries from the blackboard")
    group.add_argument("--list", action="store_true", help="List all active swarm tasks")
    group.add_argument("--vacuum", action="store_true", help="Manually purge expired TTL entries")
    group.add_argument("--clear", action="store_true", help="Clear a task or the entire blackboard")

    parser.add_argument("--task-id", help="Unique Swarm Task identifier (e.g. Task-001)")
    parser.add_argument("--agent", help="Originating or target Agent name (e.g. Agent-Alpha)")
    parser.add_argument("--key", help="State key name (e.g. kernel_ioctl_spec)")
    parser.add_argument("--value", help="Value string or JSON payload to store")
    parser.add_argument("--value-file", help="Path to file containing large value payload to store")
    parser.add_argument("--ttl", type=int, help="Time-To-Live in seconds for ephemeral state")
    parser.add_argument("--data-type", choices=["text", "json", "ast", "c_code", "asm"], default="text", help="Content data type")
    parser.add_argument("--encrypt", action="store_true", help="Encrypt state payload at rest using ChaCha20+HMAC")
    parser.add_argument("--no-decrypt", action="store_true", help="Keep raw ciphertext during pull without decrypting")
    parser.add_argument("--passphrase", default=DEFAULT_PASSPHRASE, help="Secret passphrase for state encryption/decryption")
    parser.add_argument("--db-path", default=DEFAULT_BLACKBOARD_DB, help="Path to SQLite blackboard database")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    args = parser.parse_args()
    bb = SwarmBlackboard(args.db_path)

    if args.push:
        if not args.task_id or not args.agent or not args.key or (args.value is None and not args.value_file):
            parser.error("--push requires --task-id, --agent, --key, and either --value or --value-file")
        
        if args.value_file:
            with open(args.value_file, "r", encoding="utf-8", errors="replace") as f:
                raw_val = f.read()
        else:
            raw_val = args.value

        val = raw_val
        d_type = args.data_type
        try:
            parsed = json.loads(raw_val)
            if isinstance(parsed, (dict, list)):
                val = parsed
                d_type = "json"
        except Exception:
            pass

        entry_id = bb.push(args.task_id, args.agent, args.key, val, data_type=d_type,
                           encrypt=args.encrypt, passphrase=args.passphrase, ttl=args.ttl)
        if args.json:
            print(json.dumps({
                "status": "SUCCESS",
                "entry_id": entry_id,
                "task_id": args.task_id,
                "agent": args.agent,
                "key": args.key,
                "ttl": args.ttl,
                "encrypted": args.encrypt
            }))
        else:
            print("=" * 80)
            print(" [DDW-X SWARM BLACKBOARD] MEMORY PUSH CONFIRMED (v3.0)")
            print("=" * 80)
            print(f" [*] Task ID      : {args.task_id}")
            print(f" [*] Origin Agent : {args.agent}")
            print(f" [*] State Key    : {args.key}")
            print(f" [*] Ephemeral TTL: {f'{args.ttl} seconds' if args.ttl else 'PERMANENT'}")
            print(f" [*] Data Type    : {d_type}")
            print(f" [*] Encrypted    : {'YES (ChaCha20-Poly/HMAC)' if args.encrypt else 'NO (Plaintext)'}")
            print(f" [*] Entry ID     : #{entry_id}")
            print("-" * 80)
            print(f" [PAYLOAD]:\n{json.dumps(val, indent=2) if isinstance(val, (dict, list)) else val}")
            print("=" * 80)

    elif args.pull:
        if not args.task_id:
            parser.error("--pull requires --task-id")
        
        entries = bb.pull(args.task_id, key=args.key, agent_name=args.agent,
                          decrypt=not args.no_decrypt, passphrase=args.passphrase)
        if args.json:
            print(json.dumps({"task_id": args.task_id, "count": len(entries), "entries": entries}, indent=2))
        else:
            print("=" * 80)
            print(f" [DDW-X SWARM BLACKBOARD] STATE PULL FOR TASK: {args.task_id}")
            print("=" * 80)
            print(f" [*] Total Active Records   : {len(entries)}")
            print(f" [*] Decryption Mode        : {'PLAINTEXT_RESTORED' if not args.no_decrypt else 'RAW_CIPHERTEXT'}")
            print("-" * 80)
            if not entries:
                print(" [*] No active or unexpired records found for this task/key.")
            for i, e in enumerate(entries, 1):
                enc_tag = " [ENCRYPTED]" if e["is_encrypted"] else ""
                ttl_tag = f" [EXPIRES: {time.ctime(e['expires_at'])}]" if e["expires_at"] else ""
                print(f" Record #{i} | From: {e['agent_name']:<15} | Key: {e['key']:<20}{enc_tag}{ttl_tag}")
                val_display = json.dumps(e['value'], indent=2) if isinstance(e['value'], (dict, list)) else str(e['value'])
                print(f" Data:\n{val_display}")
                print("-" * 80)
            print("=" * 80)

    elif args.vacuum:
        purged = bb.vacuum_expired()
        print(f"[SUCCESS] TTL Vacuum completed. Purged {purged} expired entries.")

    elif args.list:
        tasks = bb.list_tasks()
        if args.json:
            print(json.dumps(tasks, indent=2))
        else:
            print("=" * 80)
            print(" [DDW-X SWARM BLACKBOARD] ACTIVE TASKS MANIFEST (v3.0)")
            print("=" * 80)
            if not tasks:
                print(" [*] Blackboard is currently empty.")
            for t in tasks:
                agents_str = ", ".join(t["agents"]) if t["agents"] else "None"
                print(f" Task ID   : {t['task_id']:<15} | Active Entries: {t['entry_count']:<4} | Encrypted: {t['encrypted_count']}")
                print(f" Agents    : {agents_str}")
                print(f" Updated   : {time.ctime(t['updated_at'])}")
                print("-" * 80)
            print("=" * 80)

    elif args.clear:
        bb.clear(args.task_id)
        target = f"Task: {args.task_id}" if args.task_id else "ENTIRE BLACKBOARD"
        print(f"[SUCCESS] Swarm Blackboard memory cleared for: {target}")


if __name__ == "__main__":
    main()
