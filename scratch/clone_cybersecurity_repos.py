import os
import subprocess
import sys
import shutil

REPOSITORIES = [
    "https://github.com/rshipp/awesome-malware-analysis",
    "https://github.com/HuskyHacks/PMAT-labs",
    "https://github.com/OALabs/Lab-Notes",
    "https://github.com/infosecn1nja/Red-Teaming-Toolkit",
    "https://github.com/requie/AI-Red-Teaming-Guide",
    "https://github.com/Threekiii/Awesome-Redteam",
    "https://github.com/MorDavid/awesome-cyber-security-mcp",
    "https://github.com/LaurieWired/GhidraMCP",
    "https://github.com/mukul975/Anthropic-Cybersecurity-Skills",
    "https://github.com/matank001/cursor-security-rules",
    "https://github.com/offensive-security/exploitdb",
    "https://github.com/swisskyrepo/PayloadsAllTheThings",
    "https://github.com/trickest/cve",
    "https://github.com/redcanaryco/atomic-red-team",
    "https://github.com/Cobalt-Strike/community_kit",
    "https://github.com/JhonMA82/awesome-clinerules"
]

def get_repo_name(url: str) -> str:
    name = url.rstrip("/").split("/")[-1]
    if name.endswith(".git"):
        name = name[:-4]
    return name

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(root_dir, "cs")
    
    os.makedirs(target_dir, exist_ok=True)
    print(f"[*] Target directory: {target_dir}")
    print(f"[*] Total repositories to clone: {len(REPOSITORIES)}")
    print("=" * 60)

    results = []

    for idx, repo_url in enumerate(REPOSITORIES, 1):
        repo_name = get_repo_name(repo_url)
        dest_path = os.path.join(target_dir, repo_name)
        
        print(f"\n[{idx}/{len(REPOSITORIES)}] Processing: {repo_name} ({repo_url})")

        if os.path.exists(dest_path):
            if os.path.isdir(dest_path) and os.path.exists(os.path.join(dest_path, ".git")):
                print(f"    [!] Destination '{repo_name}' already exists and contains a git repository. Skipping clone.")
                results.append((repo_name, repo_url, "SKIPPED (Already exists)"))
                continue
            else:
                print(f"    [!] Directory '{repo_name}' exists but is not a valid git repo.")

        cmd = ["git", "clone", "--depth", "1", repo_url, dest_path]
        print(f"    Executing: {' '.join(cmd)}")

        try:
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )

            if process.returncode == 0:
                print(f"    [+] Successfully cloned: {repo_name}")
                results.append((repo_name, repo_url, "SUCCESS"))
            else:
                print(f"    [-] Failed to clone {repo_name}. Exit code: {process.returncode}")
                if process.stderr:
                    print(f"    Error output:\n{process.stderr.strip()}")
                results.append((repo_name, repo_url, f"FAILED (Exit code {process.returncode})"))

        except subprocess.TimeoutExpired:
            print(f"    [-] Timeout expired while cloning {repo_name}")
            results.append((repo_name, repo_url, "FAILED (Timeout)"))
        except Exception as ex:
            print(f"    [-] Unexpected error: {ex}")
            results.append((repo_name, repo_url, f"FAILED ({type(ex).__name__}: {ex})"))

    print("\n" + "=" * 60)
    print("SUMMARY OF CLONING OPERATIONS")
    print("=" * 60)
    
    success_count = 0
    skipped_count = 0
    failed_count = 0

    for name, url, status in results:
        status_tag = f"[{status}]"
        print(f"{status_tag:<30} {name} -> {url}")
        if "SUCCESS" in status:
            success_count += 1
        elif "SKIPPED" in status:
            skipped_count += 1
        else:
            failed_count += 1

    print("-" * 60)
    print(f"Total: {len(REPOSITORIES)} | Succeeded: {success_count} | Skipped: {skipped_count} | Failed: {failed_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
