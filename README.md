# AutoClicker

A simple cross-platform desktop autoclicker with a Tkinter UI. Adjust click speed, start, and stop from the window. Works on Windows, macOS, and Linux (with GUI support).

## Requirements

- Python 3.8+
- Display/GUI session (X11/Wayland on Linux)

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

Use the slider to set clicks per second, then press **Start**. Move your cursor to the target area; press **Stop** to halt.

### Keyboard shortcuts

- **Ctrl + Alt + S** — start clicking
- **Ctrl + Alt + D** — stop clicking

Shortcuts are bound to the app window; ensure it has focus when triggering them.

## Build a standalone executable

Install PyInstaller if you don't have it:

```powershell
python -m pip install pyinstaller
```

Build (Windows example):

```powershell
python -m PyInstaller --onefile --windowed main.py
```
 
- The executable will appear in the `dist` folder.
- On macOS/Linux use the same command from a terminal; ensure necessary permissions to run GUI apps.

### Portable build (no installer)

The `--onefile` flag already produces a portable executable. After building, you can zip the `dist` output and run it on another machine with a compatible OS/architecture:

```powershell
# build portable exe
python -m PyInstaller --onefile --windowed main.py

# optional: zip the portable exe
Compress-Archive -Path dist\main.exe -DestinationPath dist\AutoClicker-portable.zip -Force
```

On macOS/Linux, the same `--onefile --windowed` build works; ensure the target machine allows GUI apps to run.

## Notes

- PyAutoGUI failsafe is enabled; slam mouse to the upper-left corner to abort.
- Extremely high click rates may be limited by the OS and hardware timing.
