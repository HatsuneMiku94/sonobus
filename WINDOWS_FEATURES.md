# Windows Fork Features

This document describes the Windows-only quality-of-life features added by the unofficial `PixelCat55/sonobus` fork.

These additions are **not part of upstream SonoBus unless separately adopted there**. The original SonoBus project remains at `sonosaurus/sonobus`.

## Native minimize to system tray

The standalone Windows application keeps the normal Windows title bar and minimize button.

When SonoBus is minimized:

1. Windows completes the native minimize transition.
2. The SonoBus window is hidden from the normal taskbar.
3. The process continues running normally.
4. The system tray icon remains available.

### Tray controls

- **Left-click:** restore the SonoBus main window.
- **Right-click → Open SonoBus:** restore the main window.
- **Right-click → Exit SonoBus:** request a normal SonoBus shutdown.

The normal window **Close (X)** button is intentionally unchanged and exits the application rather than hiding it to the tray.

## Start with Windows, minimized to tray

Open:

**SonoBus Settings → OPTIONS**

and use:

**Start with Windows (minimized to tray)**

### When enabled

SonoBus writes a per-user startup entry under:

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

The value is named:

```text
SonoBus
```

and launches the current executable with:

```text
--start-minimized
```

Because this uses `HKEY_CURRENT_USER`, enabling or disabling the option does not normally require Administrator privileges.

### Startup behavior

When launched with `--start-minimized`, SonoBus still initializes the standalone application and audio/network systems, but the main window is not shown. The tray icon provides access to restore or exit the application.

### Moving the executable

The startup entry contains the exact path to the `SonoBus.exe` that enabled the setting.

If you move or rename the executable afterward:

1. launch SonoBus from its new location;
2. open **Settings → OPTIONS**;
3. disable **Start with Windows (minimized to tray)** if it still appears enabled;
4. enable it again.

This updates Windows to use the new executable path.

## Scope

These features are currently intended only for the **Windows standalone application**.

They do not change the behavior of SonoBus plugin formats, macOS, Linux, iOS, or Android builds.

## Implementation principles

The fork deliberately avoids external utilities for these features:

- no tray helper executable;
- no Windows service;
- no scheduled task;
- no separate launcher;
- no required Administrator elevation.

The tray and startup behavior are compiled directly into the SonoBus standalone source.

## Troubleshooting

### The startup toggle is enabled but SonoBus no longer starts

The executable may have been moved or renamed. Disable and re-enable the option from the executable's current location.

### SonoBus appears in the taskbar after minimizing

Make sure you are running a build from this fork that includes the native tray integration. Builds from upstream SonoBus do not automatically contain these fork-specific features.

### I want Close (X) to hide to tray too

That is not the current behavior. Close deliberately retains SonoBus's normal quit behavior. Only **Minimize** sends the application to the tray.

## Reporting fork-specific issues

When reporting a problem with these features, include:

- Windows version;
- SonoBus fork build/commit if known;
- whether the problem occurs with manual launch, startup launch, or both;
- whether the tray icon is visible;
- whether audio/network operation continues in the background.
