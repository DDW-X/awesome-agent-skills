# Threat Intelligence Bulletin: APT-Emulation TTP Matrix

## Overview
Adversaries frequently employ indirect syscall stubs to circumvent user-mode API hooking in Endpoint Detection and Response (EDR) solutions.

### Key Telemetry Triggers:
- Sysmon Event ID 1: Process Creation with anomalous command lines
- Sysmon Event ID 8: CreateRemoteThread across session boundaries
- Sysmon Event ID 10: ProcessAccess requesting PROCESS_VM_WRITE and PROCESS_VM_OPERATION
