# Fork Changes

This repository is an **unofficial fork of SonoBus** (`sonosaurus/sonobus`).

This fork does **not** claim ownership of the original SonoBus project or its upstream work; it only maintains additional modifications and quality-of-life features on top of the original project.

SonoBus remains licensed under the **GNU General Public License v3.0 (GPLv3)**. This fork preserves the original license and copyright notices and publishes its modifications under the same license.

## Purpose of this fork

The goal of this fork is to add practical quality-of-life improvements to SonoBus while keeping the original application and workflow intact.

## Current modifications

### Windows native minimize-to-tray support

Added on **2026-08-17**.

- Adds a native Windows system tray icon to the standalone SonoBus application.
- Minimizing SonoBus hides the main window from the normal Windows taskbar while keeping audio and network activity running.
- Clicking the tray icon restores the main SonoBus window.
- The tray context menu provides **Open SonoBus** and **Exit SonoBus** actions.
- The normal window **Close (X)** button still exits the application.
- The tray functionality is compiled directly into `SonoBus.exe`; no companion helper process is required.

## Building this fork

The minimize-to-tray implementation is part of the source code directly, so there is **no fork-specific patch step** required before compiling.

The repository also includes a Windows x64 GitHub Actions workflow that provisions SonoBus's existing ASIO SDK dependency automatically and builds the standalone application.

## Upstream

Original project: **SonoBus** by its original authors and contributors.

This fork is not an official SonoBus release. Issues caused specifically by modifications in this fork should be reported here rather than to the upstream project.

## License

This fork is distributed under the same **GNU General Public License v3.0** terms as the upstream project. See the repository's `LICENSE` file for the full license text.
