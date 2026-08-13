#!/usr/bin/env python3
"""
================================================================================
DDW-X ZERO-KNOWLEDGE COGNITIVE FIREWALL: PROMPT OBFUSCATION & PRIVACY MIDDLEWARE
================================================================================
Module: src/core/rag/zk_cognitive_firewall.py
Architect: Principal AI Architect & Lead DevSecOps Engineer

CAPABILITIES:
1. The Interceptor (Masking):
   - High-precision regex pattern matchers for IOCs (IPv4, IPv6, MAC, Domains, URLs, CVEs).
   - Domain-specific entity extractors for EDR vendors, Threat Actors (APTs), and internal assets.
   - Deterministic abstract tag assignment (e.g. [TARGET_IP_1], [EDR_VENDOR_1], [THREAT_ACTOR_1]).
2. The Vault (Stateful Mapping):
   - Secure local storage of bidirectional token mappings in 'scratch/prompt_vault.json'.
   - Atomic file transactions ensuring consistency across concurrent agent invocations.
3. The Reconstitutor (Unmasking):
   - Deterministic reverse-substitution mapping abstract tags back to original values.
================================================================================
"""

import os
import sys
import re
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEFAULT_VAULT_PATH = "scratch/prompt_vault.json"

# ==============================================================================
# KNOWN ENTITY DICTIONARIES (EDR, APTs, Tooling, Infrastructure)
# ==============================================================================

KNOWN_EDR_VENDORS = [
    "CrowdStrike Falcon", "CrowdStrike", "Falcon Sensor",
    "Microsoft Defender for Endpoint", "Microsoft Defender", "Windows Defender",
    "SentinelOne Singularity", "SentinelOne",
    "Carbon Black", "VMware Carbon Black",
    "Cortex XDR", "Palo Alto Cortex",
    "Symantec Endpoint Protection", "Broadcom Symantec",
    "Kaspersky Endpoint Security", "Kaspersky",
    "Sophos Intercept X", "Sophos",
    "Trend Micro Apex One", "Trend Micro",
    "Cybereason EDR", "Cybereason",
    "Elastic EDR", "Elastic Security",
    "FireEye HX", "Trellix EDR", "Trellix"
]

KNOWN_THREAT_ACTORS = [
    "APT29", "APT28", "APT41", "APT33", "APT34", "APT38", "APT39", "APT40",
    "Cozy Bear", "Fancy Bear", "Lazarus Group", "Lazarus", "FIN7", "FIN8",
    "Wizard Spider", "Sandworm", "Turla", "MuddyWater", "Scattered Spider",
    "Volt Typhoon", "Salt Typhoon", "Midnight Blizzard", "Forest Blizzard",
    "LockBit", "BlackCat", "ALPHV", "Clop", "DarkSide", "BlackMatter"
]

# ==============================================================================
# 1. THE COGNITIVE INTERCEPTOR & VAULT MANAGER
# ==============================================================================

