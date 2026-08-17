from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


# -----------------------------------------------------------------------------
# Move the Windows startup control into SonoBus's real in-app OPTIONS tab.
# -----------------------------------------------------------------------------
h_path = Path("Source/OptionsView.h")
h = h_path.read_text(encoding="utf-8")

h = replace_once(
    h,
    "    std::unique_ptr<ToggleButton> mOptionsAutoReconnectButton;\n    std::unique_ptr<ToggleButton> mOptionsSliderSnapToMouseButton;\n",
    "    std::unique_ptr<ToggleButton> mOptionsAutoReconnectButton;\n#if JUCE_WINDOWS\n    std::unique_ptr<ToggleButton> mOptionsStartWithWindowsButton;\n#endif\n    std::unique_ptr<ToggleButton> mOptionsSliderSnapToMouseButton;\n",
    "OptionsView toggle member",
)

h = replace_once(
    h,
    "    FlexBox optionsAutoReconnectBox;\n    FlexBox optionsSnapToMouseBox;\n",
    "    FlexBox optionsAutoReconnectBox;\n#if JUCE_WINDOWS\n    FlexBox optionsStartWithWindowsBox;\n#endif\n    FlexBox optionsSnapToMouseBox;\n",
    "OptionsView flexbox member",
)

h_path.write_text(h, encoding="utf-8", newline="\n")


cpp_path = Path("Source/OptionsView.cpp")
cpp = cpp_path.read_text(encoding="utf-8")

cpp = replace_once(
    cpp,
    "enum {\n    nameTextColourId = 0x1002830,\n    selectedColourId = 0x1002840,\n    separatorColourId = 0x1002850,\n};\n\n\nvoid OptionsView::initializeLanguages()\n",
    '''enum {
    nameTextColourId = 0x1002830,
    selectedColourId = 0x1002840,
    separatorColourId = 0x1002850,
};

#if JUCE_WINDOWS
namespace
{
String getSonoBusWindowsStartupRegistryPath()
{
    return "HKEY_CURRENT_USER\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run\\\\SonoBus";
}

String getSonoBusWindowsStartupCommand()
{
    const auto executablePath = File::getSpecialLocation (File::currentExecutableFile).getFullPathName();
    return "\\\"" + executablePath + "\\\" --start-minimized";
}

bool isSonoBusWindowsStartupEnabled()
{
    return WindowsRegistry::getValue (getSonoBusWindowsStartupRegistryPath()).trim()
           == getSonoBusWindowsStartupCommand();
}

bool setSonoBusWindowsStartupEnabled (bool shouldEnable)
{
    const auto registryPath = getSonoBusWindowsStartupRegistryPath();

    if (shouldEnable)
        return WindowsRegistry::setValue (registryPath, getSonoBusWindowsStartupCommand());

    if (! WindowsRegistry::valueExists (registryPath))
        return true;

    return WindowsRegistry::deleteValue (registryPath);
}
}
#endif


void OptionsView::initializeLanguages()
''',
    "Windows startup helpers",
)

cpp = replace_once(
    cpp,
    '''    mOptionsAutoReconnectButton = std::make_unique<ToggleButton>(TRANS("Auto-Reconnect to Last Group"));
    mAutoReconnectAttachment = std::make_unique<AudioProcessorValueTreeState::ButtonAttachment> (processor.getValueTreeState(), SonobusAudioProcessor::paramAutoReconnectLast, *mOptionsAutoReconnectButton);

    mOptionsOverrideSamplerateButton = std::make_unique<ToggleButton>(TRANS("Override Device Sample Rate"));
''',
    '''    mOptionsAutoReconnectButton = std::make_unique<ToggleButton>(TRANS("Auto-Reconnect to Last Group"));
    mAutoReconnectAttachment = std::make_unique<AudioProcessorValueTreeState::ButtonAttachment> (processor.getValueTreeState(), SonobusAudioProcessor::paramAutoReconnectLast, *mOptionsAutoReconnectButton);

#if JUCE_WINDOWS
    mOptionsStartWithWindowsButton = std::make_unique<ToggleButton>(TRANS("Start with Windows (minimized to tray)"));
    mOptionsStartWithWindowsButton->setTooltip(TRANS("Automatically launch SonoBus when you sign in to Windows and keep it hidden in the system tray."));
    mOptionsStartWithWindowsButton->setToggleState(isSonoBusWindowsStartupEnabled(), dontSendNotification);
    mOptionsStartWithWindowsButton->addListener(this);
#endif

    mOptionsOverrideSamplerateButton = std::make_unique<ToggleButton>(TRANS("Override Device Sample Rate"));
''',
    "Windows startup toggle construction",
)

