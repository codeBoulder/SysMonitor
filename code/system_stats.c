#include <stdlib.h>
#include <windows.h>
#include <stdio.h>

__declspec(dllexport) double get_cpu_usage()
{
    FILETIME idleTime, kernelTime, userTime;
    static FILETIME preIdleTime, preKernelTime, preUserTime;

    if (!GetSystemTimes(&idleTime, &kernelTime, &userTime))
        return -1.0;

    ULONGLONG idle = (*(ULONGLONG*)&idleTime) - (*(ULONGLONG*)&preIdleTime);
    ULONGLONG kernel = (*(ULONGLONG*)&kernelTime) - (*(ULONGLONG*)&preKernelTime);
    ULONGLONG user = (*(ULONGLONG*)&userTime) - (*(ULONGLONG*)&preUserTime);

    preIdleTime = idleTime;
    preKernelTime = kernelTime;
    preUserTime = userTime;

    return (double)(kernel + user - idle) * 100.0 / (kernel + user);
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