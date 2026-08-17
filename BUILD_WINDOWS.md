# Windows Build Guide

This fork's Windows tray and autostart features are already part of the source tree. No patch script or helper program is required before compiling.

## Requirements

- Windows 10 or 11
- Git
- CMake 3.15+
- Visual Studio with the Desktop development with C++ workload
- Steinberg ASIO SDK

SonoBus's existing CMake configuration expects the ASIO SDK at:

```text
../asiosdk/common
```

relative to the repository root. A typical layout is:

```text
ParentFolder\
├─ sonobus\
└─ asiosdk\
   └─ common\
      ├─ iasiodrv.h
      └─ ...
```

The ASIO requirement comes from the existing SonoBus Windows build; it is not introduced by this fork's tray/autostart features.

## Clone

```powershell
git clone https://github.com/PixelCat55/sonobus.git
cd sonobus
```

## Configure

```powershell
cmake -S . -B build -G "Visual Studio 17 2022" -A x64
```

## Build the standalone application

```powershell
cmake --build build --config Release --target SonoBus_Standalone --parallel 2
```

The resulting Release build contains the normal SonoBus standalone application plus this fork's native Windows tray integration and **Start with Windows (minimized to tray)** option.

## GitHub Actions

`.github/workflows/build-windows-native-tray.yml` performs the same x64 standalone build automatically. It provisions the ASIO SDK, verifies the fork-specific Windows source integration, configures CMake, builds `SonoBus_Standalone`, and uploads `SonoBus.exe` as an artifact.

A fresh clone of current `main` requires no fork-specific migration or patch step.
