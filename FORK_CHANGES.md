# Fork Changes

This repository is an **unofficial fork of SonoBus** (`sonosaurus/sonobus`).

It does **not** claim ownership of the original SonoBus project, branding, design, source history, or upstream contributions. The purpose of this fork is simply to maintain a small set of clearly documented quality-of-life modifications on top of the original project.

SonoBus remains licensed under the **GNU General Public License v3.0 (GPLv3)**, together with the repository's existing license exception where applicable. Original copyright and license notices are preserved.

## Fork goals

The fork is intended to stay close to upstream SonoBus while adding practical desktop conveniences, primarily for Windows users. Changes should be:

- small and understandable;
- optional where possible;
- implemented directly in source rather than through external helper processes;
- documented transparently;
- easy to distinguish from upstream SonoBus behavior.

## Current fork-specific modifications

### 1. Native Windows minimize-to-tray

**Added:** 2026-08-17

The Windows standalone SonoBus application now integrates directly with the Windows notification area.

Behavior:

- Clicking the normal Windows **Minimize** button hides the SonoBus main window from the taskbar.
- SonoBus continues running normally in the background.
- Audio and network processing remain active while the window is hidden.
- A SonoBus tray icon remains available in the Windows notification area.
- Left-clicking the tray icon restores the SonoBus window.
- Right-clicking the tray icon opens a context menu containing:
  - **Open SonoBus**
  - **Exit SonoBus**
- The normal window **Close (X)** button keeps its original behavior and exits SonoBus.

Implementation notes:

- The feature is native to the standalone application source.
- No sidecar tray program or helper process is used.
- The minimize handling is deferred through JUCE's message loop to avoid racing the native Windows minimize transition and leaving stale taskbar state.

### 2. Start with Windows, minimized to tray

**Added:** 2026-08-17

The Windows standalone application's **Settings → OPTIONS** tab now includes:

**Start with Windows (minimized to tray)**

Behavior:

- Enabling the toggle registers SonoBus to start for the **current Windows user** at sign-in.
- It uses the standard per-user Windows `Run` registry location under `HKEY_CURRENT_USER`.
- Administrator privileges are not required.
- The startup entry launches the current `SonoBus.exe` with the internal `--start-minimized` argument.
- At sign-in, SonoBus initializes normally but keeps the main window hidden and remains available from the system tray.
- Disabling the toggle removes the startup entry.
- The in-app toggle reads the actual registry state when the Options panel is opened or refreshed.

Path behavior:

The startup entry stores the exact executable path that enabled the option. If the user later moves or renames the executable, they should disable and re-enable the setting from the new location.

Runtime status:

This behavior has been compiled successfully through the repository's Windows GitHub Actions build and confirmed working in normal Windows runtime testing by the fork maintainer.

## Build integration

The fork-specific Windows changes are part of the normal source tree. There is **no patch script** or post-checkout transformation required.

The repository includes a Windows x64 GitHub Actions workflow that:

- checks out `main`;
- provisions SonoBus's existing Steinberg ASIO SDK dependency;
- verifies the tray and autostart source integration;
- configures the project with CMake and Visual Studio;
- builds the `SonoBus_Standalone` target;
- uploads the resulting `SonoBus.exe` as an artifact.

For manual Windows build information, see [`BUILD_WINDOWS.md`](BUILD_WINDOWS.md).

## Upstream relationship

Original project: **SonoBus** by Jesse Chappell / Sonosaurus and the upstream contributors.

Original repository:

`https://github.com/sonosaurus/sonobus`

This repository:

`https://github.com/PixelCat55/sonobus`

This fork is **not an official SonoBus release**. General SonoBus bugs and upstream behavior belong to the original project; issues caused specifically by the modifications documented here belong to this fork.

## Ownership and attribution

The maintainer of this fork claims ownership only over new fork-specific contributions to the extent allowed by the applicable license. No ownership is claimed over the original SonoBus project or upstream work.

The intent is to keep attribution straightforward: **SonoBus is SonoBus; this fork simply adds optional convenience features on top of it.**

## License

This fork is distributed under the same applicable open-source licensing terms as upstream SonoBus. See:

- [`LICENSE`](LICENSE)
- [`LICENSE_EXCEPTION`](LICENSE_EXCEPTION)

Third-party dependencies retain their own copyright and license terms.
