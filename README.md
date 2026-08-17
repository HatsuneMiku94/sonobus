# SonoBus — Windows Comfort Fork

> **Unofficial community fork of [SonoBus](https://github.com/sonosaurus/sonobus)** with a small set of Windows quality-of-life additions.
>
> The original SonoBus project, application, design, and upstream work belong to **Jesse Chappell / Sonosaurus and the SonoBus contributors**. This fork does **not** claim ownership of the original project. It only maintains clearly documented modifications on top of the upstream source.

This fork keeps SonoBus's normal behavior intact while adding a few convenient Windows desktop features that are useful for leaving SonoBus running in the background.

## What this fork adds

### Native minimize to system tray

On the Windows standalone application:

- Pressing **Minimize** removes the SonoBus window from the normal taskbar and keeps it running in the Windows notification area.
- **Left-click** the SonoBus tray icon to restore the window.
- **Right-click** the tray icon for **Open SonoBus** and **Exit SonoBus**.
- The normal window **Close (X)** button still exits SonoBus.
- Audio, networking, and the SonoBus process continue running while the window is hidden.
- The implementation is built directly into `SonoBus.exe`; there is no tray helper or companion process.

### Start with Windows, minimized to tray

The Windows standalone application's **Settings → OPTIONS** tab includes:

**Start with Windows (minimized to tray)**

When enabled:

- SonoBus starts automatically when the current Windows user signs in.
- It starts directly in the system tray instead of opening the main window.
- No administrator privileges, service, scheduled task, or helper executable are required.
- Disabling the option removes the startup entry again.

The startup entry follows the exact location of the `SonoBus.exe` that enabled it. If the executable is later moved, disable and re-enable the option from the new location.

For the full behavior and implementation notes, see **[WINDOWS_FEATURES.md](WINDOWS_FEATURES.md)**.

## Builds

The repository includes a Windows x64 GitHub Actions workflow that builds the standalone application and publishes a `SonoBus.exe` artifact.

The workflow verifies that the fork-specific Windows features are present, provisions SonoBus's existing ASIO SDK dependency, configures CMake, builds `SonoBus_Standalone`, and uploads the resulting executable.

There is **no patching step required** after cloning this fork. The Windows additions are part of the source tree itself.

For manual compilation details, see **[BUILD_WINDOWS.md](BUILD_WINDOWS.md)**.

## Fork philosophy

This is intentionally a **quality-of-life fork**, not a replacement project or a rebranding of SonoBus. The goals are to:

- keep upstream SonoBus recognizable and compatible;
- make small, practical desktop improvements where useful;
- preserve original copyright and attribution;
- keep every fork-specific change visible in source control;
- remain under the same open-source licensing terms as the upstream project.

A chronological record of fork-specific modifications is maintained in **[FORK_CHANGES.md](FORK_CHANGES.md)**.

---

# About SonoBus

**The information below describes the original SonoBus project.**

SonoBus is an easy-to-use application for streaming high-quality, low-latency peer-to-peer audio between devices over the internet or a local network.

Choose a unique group name, optionally add a password, and connect multiple people for music, remote sessions, podcasts, and other real-time audio use. SonoBus provides fine-grained control over latency, audio quality, and the overall mix, and includes recording, input processing, network statistics, and other audio tools.

SonoBus works as a standalone application on macOS, Windows, iOS, and Linux, and as an audio plugin on supported desktop platforms.

<img src="https://sonobus.net/assets/images/sonobus_screenshot.png" width="871" alt="SonoBus application screenshot" />

## Important usage notes from upstream

SonoBus does not use echo cancellation or automatic noise reduction in order to maintain high audio quality. If you have a live microphone signal, headphones are recommended to prevent echo and feedback.

For the lowest practical network latency, a wired Ethernet connection is preferred. Wi-Fi can introduce additional jitter and packet loss, requiring larger safety buffers and therefore higher latency.

SonoBus does not currently encrypt its audio/data communication. Audio is sent directly between users peer-to-peer; the connection server is primarily used so members of a group can find each other.

## Official SonoBus resources

- **Official project:** [sonobus.net](https://sonobus.net)
- **Original source repository:** [sonosaurus/sonobus](https://github.com/sonosaurus/sonobus)
- **This unofficial fork:** `PixelCat55/sonobus`

For official SonoBus releases, platform packages, general documentation, and upstream support, use the official SonoBus project resources above. Fork-specific Windows behavior should be reported against this fork rather than assumed to be part of upstream SonoBus.

## Building the upstream project

SonoBus uses CMake 3.15 or newer. The upstream repository contains its JUCE/AOO source dependencies and platform-specific project files. Platform build requirements still apply.

### macOS

With CMake and Xcode installed, the upstream helper scripts can be used:

```sh
./setupcmake.sh
./buildcmake.sh
```

### Windows

The Windows build requires CMake, Visual Studio/MSVC, and the ASIO SDK expected by the SonoBus CMake configuration. This fork's GitHub Actions workflow handles those requirements automatically for its x64 standalone build.

For a reproducible manual build of **this fork**, use **[BUILD_WINDOWS.md](BUILD_WINDOWS.md)** instead of relying on older helper-script assumptions.

### Linux

See [`linux/BUILDING.md`](linux/BUILDING.md) for the upstream Linux build instructions.

## License and third-party software

SonoBus was written by **Jesse Chappell** and is licensed under the **GNU General Public License v3.0**, with the repository's existing license exception where applicable. The full texts are provided in [`LICENSE`](LICENSE) and [`LICENSE_EXCEPTION`](LICENSE_EXCEPTION).

This fork preserves those license and copyright notices. Fork-specific modifications are distributed under the same applicable open-source terms; modifying this repository does not transfer ownership of the original SonoBus work to the maintainer of this fork.

SonoBus uses JUCE, AOO (Audio over OSC), Opus, and other third-party components whose own notices and licenses remain applicable.

## Upstream credits

Thanks belong to the original SonoBus authors and contributors, including the upstream development, documentation, testing, translation, JUCE/AOO, and other dependency contributors.

Original upstream credits include:

- **Jesse Chappell** — SonoBus author / maintainer
- **Christof Ressi** — AOO library
- **Sten Wessel** — Soundboard feature
- **Hannah Schellekens** — Soundboard feature
- **Michael Eskin** — documentation
- **Tony Becker** — documentation
- **RelationLife (Taewook Yang)** — translation

This fork's additions are intentionally documented separately in [`FORK_CHANGES.md`](FORK_CHANGES.md) so upstream work and fork-specific work remain easy to distinguish.
