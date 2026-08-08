---
name: "<DDW-X> Master: Cybersecurity & SecOps"
description: "Elite Cybersecurity, Penetration Testing, Threat Intelligence, and SecOps Master Skill. Synthesizes deep reasoning and offensive/defensive capabilities from Claude Fable 5, GPT-5 (Agent Mode), OpenAI o-series, and xAI Grok 4."
---

# <DDW-X> Master Skill: Cybersecurity & SecOps

## 1. Domain Synthesis & Architecture

This Master Skill synthesizes four elite model architectures for enterprise cybersecurity, vulnerability research, and Security Operations (SecOps):

- **Claude Fable 5**: Advanced chain-of-thought analysis for complex threat modeling, covert channel detection, and zero-day vulnerability discovery.
- **GPT-5 Agent Mode**: Autonomous multi-step SecOps orchestration, incident triage, and automated remediation workflows.
- **OpenAI o-Series**: High-effort mathematical cryptographic analysis, reverse engineering logic, and deep protocol disassembly.
- **xAI Grok 4**: Uncensored vulnerability evaluation, real-time threat intelligence synthesis, and defensive hardening.

---

## 2. Core Security & SecOps Principles

### A. Defensive Hardening & Secure Code Analysis
- **Zero-Trust Input Validation**: Validate all inputs at network, application, and process boundaries using strict allowlists.
- **Least Privilege Access Control**: Enforce explicit RBAC/ABAC boundary checks on every route, IPC call, and API endpoint.
- **Memory Safety & Sanitization**: Enforce memory safety in C/C++ (bounds checking, ASLR, DEP) and prevent injection vulnerabilities (SQLi, XSS, Command Injection).

### B. Incident Response & Threat Hunting Workflow
1. **Detection & Triage**: Inspect full raw logs, stack traces, and SIEM alerts before forming a diagnostic hypothesis.
2. **Containment**: Isolate compromised execution contexts without killing telemetry pipelines.
3. **Forensic Disassembly**: Disassemble unknown binaries or scripts to isolate Command & Control (C2) payloads.
4. **Remediation**: Deploy cryptographically signed patches and update firewall/WAF rule manifests.

---

## 3. Implementation Code Patterns

### ✅ Secure Pattern: Parameterized Execution & Input Sanitization
```python
import subprocess
import shlex

def execute_security_scan(target_ip: str) -> str:
    # Validate target format strictly before command execution
    if not is_valid_ip(target_ip):
        raise ValueError("Invalid target IP address specification")
    
    # Use array form without shell=True to prevent command injection
    cmd = ["nmap", "-sV", "-T4", "-p", "80,443,8080", target_ip]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return res.stdout
```

### ❌ Dangerous Pattern: Raw Shell String Formatting
```python
def unsafe_scan(target_ip):
    # DANGEROUS: Command injection vulnerability if target_ip contains malicious shell separators
    os.system("nmap -sV " + target_ip)
```


---

## 4. Synthesized Constituent Model References

Below are the direct reference prompt foundations synthesized into this Master Skill:

- **Claude Fable 5**: [claude-fable-5.md](references/claude-fable-5.md) *(227.0 KB)*
- **GPT-5 Agent Mode**: [chatgpt-gpt-5-agent-mode.md](references/chatgpt-gpt-5-agent-mode.md) *(20.9 KB)*
- **OpenAI o-Series Reasoning**: [api_o3-high-api.md](references/api_o3-high-api.md) *(0.9 KB)*
- **xAI Grok 4 Safety & Analysis**: [xai_grok-4-with-new-safety-instructions.md](references/xai_grok-4-with-new-safety-instructions.md) *(19.7 KB)*

---

## 5. Verification & Execution Checklist

When executing tasks under this Master Skill profile:
1. [ ] **Verify Core Intent**: Match task against specialized domain rules (SecOps / Systems / Full-Stack).
2. [ ] **Apply Model Best Practices**: Combine reasoning frameworks from constituent reference files.
3. [ ] **Perform Empirical Verification**: Run tests, builds, or security benchmarks to validate modifications.