cpp = replace_once(
    cpp,
    '''    if (JUCEApplicationBase::isStandaloneApp()) {
        mOptionsComponent->addAndMakeVisible(mOptionsOverrideSamplerateButton.get());
        mOptionsComponent->addAndMakeVisible(mOptionsShouldCheckForUpdateButton.get());
        if (mOptionsAllowBluetoothInput) {
''',
    '''    if (JUCEApplicationBase::isStandaloneApp()) {
        mOptionsComponent->addAndMakeVisible(mOptionsOverrideSamplerateButton.get());
        mOptionsComponent->addAndMakeVisible(mOptionsShouldCheckForUpdateButton.get());
#if JUCE_WINDOWS
        mOptionsComponent->addAndMakeVisible(mOptionsStartWithWindowsButton.get());
#endif
        if (mOptionsAllowBluetoothInput) {
''',
    "Windows startup toggle visibility",
)

cpp = replace_once(
    cpp,
    '''        if (getShouldCheckForNewVersionValue) {
            Value * val = getShouldCheckForNewVersionValue();
            mOptionsShouldCheckForUpdateButton->setToggleState((bool)val->getValue(), dontSendNotification);
        }

        if (getAllowBluetoothInputValue && mOptionsAllowBluetoothInput) {
''',
    '''        if (getShouldCheckForNewVersionValue) {
            Value * val = getShouldCheckForNewVersionValue();
            mOptionsShouldCheckForUpdateButton->setToggleState((bool)val->getValue(), dontSendNotification);
        }
#if JUCE_WINDOWS
        if (mOptionsStartWithWindowsButton)
            mOptionsStartWithWindowsButton->setToggleState(isSonoBusWindowsStartupEnabled(), dontSendNotification);
#endif

        if (getAllowBluetoothInputValue && mOptionsAllowBluetoothInput) {
''',
    "Windows startup toggle state refresh",
)

cpp = replace_once(
    cpp,
    '''    optionsAutoReconnectBox.items.clear();
    optionsAutoReconnectBox.flexDirection = FlexBox::Direction::row;
    optionsAutoReconnectBox.items.add(FlexItem(10, 12).withFlex(0));
    optionsAutoReconnectBox.items.add(FlexItem(180, minpassheight, *mOptionsAutoReconnectButton).withMargin(0).withFlex(1));

    optionsOverrideSamplerateBox.items.clear();
''',
    '''    optionsAutoReconnectBox.items.clear();
    optionsAutoReconnectBox.flexDirection = FlexBox::Direction::row;
    optionsAutoReconnectBox.items.add(FlexItem(10, 12).withFlex(0));
    optionsAutoReconnectBox.items.add(FlexItem(180, minpassheight, *mOptionsAutoReconnectButton).withMargin(0).withFlex(1));

#if JUCE_WINDOWS
    optionsStartWithWindowsBox.items.clear();
    optionsStartWithWindowsBox.flexDirection = FlexBox::Direction::row;
    optionsStartWithWindowsBox.items.add(FlexItem(10, 12).withFlex(0));
    optionsStartWithWindowsBox.items.add(FlexItem(180, minpassheight, *mOptionsStartWithWindowsButton).withMargin(0).withFlex(1));
#endif

    optionsOverrideSamplerateBox.items.clear();
''',
    "Windows startup flexbox layout",
)

