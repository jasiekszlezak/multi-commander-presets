# Presety do Multi Commandera od JNL Software

[Wersja angielska](README.md)

- **Soft Gray** ustawia jasnoszary motyw oraz niebieskie oznaczenie plików i folderów zaznaczonych spacją.
- **F1 Rename** przypisuje F1 do zmiany nazwy w panelach plików.

## Podgląd i zastosowanie

Wymagany Python 3.10 lub nowszy. Przed zapisaniem zmian zamknij Multi Commandera. Domyślny katalog to `%APPDATA%\MultiCommander\Config`. W instalacji przenośnej wskaż właściwy katalog za pomocą `--config-dir "D:\MultiCommander\Config"`.

```powershell
python apply_preset.py soft-gray
python apply_preset.py soft-gray --apply
python apply_preset.py f1-rename
python apply_preset.py f1-rename --apply
```

Polecenie bez `--apply` pokazuje podgląd zmian. Przy zapisie skrypt tworzy kopię istniejącego pliku XML z datą i rozszerzeniem `.bak`. Motyw nakłada wybrane pola w sekcji kolorów. Skrót zmienia wyłącznie powiązanie F1 bez modyfikatorów dla panelu plików. Aby cofnąć zmianę, zamknij program i zastąp XML jego kopią. Jeśli preset F1 utworzył nowy plik, możesz go usunąć przed wprowadzeniem innych własnych skrótów.

Paleta została zaczerpnięta z konfiguracji kompilacji 3238.
