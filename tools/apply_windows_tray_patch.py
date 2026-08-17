from pathlib import Path

SOURCE = Path("Source/SonoStandaloneFilterWindow.h")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


text = SOURCE.read_text(encoding="utf-8")

if "class SonoBusSystemTrayIcon final" in text:
    print("Windows tray patch is already applied.")
    raise SystemExit(0)

text = replace_once(
    text,
    '#include <algorithm>\n\nnamespace juce\n{',
    '''#include <algorithm>\n#include <functional>\n\nnamespace juce\n{\n\n#if JUCE_WINDOWS\nclass SonoBusSystemTrayIcon final : public SystemTrayIconComponent\n{\npublic:\n    SonoBusSystemTrayIcon()\n    {\n        Image icon (Image::ARGB, 32, 32, true);\n        Graphics g (icon);\n        g.setColour (Colour (0xff188fbe));\n        g.fillEllipse (2.0f, 2.0f, 28.0f, 28.0f);\n        g.setColour (Colours::white);\n        g.setFont (Font (20.0f, Font::bold));\n        g.drawText ("S", icon.getBounds(), Justification::centred, false);\n\n        setIconImage (icon, icon);\n        setIconTooltip ("SonoBus");\n    }\n\n    std::function<void()> restoreRequested;\n    std::function<void()> quitRequested;\n\n    void mouseDown (const MouseEvent& event) override\n    {\n        if (! event.mods.isPopupMenu())\n        {\n            if (restoreRequested)\n                restoreRequested();\n\n            return;\n        }\n\n        PopupMenu menu;\n        menu.addItem (1, TRANS("Open SonoBus"));\n        menu.addSeparator();\n        menu.addItem (2, TRANS("Exit SonoBus"));\n        menu.showMenuAsync (PopupMenu::Options(),\n                            ModalCallbackFunction::forComponent (menuCallback, this));\n    }\n\nprivate:\n    static void menuCallback (int result, SonoBusSystemTrayIcon* tray)\n    {\n        if (tray == nullptr)\n            return;\n\n        if (result == 1 && tray->restoreRequested)\n            tray->restoreRequested();\n        else if (result == 2 && tray->quitRequested)\n            tray->quitRequested();\n    }\n};\n#endif''',
    "tray helper insertion",
)

text = replace_once(
    text,
    '        setUsingNativeTitleBar(true);\n        #endif',
    '''        setUsingNativeTitleBar(true);\n\n       #if JUCE_WINDOWS\n        systemTrayIcon = std::make_unique<SonoBusSystemTrayIcon>();\n        systemTrayIcon->restoreRequested = [this]() { restoreFromSystemTray(); };\n        systemTrayIcon->quitRequested = []()\n        {\n            if (auto* app = JUCEApplicationBase::getInstance())\n                app->systemRequestedQuit();\n        };\n       #endif\n        #endif''',
    "tray construction insertion",
)

close_block = '''    void closeButtonPressed() override\n    {\n        pluginHolder->savePluginState();\n\n        JUCEApplicationBase::getInstance()->systemRequestedQuit();\n    }'''

close_replacement = close_block + '''\n\n#if JUCE_WINDOWS\n    void minimisationStateChanged (bool isNowMinimised) override\n    {\n        if (! isNowMinimised || hideToTrayPending)\n            return;\n\n        // The Windows minimise notification arrives while the native window is\n        // still completing its minimise transition. Hiding synchronously here\n        // races that transition and can leave a stale taskbar button or a window\n        // that refuses to minimise a second time. Queue the hide until the native\n        // minimise operation has completely returned.\n        hideToTrayPending = true;\n        Component::SafePointer<StandaloneFilterWindow> safeThis (this);\n\n        MessageManager::callAsync ([safeThis]() mutable\n        {\n            if (safeThis == nullptr)\n                return;\n\n            safeThis->hideToTrayPending = false;\n\n            if (safeThis->isMinimised())\n                safeThis->setVisible (false);\n        });\n    }\n\n    void restoreFromSystemTray()\n    {\n        hideToTrayPending = false;\n\n        // Restore the native window while it is still hidden, then show it.\n        // This avoids briefly re-creating a minimised taskbar button.\n        if (isMinimised())\n            setMinimised (false);\n\n        setVisible (true);\n        toFront (true);\n    }\n#endif'''

text = replace_once(
    text,
    close_block,
    close_replacement,
    "minimise/restore handler insertion",
)

text = replace_once(
    text,
    '    std::unique_ptr<StandalonePluginHolder> pluginHolder;\n',
    '''    std::unique_ptr<StandalonePluginHolder> pluginHolder;\n#if JUCE_WINDOWS\n    std::unique_ptr<SonoBusSystemTrayIcon> systemTrayIcon;\n    bool hideToTrayPending = false;\n#endif\n''',
    "tray member insertion",
)

SOURCE.write_text(text, encoding="utf-8", newline="\n")
print("Applied native Windows system-tray support to SonoBus.")
