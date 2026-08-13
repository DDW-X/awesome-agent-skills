#include <windows.h>
#include <stdio.h>

// Diagnostic testing payload for driver IOCTL dispatch
BOOL SendDiagnosticIOCTL(HANDLE hDevice, DWORD ioctlCode) {
    DWORD bytesReturned = 0;
    BYTE inBuffer[64] = {0};
    BYTE outBuffer[64] = {0};
    return DeviceIoControl(hDevice, ioctlCode, inBuffer, sizeof(inBuffer), outBuffer, sizeof(outBuffer), &bytesReturned, NULL);
}