cpp = replace_once(
    cpp,
    '''    optionsBox.items.add(FlexItem(100, minpassheight, optionsSnapToMouseBox).withMargin(2).withFlex(0));
    optionsBox.items.add(FlexItem(100, minpassheight, optionsAutoReconnectBox).withMargin(2).withFlex(0));
    optionsBox.items.add(FlexItem(100, minitemheight, optionsUdpBox).withMargin(2).withFlex(0));
    if (JUCEApplicationBase::isStandaloneApp()) {
''',
    '''    optionsBox.items.add(FlexItem(100, minpassheight, optionsSnapToMouseBox).withMargin(2).withFlex(0));
    optionsBox.items.add(FlexItem(100, minpassheight, optionsAutoReconnectBox).withMargin(2).withFlex(0));
#if JUCE_WINDOWS
    if (JUCEApplicationBase::isStandaloneApp())
        optionsBox.items.add(FlexItem(100, minpassheight, optionsStartWithWindowsBox).withMargin(2).withFlex(0));
#endif
    optionsBox.items.add(FlexItem(100, minitemheight, optionsUdpBox).withMargin(2).withFlex(0));
    if (JUCEApplicationBase::isStandaloneApp()) {
''',
    "Windows startup row placement",
)

cpp = replace_once(
    cpp,
    '''    else if (buttonThatWasClicked == mOptionsSliderSnapToMouseButton.get()) {
        bool newval = mOptionsSliderSnapToMouseButton->getToggleState();
''',
    '''#if JUCE_WINDOWS
    else if (buttonThatWasClicked == mOptionsStartWithWindowsButton.get()) {
        if (JUCEApplicationBase::isStandaloneApp()) {
            const bool shouldEnable = mOptionsStartWithWindowsButton->getToggleState();
            if (! setSonoBusWindowsStartupEnabled (shouldEnable)) {
                mOptionsStartWithWindowsButton->setToggleState(!shouldEnable, dontSendNotification);
                AlertWindow::showMessageBoxAsync(AlertWindow::WarningIcon,
                                                 TRANS("Startup Setting"),
                                                 TRANS("SonoBus could not update the Windows startup setting."));
            }
        }
    }
#endif
    else if (buttonThatWasClicked == mOptionsSliderSnapToMouseButton.get()) {
        bool newval = mOptionsSliderSnapToMouseButton->getToggleState();
''',
    "Windows startup button handler",
)

cpp_path.write_text(cpp, encoding="utf-8", newline="\n")


# -----------------------------------------------------------------------------
# Remove the duplicate startup control from JUCE's host popup. The native
# tray/minimise implementation itself remains untouched.
# -----------------------------------------------------------------------------
window_path = Path("Source/SonoStandaloneFilterWindow.h")
window = window_path.read_text(encoding="utf-8")

window = replace_once(
    window,
    '''#if JUCE_WINDOWS
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
''',
    '''#if JUCE_WINDOWS
    void minimisationStateChanged (bool isNowMinimised) override
''',
    "remove host startup helpers",
)

window = replace_once(
    window,
    '''        m.addItem (4, TRANS("Reset to default state"));
#if JUCE_WINDOWS
        m.addSeparator();
        m.addItem (5, TRANS("Start with Windows (minimized to tray)"), true, isStartWithWindowsEnabled());
#endif

        m.showMenuAsync''',
    '''        m.addItem (4, TRANS("Reset to default state"));

        m.showMenuAsync''',
    "remove host startup menu item",
)

window = replace_once(
    window,
    '''            case 4:  resetToDefaultState(); break;
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
''',
    '''            case 4:  resetToDefaultState(); break;
            default: break;
''',
    "remove host startup menu handler",
)

window_path.write_text(window, encoding="utf-8", newline="\n")


# -----------------------------------------------------------------------------
# Clarify fork-facing documentation.
# -----------------------------------------------------------------------------
readme_path = Path("README.md")
readme = readme_path.read_text(encoding="utf-8")
readme = replace_once(
    readme,
    "Unofficial SonoBus fork featuring native Windows minimize-to-tray integration.\n",
    "Unofficial SonoBus fork featuring native Windows minimize-to-tray integration and optional autostart-to-tray support.\n",
    "README summary",
)
readme_path.write_text(readme, encoding="utf-8", newline="\n")

changes_path = Path("FORK_CHANGES.md")
changes = changes_path.read_text(encoding="utf-8")
changes = replace_once(
    changes,
    "- Adds a **Start with Windows (minimized to tray)** toggle to the standalone app's Options menu.\n",
    "- Adds a **Start with Windows (minimized to tray)** toggle directly to SonoBus's in-app **OPTIONS** tab.\n",
    "fork changes UI clarification",
)
changes_path.write_text(changes, encoding="utf-8", newline="\n")

print("Moved the Windows autostart toggle into the real SonoBus OPTIONS tab.")
