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

## Notes

- PyAutoGUI failsafe is enabled; slam mouse to the upper-left corner to abort.
- Extremely high click rates may be limited by the OS and hardware timing.