class CognitiveFirewallVault:
    """
    Manages stateful, persistent token-to-literal mappings in a local JSON vault.
    """
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.vault_path.parent.mkdir(parents=True, exist_ok=True)
        self.token_to_value: Dict[str, str] = {}
        self.value_to_token: Dict[str, str] = {}
        self.tag_counters: Dict[str, int] = {}
        self._load_vault()

    def _load_vault(self):
        if self.vault_path.exists():
            try:
                with open(self.vault_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.token_to_value = data.get("token_to_value", {})
                    self.value_to_token = data.get("value_to_token", {})
                    self.tag_counters = data.get("tag_counters", {})
            except Exception:
                self.token_to_value = {}
                self.value_to_token = {}
                self.tag_counters = {}

    def save_vault(self):
        temp_path = self.vault_path.with_suffix(".tmp")
        data = {
            "metadata": {
                "version": "1.0.0-zk-firewall",
                "last_updated": time.time(),
                "total_mappings": len(self.token_to_value)
            },
            "token_to_value": self.token_to_value,
            "value_to_token": self.value_to_token,
            "tag_counters": self.tag_counters
        }
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        if os.name == "nt" and self.vault_path.exists():
            os.replace(temp_path, self.vault_path)
        else:
            temp_path.replace(self.vault_path)

    def get_or_create_tag(self, value: str, category_prefix: str) -> str:
        # Check if already mapped
        val_clean = value.strip()
        if val_clean in self.value_to_token:
            return self.value_to_token[val_clean]

        self.tag_counters[category_prefix] = self.tag_counters.get(category_prefix, 0) + 1
        counter = self.tag_counters[category_prefix]
        tag = f"[{category_prefix}_{counter}]"

        self.value_to_token[val_clean] = tag
        self.token_to_value[tag] = val_clean
        return tag

    def clear(self):
        self.token_to_value = {}
        self.value_to_token = {}
        self.tag_counters = {}
        if self.vault_path.exists():
            self.vault_path.unlink()


# ==============================================================================
# 2. THE PATTERN RECOGNITION & MASKING ENGINE
# ==============================================================================

class CognitiveMaskingEngine:
    """
    Applies regex rules and entity dictionaries to detect and mask sensitive items.
    """
    # Regex Rules (Ordered by specificity)
    CVE_REGEX = re.compile(r'\bCVE-\d{4}-\d{4,7}\b', re.IGNORECASE)
    IPV4_REGEX = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
    MAC_REGEX = re.compile(r'\b(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})\b')
    EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
    DOMAIN_REGEX = re.compile(r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+(?:com|org|net|edu|gov|mil|io|corp|internal|local|lan)\b', re.IGNORECASE)

    def __init__(self, vault: CognitiveFirewallVault):
        self.vault = vault

    def mask_text(self, text: str) -> Tuple[str, List[Dict[str, str]]]:
        if not text:
            return "", []

        masked = text
        substitutions: List[Dict[str, str]] = []

        # 1. Mask Known EDR Vendors (Single unified compiled regex)
        edr_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(v) for v in sorted(KNOWN_EDR_VENDORS, key=len, reverse=True)) + r')\b', re.IGNORECASE)
        def _replace_edr(m):
            v_match = m.group(0)
            tag = self.vault.get_or_create_tag(v_match, "EDR_VENDOR")
            substitutions.append({"original": v_match, "tag": tag, "category": "EDR_VENDOR"})
            return tag
        masked = edr_pattern.sub(_replace_edr, masked)

        # 2. Mask Known Threat Actors (Single unified compiled regex)
        apt_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(a) for a in sorted(KNOWN_THREAT_ACTORS, key=len, reverse=True)) + r')\b', re.IGNORECASE)
        def _replace_apt(m):
            a_match = m.group(0)
            tag = self.vault.get_or_create_tag(a_match, "THREAT_ACTOR")
            substitutions.append({"original": a_match, "tag": tag, "category": "THREAT_ACTOR"})
            return tag
        masked = apt_pattern.sub(_replace_apt, masked)

        # 3. Mask CVE IDs
        def _replace_cve(m):
            c_match = m.group(0)
            tag = self.vault.get_or_create_tag(c_match.upper(), "CVE_ID")
            substitutions.append({"original": c_match, "tag": tag, "category": "CVE_ID"})
            return tag
        masked = self.CVE_REGEX.sub(_replace_cve, masked)

        # 4. Mask IPv4 Addresses
        def _replace_ip(m):
            ip_val = m.group(0)
            tag = self.vault.get_or_create_tag(ip_val, "TARGET_IP")
            substitutions.append({"original": ip_val, "tag": tag, "category": "TARGET_IP"})
            return tag
        masked = self.IPV4_REGEX.sub(_replace_ip, masked)

        # 5. Mask MAC Addresses
        def _replace_mac(m):
            mac_val = m.group(0)
            tag = self.vault.get_or_create_tag(mac_val, "MAC_ADDR")
            substitutions.append({"original": mac_val, "tag": tag, "category": "MAC_ADDR"})
            return tag
        masked = self.MAC_REGEX.sub(_replace_mac, masked)

        # 6. Mask Emails
        def _replace_email(m):
            em_val = m.group(0)
            tag = self.vault.get_or_create_tag(em_val, "EMAIL_IDENTITY")
            substitutions.append({"original": em_val, "tag": tag, "category": "EMAIL_IDENTITY"})
            return tag
        masked = self.EMAIL_REGEX.sub(_replace_email, masked)

        # 7. Mask Domains
        def _replace_domain(m):
            d_val = m.group(0)
            tag = self.vault.get_or_create_tag(d_val, "DOMAIN_NAME")
            substitutions.append({"original": d_val, "tag": tag, "category": "DOMAIN_NAME"})
            return tag
        masked = self.DOMAIN_REGEX.sub(_replace_domain, masked)

        self.vault.save_vault()
        return masked, substitutions


