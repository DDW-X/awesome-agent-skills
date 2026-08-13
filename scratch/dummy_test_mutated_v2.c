
// --- [DDW-X SYNTHETIC CFF STATE-MACHINE DISPATCHER] ---
#define _STATE_INIT 0x10
#define _STATE_EXEC 0x20
#define _STATE_EXIT 0x30

#include <stdlib.h>
#include <string.h>
static const unsigned char _enc_str_0_347[] = { 0x24, 0x0A, 0x13, 0x03, 0x46, 0x32, 0x03, 0x07, 0x0B, 0x46, 0x2E, 0x03, 0x13, 0x14, 0x0F, 0x15, 0x12, 0x0F, 0x05, 0x46, 0x32, 0x14, 0x07, 0x0F, 0x08, 0x0F, 0x08, 0x01, 0x46, 0x27, 0x14, 0x12, 0x0F, 0x00, 0x07, 0x05, 0x12 };
// --- [DDW-X MULTI-LAYER BASE64 + DUAL-XOR DECODER] ---
static char* _zk_decode_layer2(const unsigned char* enc, size_t len, unsigned char k1, unsigned char k2) {
    do {{ volatile unsigned long _t_pad = 0xCAFEBABE; }} while (0);
    char* buf = (char*)malloc(len + 1);
    if (!buf) return NULL;
    for (size_t i = 0; i < len; i++) {

    volatile int _cff_state = _STATE_INIT;
    while (_cff_state != _STATE_EXIT) {
    do {{ volatile unsigned long _t_pad = 0xCAFEBABE; }} while (0);
        switch (_cff_state) {
    if ((0xDEAD ^ 0xDEAD) != 0) {{ volatile int _dummy_trap = 0x1337; }}
            case _STATE_INIT:
                _cff_state = _STATE_EXEC;
                break;
            case _STATE_EXEC:
                _cff_state = _STATE_EXIT;
                break;
            default:
                _cff_state = _STATE_EXIT;
                break;
        }
    }
        buf[i] = (char)(enc[i] ^ k2 ^ k1);
    }
    buf[len] = '\0';
    return buf;
}

#include <stdio.h>

void _tes_GxFVC6gu() {
    printf(_zk_decode_layer2(_enc_str_0_347, sizeof(_enc_str_0_347), 0x55, 0x33));
}