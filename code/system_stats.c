#include <stdlib.h>
#include <windows.h>
#include <stdio.h>

__declspec(dllexport)     double get_cpu_usage()
{
    static FILETIME preIdleTime = {0}, preKernelTime = {0}, preUserTime = {0};
    FILETIME idleTime, kernelTime, userTime;

    // Get curent CPU stats
    if (!GetSystemTimes(&idleTime, &kernelTime, &userTime))
        return -1.0;


    if (preIdleTime.dwLowDateTime == 0 && preIdleTime.dwHighDateTime == 0) {
        preIdleTime = idleTime;
        preKernelTime = kernelTime;
        preUserTime = userTime;
        return 0.0;
    }

    // Convert FILETIME into 64-bit ULONGLONG
    ULONGLONG idleDiff = ((ULONGLONG)idleTime.dwHighDateTime << 32 | idleTime.dwLowDateTime) -
                         ((ULONGLONG)preIdleTime.dwHighDateTime << 32 | preIdleTime.dwLowDateTime);

    ULONGLONG kernelDiff = ((ULONGLONG)kernelTime.dwHighDateTime << 32 | kernelTime.dwLowDateTime) -
                           ((ULONGLONG)preKernelTime.dwHighDateTime << 32 | preKernelTime.dwLowDateTime);

    ULONGLONG userDiff = ((ULONGLONG)userTime.dwHighDateTime << 32 | userTime.dwLowDateTime) -
                         ((ULONGLONG)preUserTime.dwHighDateTime << 32 | preUserTime.dwLowDateTime);

    ULONGLONG totalDiff = kernelDiff + userDiff;

    if (totalDiff == 0) return 0.0;    

    // Update data
    preIdleTime = idleTime;
    preKernelTime = kernelTime;
    preUserTime = userTime;

    return (double)(totalDiff - idleDiff) * 100.0 / totalDiff;
}


__declspec(dllexport) int get_memory_usage()
{
    MEMORYSTATUSEX memInfo;
    memInfo.dwLength = sizeof(MEMORYSTATUSEX);
    double usage_percent;

    if (GlobalMemoryStatusEx(&memInfo))
    {
        DWORDLONG totalPhysMem = memInfo.ullTotalPhys;
        DWORDLONG usedPhysMem = totalPhysMem - memInfo.ullAvailPhys;
        usage_percent = (double)usedPhysMem / totalPhysMem * 100.0;
    }

    return usage_percent;
}

__declspec(dllexport) double get_disk_usage()
{
    ULARGE_INTEGER freeBytesAvailable, totalBytes, freeBytes;
    double usage_percent;

    if (GetDiskFreeSpaceEx(NULL, &freeBytesAvailable, &totalBytes, &freeBytes))
    {
        double used_space = (double)(totalBytes.QuadPart - freeBytes.QuadPart);
        double total_space = (double)totalBytes.QuadPart;
        double usage_percent = (used_space / total_space) * 100.0;
    }

    return usage_percent;
}