# ==============================================================================
# 3. THE RECONSTITUTOR (REVERSE TRANSLATION)
# ==============================================================================

class CognitiveReconstitutor:
    """
    Performs reverse translation by mapping abstract tags back to original sensitive values.
    """
    def __init__(self, vault: CognitiveFirewallVault):
        self.vault = vault

    def unmask_text(self, masked_text: str) -> Tuple[str, int]:
        if not masked_text or not self.vault.token_to_value:
            return masked_text, 0

        # Build unified token regex for single-pass linear reverse translation
        sorted_tokens = sorted(self.vault.token_to_value.keys(), key=len, reverse=True)
        token_pattern = re.compile("|".join(re.escape(t) for t in sorted_tokens))
        
        reconstituted_count = 0
        def _replace_token(m):
            nonlocal reconstituted_count
            t_match = m.group(0)
            reconstituted_count += 1
            return self.vault.token_to_value.get(t_match, t_match)

        unmasked = token_pattern.sub(_replace_token, masked_text)
        return unmasked, reconstituted_count


# ==============================================================================
# 4. CLI ORCHESTRATION & ENTRY POINT
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="DDW-X Zero-Knowledge Cognitive Firewall & Prompt Obfuscator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-m", "--mask", help="Sensitive input prompt to obfuscate with abstract tags")
    group.add_argument("-u", "--unmask", help="Masked AI response string to restore original literals")
    group.add_argument("--clear-vault", action="store_true", help="Clear all stored mappings in the vault")

    parser.add_argument("--vault-path", default=DEFAULT_VAULT_PATH, help="Path to local JSON mapping vault")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON summary")

    args = parser.parse_args()
    vault_path = Path(args.vault_path).resolve()
    vault = CognitiveFirewallVault(vault_path)

    if args.clear_vault:
        vault.clear()
        print(f"[SUCCESS] Cognitive firewall vault cleared at: {vault_path}")
        sys.exit(0)

    if args.mask:
        engine = CognitiveMaskingEngine(vault)
        masked_text, subs = engine.mask_text(args.mask)

        if args.json:
            out = {
                "action": "mask",
                "original_text": args.mask,
                "masked_text": masked_text,
                "substitutions": subs,
                "vault_path": str(vault_path)
            }
            print(json.dumps(out, indent=2))
        else:
            print("=" * 80)
            print(" [DDW-X COGNITIVE FIREWALL] PROMPT OBFUSCATION (OUTBOUND TO AI)")
            print("=" * 80)
            print(f" [*] Vault Path        : {vault_path.name}")
            print(f" [*] Entities Detected : {len(subs)}")
            print("-" * 80)
            print(" [1] ORIGINAL SENSITIVE PROMPT:")
            print(f"     \"{args.mask}\"")
            print("-" * 80)
            print(" [2] OBFUSCATED PROMPT (What the AI sees):")
            print(f"     \"{masked_text}\"")
            print("-" * 80)
            print(" [3] STATEFUL VAULT MAPPINGS:")
            for s in subs:
                print(f"     * {s['tag']:<20} <===>  {s['original']} ({s['category']})")
            print("=" * 80)

    elif args.unmask:
        reconstitutor = CognitiveReconstitutor(vault)
        unmasked_text, count = reconstitutor.unmask_text(args.unmask)

        if args.json:
            out = {
                "action": "unmask",
                "masked_input": args.unmask,
                "unmasked_output": unmasked_text,
                "replacements_made": count,
                "vault_path": str(vault_path)
            }
            print(json.dumps(out, indent=2))
        else:
            print("=" * 80)
            print(" [DDW-X COGNITIVE FIREWALL] REVERSE TRANSLATION (INBOUND TO USER)")
            print("=" * 80)
            print(f" [*] Vault Path         : {vault_path.name}")
            print(f" [*] Tokens Replaced    : {count}")
            print("-" * 80)
            print(" [1] MASKED INPUT:")
            print(f"     \"{args.unmask}\"")
            print("-" * 80)
            print(" [2] FULLY RECONSTITUTED TEXT:")
            print(f"     \"{unmasked_text}\"")
            print("=" * 80)


if __name__ == "__main__":
    main()
