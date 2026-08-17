from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


window_path = Path("Source/SonoStandaloneFilterWindow.h")
window = window_path.read_text(encoding="utf-8")

marker = """#if JUCE_WINDOWS
    void minimisationStateChanged (bool isNowMinimised) override
"""
helpers = """#if JUCE_WINDOWS
    static String getWindowsStartupRegistryPath()
    {
        return "HKEY_CURRENT_USER\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run\\\\SonoBus";
    }

    static String getWindowsStartupCommand()
    {
        const auto executablePath = File::getSpecialLocation (File::currentExecutableFile).getFullPathName();
        return "\\\"" + executablePath + "\\\" --start-minimized";
    }

    bool isStartWithWindowsEnabled() const
    {
        return WindowsRegistry::getValue (getWindowsStartupRegistryPath()).trim() == getWindowsStartupCommand();
    }

    bool setStartWithWindowsEnabled (bool shouldEnable)
    {
        const auto registryPath = getWindowsStartupRegistryPath();
        if (shouldEnable)
            return WindowsRegistry::setValue (registryPath, getWindowsStartupCommand());
        if (! WindowsRegistry::valueExists (registryPath))
            return true;
        return WindowsRegistry::deleteValue (registryPath);
    }

    void minimisationStateChanged (bool isNowMinimised) override
"""
window = replace_once(window, marker, helpers, "startup helper insertion")

old_menu = """        m.addSeparator();
        m.addItem (4, TRANS("Reset to default state"));

        m.showMenuAsync"""
new_menu = """        m.addSeparator();
        m.addItem (4, TRANS("Reset to default state"));
#if JUCE_WINDOWS
        m.addSeparator();
        m.addItem (5, TRANS("Start with Windows (minimized to tray)"), true, isStartWithWindowsEnabled());
#endif

        m.showMenuAsync"""
window = replace_once(window, old_menu, new_menu, "options menu insertion")

old_switch = """            case 3:  pluginHolder->askUserToLoadState(); break;
            case 4:  resetToDefaultState(); break;
            default: break;
"""
new_switch = """            case 3:  pluginHolder->askUserToLoadState(); break;
            case 4:  resetToDefaultState(); break;
#if JUCE_WINDOWS
            case 5:
            {
                const bool shouldEnable = ! isStartWithWindowsEnabled();
                if (! setStartWithWindowsEnabled (shouldEnable))
                    AlertWindow::showMessageBoxAsync (AlertWindow::WarningIcon, TRANS("Startup Setting"), TRANS("SonoBus could not update the Windows startup setting."));
                break;
            }
#endif
            default: break;
"""
window = replace_once(window, old_switch, new_switch, "menu handler insertion")
window_path.write_text(window, encoding="utf-8", newline="\n")

app_path = Path("Source/SonoStandaloneFilterApp.cpp")
app = app_path.read_text(encoding="utf-8")

app = replace_once(app,
"""    bool doImmediateQuit = false;
    bool doHeadless = false;
    String loadSetupFilename;
""",
"""    bool doImmediateQuit = false;
    bool doHeadless = false;
#if JUCE_WINDOWS
    bool startMinimizedToTray = false;
#endif
    String loadSetupFilename;
""", "startup flag insertion")

app = replace_once(app,
"""        const String headlessSpec("-q|--headless");
        const String headlessSpecDesc("-q|--headless");

        const String loadSetupSpec("-l|--load-setup");
""",
"""        const String headlessSpec("-q|--headless");
        const String headlessSpecDesc("-q|--headless");
#if JUCE_WINDOWS
        const String startMinimizedSpec("--start-minimized");
#endif

        const String loadSetupSpec("-l|--load-setup");
""", "command spec insertion")

app = replace_once(app,
"""        app.addCommand ({ headlessSpec, headlessSpecDesc,
            TRANS("If specified, no GUI will be used and the application will be run headless."),
            TRANS("You'll need to use other command-line options to connect to a group... eventually there will be an OSC remote control interface."),
            nullptr
        });



        if (arglist.removeOptionIfFound(versionSpec))""",
"""        app.addCommand ({ headlessSpec, headlessSpecDesc,
            TRANS("If specified, no GUI will be used and the application will be run headless."),
            TRANS("You'll need to use other command-line options to connect to a group... eventually there will be an OSC remote control interface."),
            nullptr
        });
#if JUCE_WINDOWS
        app.addCommand ({ startMinimizedSpec, startMinimizedSpec,
            TRANS("Start SonoBus hidden in the Windows system tray."), {}, nullptr
        });
#endif

        if (arglist.removeOptionIfFound(versionSpec))""", "command registration insertion")

app = replace_once(app,
"""        auto setupfile = arglist.removeValueForOption(loadSetupSpec);
        if (setupfile.isNotEmpty()) {
            loadSetupFilename = setupfile;
        }


        if (arglist.removeOptionIfFound(headlessSpec)) {
""",
"""        auto setupfile = arglist.removeValueForOption(loadSetupSpec);
        if (setupfile.isNotEmpty()) {
            loadSetupFilename = setupfile;
        }
#if JUCE_WINDOWS
        if (arglist.removeOptionIfFound(startMinimizedSpec))
            startMinimizedToTray = true;
#endif

        if (arglist.removeOptionIfFound(headlessSpec)) {
""", "command parsing insertion")

app = replace_once(app,
"""            mainWindow->setVisible (true);

            Desktop::getInstance().setScreenSaverEnabled(false);""",
"""#if JUCE_WINDOWS
            if (startMinimizedToTray)
                mainWindow->setVisible (false);
            else
#endif
                mainWindow->setVisible (true);

            Desktop::getInstance().setScreenSaverEnabled(false);""", "startup visibility insertion")
app_path.write_text(app, encoding="utf-8", newline="\n")

changes_path = Path("FORK_CHANGES.md")
changes = changes_path.read_text(encoding="utf-8")
anchor = "- The tray functionality is compiled directly into `SonoBus.exe`; no companion helper process is required.\n\n"
section = anchor + """### Windows autostart minimized to tray

Added on **2026-08-17**.

- Adds a **Start with Windows (minimized to tray)** toggle to the standalone app's Options menu.
- Uses the current user's standard Windows startup registry entry (`HKEY_CURRENT_USER`), so enabling it does not require administrator privileges.
- The startup entry points to the exact `SonoBus.exe` being used and passes the internal `--start-minimized` option.
- At Windows sign-in, SonoBus initializes normally but keeps its main window hidden and remains available from the system tray.
- Disabling the toggle removes the startup entry.

"""
changes = replace_once(changes, anchor, section, "fork changes insertion")
changes_path.write_text(changes, encoding="utf-8", newline="\n")

readme_path = Path("README.md")
readme = readme_path.read_text(encoding="utf-8")
old_note = "> **Fork note:** The Windows minimize-to-tray implementation is built directly into the standalone SonoBus source. No helper executable or tray patch step is required when compiling this fork. The Windows GitHub Actions build provisions SonoBus's existing ASIO SDK dependency automatically."
new_note = "> **Fork note:** Native Windows minimize-to-tray support and optional **Start with Windows (minimized to tray)** support are built directly into the standalone SonoBus source. No helper executable or tray patch step is required when compiling this fork. The Windows GitHub Actions build provisions SonoBus's existing ASIO SDK dependency automatically."
readme = replace_once(readme, old_note, new_note, "README fork note update")
readme_path.write_text(readme, encoding="utf-8", newline="\n")

print("Applied Windows autostart minimized-to-tray support.")
