import threading
import time
import tkinter as tk
from tkinter import ttk
from typing import Callable

try:
    import pyautogui  # type: ignore
except ImportError as exc:
    raise SystemExit(
        "pyautogui is required. Install with: pip install -r requirements.txt"
    ) from exc

try:
    import keyboard  # type: ignore

    _HAS_KEYBOARD = True
except ImportError:
    keyboard = None  # type: ignore
    _HAS_KEYBOARD = False


class AutoClickerApp(tk.Tk):
    """
    A simple cross-platform autoclicker with a Tkinter GUI.
    Features:
    - Start/Stop buttons
    - Adjustable click speed via slider (clicks per second)
    - Clean shutdown on window close
    """

    def __init__(self) -> None:
        super().__init__()
        self.title("Autoclicker")
        self.resizable(False, False)

        # State
        self._click_thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._running = False
        self._global_hotkeys_registered = False

        # UI
        self._build_ui()
        # Keyboard shortcuts (in-app and optional global)
        self.bind_all("<Control-Alt-s>", lambda event: self.start_clicking())
        self.bind_all("<Control-Alt-d>", lambda event: self.stop_clicking())
        self._register_hotkeys()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # UI setup ------------------------------------------------------------
    def _build_ui(self) -> None:
        main = ttk.Frame(self, padding=16)
        main.grid(row=0, column=0, sticky="nsew")

        title = ttk.Label(main, text="AutoClicker", font=("Segoe UI", 14, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 12))

        # Speed slider (clicks per second)
        ttk.Label(main, text="Click speed (clicks/sec)").grid(
            row=1, column=0, sticky="w"
        )
        self.speed_var = tk.DoubleVar(value=5.0)
        self.speed_slider = ttk.Scale(
            main,
            from_=1,
            to=20,
            orient="horizontal",
            variable=self.speed_var,
            command=lambda _: self._update_speed_label(),
        )
        self.speed_slider.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(4, 0))
        self.speed_label = ttk.Label(main, text="5.0 cps (~0.20s interval)")
        self.speed_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(2, 12))

        # Buttons
        self.start_btn = ttk.Button(main, text="Start", command=self.start_clicking)
        self.stop_btn = ttk.Button(
            main, text="Stop", command=self.stop_clicking, state=tk.DISABLED
        )
        self.start_btn.grid(row=4, column=0, padx=(0, 8))
        self.stop_btn.grid(row=4, column=1, padx=(8, 0))

        # Status
        self.status_var = tk.StringVar(value="Idle")
        status = ttk.Label(main, textvariable=self.status_var, foreground="#555")
        status.grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0))

        self.columnconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)

    # Helpers --------------------------------------------------------------
    def _current_interval(self) -> float:
        cps = max(self.speed_var.get(), 0.1)
        return max(0.01, 1.0 / cps)

    def _update_speed_label(self) -> None:
        interval = self._current_interval()
        cps = self.speed_var.get()
        self.speed_label.config(text=f"{cps:.1f} cps (~{interval:.2f}s interval)")

    def _register_hotkeys(self) -> None:
        """Register global hotkeys when the optional keyboard module is present."""
        if not _HAS_KEYBOARD or self._global_hotkeys_registered:
            if not _HAS_KEYBOARD:
                print("Global hotkeys unavailable: install the 'keyboard' package")
            return

        def _safe(fn: Callable[[], None]) -> Callable[[], None]:
            # Ensure callbacks hop back onto the Tk event loop to avoid thread issues
            return lambda: self._run_on_ui_thread(fn)

        keyboard.add_hotkey("ctrl+alt+s", _safe(self.start_clicking))
        keyboard.add_hotkey("ctrl+alt+d", _safe(self.stop_clicking))
        self._global_hotkeys_registered = True

    def _unregister_hotkeys(self) -> None:
        if _HAS_KEYBOARD and self._global_hotkeys_registered:
            keyboard.remove_hotkey("ctrl+alt+s")
            keyboard.remove_hotkey("ctrl+alt+d")
            self._global_hotkeys_registered = False

    def _run_on_ui_thread(self, fn: Callable[[], None]) -> None:
        if not self.winfo_exists():
            return
        self.after(0, fn)

    # Actions --------------------------------------------------------------
    def start_clicking(self) -> None:
        if self._running:
            return

        interval = self._current_interval()
        self._stop_event.clear()
        self._click_thread = threading.Thread(
            target=self._click_loop, args=(interval,), daemon=True
        )
        self._running = True
        self._click_thread.start()

        self.start_btn.state(["disabled"])
        self.stop_btn.state(["!disabled"])
        self.status_var.set("Running… (move mouse to target position)")

    def stop_clicking(self) -> None:
        if not self._running:
            return
        self._stop_event.set()
        self._running = False
        self.start_btn.state(["!disabled"])
        self.stop_btn.state(["disabled"])
        self.status_var.set("Stopped")

    def _click_loop(self, interval: float) -> None:
        # Allow slight delay before starting to avoid clicking the Start button
        time.sleep(0.3)
        while not self._stop_event.is_set():
            try:
                pyautogui.click()
            except Exception as exc:  # broad to ensure thread does not die silently
                self.status_var.set(f"Click error: {exc}")
                break
            time.sleep(interval)
        self.status_var.set("Idle")

    def _on_close(self) -> None:
        self._stop_event.set()
        self._unregister_hotkeys()
        self.destroy()


def main() -> None:
    # Recommended to disable PyAutoGUI failsafe only if necessary
    pyautogui.FAILSAFE = True
    app = AutoClickerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
