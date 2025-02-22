#include <stdlib.h>
#include <windows.h>
#include <stdio.h>

__declspec(dllexport) double get_cpu_usage() {
    FILETIME idleTime, kernelTime, userTime;
    double cpu_usage;
    if (GetSystemTimes(&idleTime, &kernelTime, &userTime)) {
        cpu_usage = (double)idleTime.dwLowDateTime;
    }
    return cpu_usage;
}

__declspec(dllexport) double get_memory_stats() {
    MEMORYSTATUSEX statex;
    statex.dwLength = sizeof(statex);
    float all_memory, free_memory, in_use_memory;
    
    if (GlobalMemoryStatusEx(&statex)) {
        in_use_memory = (float)statex.dwMemoryLoad;
    }
    return in_use_memory;
}

__declspec(dllexport) double get_disk_usage() {
    ULARGE_INTEGER freeBytesAvailable, totalBytes, freeBytes;
    double memory_used;
    char path[] = "C:\\";

    if (GetDiskFreeSpaceEx(path, &freeBytesAvailable, &totalBytes, &freeBytes)) {
        memory_used = (double)(totalBytes.QuadPart - freeBytes.QuadPart) / (1024 * 1024 * 1024);
    } else {
        printf("Error getting disk information\n");
    }

    return memory_used;
}