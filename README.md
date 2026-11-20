# Multi Commander Presets by JNL Software

[Instrukcja po polsku](README.pl.md)

Two optional presets for the Multi Commander file manager:

- **Soft Gray** uses a light gray palette with a blue spacebar-marked selection for files and folders.
- **F1 Rename** binds F1 to Rename in Explorer panels.

## Preview and apply

Use Python 3.10 or newer and close Multi Commander before applying a preset. The default configuration directory is `%APPDATA%\MultiCommander\Config`. For portable installations, pass `--config-dir "D:\MultiCommander\Config"` to point to your actual directory.

```powershell
python apply_preset.py soft-gray
python apply_preset.py soft-gray --apply
python apply_preset.py f1-rename
python apply_preset.py f1-rename --apply
```

Without `--apply`, the script only displays changes. Applying a preset creates a timestamped `.bak` of an existing XML file. The theme merges known color fields in `ExplorerPanel.xml`. The shortcut changes only the unmodified F1 binding for the Explorer extension in `CustomKeymappings.xml`. To restore an existing configuration, close Multi Commander and copy the backup over the modified XML file. If the shortcut preset created a new file, remove that new file to undo it before making other shortcut changes.

The source palette came from configuration build 3238. Multi Commander is available from its [official website](https://multicommander.com/). Presets maintained by [JNL Software](https://www.jnlsoftware.pl/).
