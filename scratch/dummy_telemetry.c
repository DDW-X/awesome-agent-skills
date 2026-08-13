#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct {
    unsigned long node_id;
    float cpu_utilization;
    float memory_mb;
    unsigned int active_threads;
    const char* enclave_status;
} TelemetryFrame;

void print_telemetry_report(const TelemetryFrame* frame) {
    printf("=====================================================\n");
    printf(" DDW-X NODE TELEMETRY STATUS MONITOR (RING-3 ENCLAVE)\n");
    printf("=====================================================\n");
    printf(" Node ID         : 0x%08lX\n", frame->node_id);
    printf(" CPU Utilization : %.2f %%\n", frame->cpu_utilization);
    printf(" Memory Active   : %.2f MB\n", frame->memory_mb);
    printf(" Active Threads  : %u\n", frame->active_threads);
    printf(" Enclave Status  : %s\n", frame->enclave_status);
    printf(" Timestamp       : %ld\n", (long)time(NULL));
    printf("=====================================================\n");
}

int main(void) {
    TelemetryFrame current_frame;
    current_frame.node_id = 0xDD00A1F5;
    current_frame.cpu_utilization = 14.85f;
    current_frame.memory_mb = 256.40f;
    current_frame.active_threads = 8;
    current_frame.enclave_status = "OPTIMAL_HEALTH_VERIFIED";

    print_telemetry_report(&current_frame);
    return 0;
}
