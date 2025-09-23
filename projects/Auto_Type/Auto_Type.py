import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
import pyautogui
from pynput import keyboard

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

class AutoTyperApp:
    def __init__(self, root):
        self.root = root
        root.title("AutoTyper")
        root.geometry("580x460")
        root.resizable(False, False)

        # State
        self.wpm_var = tk.StringVar(value="60")
        self.start_hotkey_var = tk.StringVar(value="ctrl+alt+s")
        self.stop_hotkey_var = tk.StringVar(value="ctrl+alt+e")
        self.delay_var = tk.IntVar(value=3)
        self.always_on_top_var = tk.BooleanVar(value=True)
        self.hotkeys_obj = None
        self.running = False
        self.typing_thread = None

        self._build_ui()
        self.root.attributes("-topmost", True)
        self._periodic_update()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        tk.Label(self.root, text="Paste text to type:", anchor="w").place(x=10, y=10)
        self.text_box = tk.Text(self.root, wrap="word", height=10, width=68)
        self.text_box.place(x=10, y=32)

        # WPM combobox
        tk.Label(self.root, text="Typing speed (WPM):").place(x=10, y=250)
        wpm_values = [str(i) for i in range(20, 151)]
        self.wpm_combo = ttk.Combobox(self.root, values=wpm_values, textvariable=self.wpm_var, width=8, state="readonly")
        self.wpm_combo.place(x=130, y=250)
        self.wpm_combo.set(self.wpm_var.get())

        # Start delay
        tk.Label(self.root, text="Start delay (seconds):").place(x=10, y=280)
        self.delay_spin = tk.Spinbox(self.root, from_=0, to=10, textvariable=self.delay_var, width=5)
        self.delay_spin.place(x=160, y=280)

        # Always on top
        self.top_check = ttk.Checkbutton(self.root, text="Always on top", variable=self.always_on_top_var, command=self._toggle_topmost)
        self.top_check.place(x=240, y=278)

        # Hotkeys
        tk.Label(self.root, text="Start Hotkey:").place(x=10, y=320)
        self.start_entry = ttk.Entry(self.root, textvariable=self.start_hotkey_var, width=22)
        self.start_entry.place(x=120, y=320)

        tk.Label(self.root, text="Stop Hotkey:").place(x=10, y=350)
        self.stop_entry = ttk.Entry(self.root, textvariable=self.stop_hotkey_var, width=22)
        self.stop_entry.place(x=120, y=350)

        # Control buttons
        self.activate_btn = ttk.Button(self.root, text="Activate Hotkeys", command=self.activate_hotkeys)
        self.activate_btn.place(x=10, y=390, width=160)

        self.deactivate_btn = ttk.Button(self.root, text="Deactivate Hotkeys", command=self.deactivate_hotkeys, state="disabled")
        self.deactivate_btn.place(x=180, y=390, width=160)

        self.start_btn = ttk.Button(self.root, text="▶ Start Typing", command=lambda: self._start_typing_thread())
        self.start_btn.place(x=350, y=390, width=100)

        self.stop_btn = ttk.Button(self.root, text="■ Stop Typing", command=lambda: self._stop_typing())
        self.stop_btn.place(x=460, y=390, width=100)

        # Status bar
        self.status_var = tk.StringVar(value="Hotkeys: Inactive  |  Typing: Stopped")
        self.status_label = tk.Label(self.root, textvariable=self.status_var, anchor="w", relief="sunken")
        self.status_label.place(x=10, y=430, width=560, height=20)

    def _toggle_topmost(self):
        self.root.attributes("-topmost", bool(self.always_on_top_var.get()))

    def _convert_to_gh_format(self, combo_str: str):
        if not combo_str:
            return None
        parts = [p.strip().lower() for p in combo_str.split("+") if p.strip()]
        if not parts:
            return None
        modifier_map = {"ctrl": "<ctrl>", "alt": "<alt>", "shift": "<shift>", "cmd": "<cmd>", "win": "<cmd>", "super": "<cmd>", "option": "<alt>"}
        if len(parts) == 1:
            return parts[0]
        *mods, last = parts
        converted = []
        for m in mods:
            if m in modifier_map:
                converted.append(modifier_map[m])
            else:
                return None
        last_map = {"space": "space", "enter": "enter", "tab": "tab", "esc": "esc"}
        last_key = last_map.get(last, last)
        converted.append(last_key)
        return "+".join(converted)

    def activate_hotkeys(self):
        if self.hotkeys_obj:
            self.hotkeys_obj.stop()
            self.hotkeys_obj = None
        start_key = self._convert_to_gh_format(self.start_hotkey_var.get())
        stop_key  = self._convert_to_gh_format(self.stop_hotkey_var.get())
        if not start_key or not stop_key:
            messagebox.showerror("Hotkey error", "Invalid hotkey format")
            return
        mapping = {}
        if start_key == stop_key:
            mapping[start_key] = self._on_toggle_hotkey
        else:
            mapping[start_key] = self._on_start_hotkey
            mapping[stop_key] = self._on_stop_hotkey
        self.hotkeys_obj = keyboard.GlobalHotKeys(mapping)
        self.hotkeys_obj.start()
        self.activate_btn.config(state="disabled")
        self.deactivate_btn.config(state="normal")
        self.status_var.set("Hotkeys: Active  |  Typing: Stopped")

    def deactivate_hotkeys(self):
        if self.hotkeys_obj:
            self.hotkeys_obj.stop()
            self.hotkeys_obj = None
        self.activate_btn.config(state="normal")
        self.deactivate_btn.config(state="disabled")
        self.status_var.set("Hotkeys: Inactive  |  Typing: Stopped")

    def _on_start_hotkey(self):
        if not self.running:
            self.root.after(0, lambda: self._start_typing_thread())
    def _on_stop_hotkey(self):
        self._stop_typing()
    def _on_toggle_hotkey(self):
        if self.running:
            self._stop_typing()
        else:
            self._start_typing_thread()

    def _start_typing_thread(self):
        if self.running:
            return
        try:
            wpm = int(self.wpm_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid WPM")
            return
        delay = self.delay_var.get()
        self.running = True
        self.status_var.set("Preparing to type...")
        t = threading.Thread(target=self._type_text_worker, args=(wpm, delay), daemon=True)
        self.typing_thread = t
        t.start()

    def _stop_typing(self):
        self.running = False
        self.status_var.set("Hotkeys: Active  |  Typing: Stopped")

    def _type_text_worker(self, wpm, delay):
        text = self.text_box.get("1.0", "end-1c")
        if not text.strip():
            self.running = False
            self.status_var.set("Hotkeys: Active  |  Typing: Stopped")
            return
        # Wait delay before typing
        for i in range(delay, 0, -1):
            if not self.running:
                return
            self.status_var.set(f"Starting in {i}...")
            time.sleep(1)
        self.status_var.set("Typing...")
        cps = (wpm * 5) / 60.0
        base_delay = 1.0 / max(cps, 1e-6)
        for ch in text:
            if not self.running:
                break
            if ch == "\n":
                pyautogui.press("enter")
                time.sleep(base_delay * 1.2)
                continue
            if random.random() < 0.05 and ch.strip():
                wrong = random.choice("abcdefghijklmnopqrstuvwxyz")
                pyautogui.typewrite(wrong, interval=base_delay*0.5)
                pyautogui.press("backspace")
                time.sleep(base_delay*0.5)
            pyautogui.typewrite(ch, interval=base_delay*random.uniform(0.9,1.2))
        self.running = False
        self.status_var.set("Hotkeys: Active  |  Typing: Stopped")

    def _periodic_update(self):
        hk_status = "Active" if self.hotkeys_obj else "Inactive"
        typing_status = "Running" if self.running else "Stopped"
        self.status_var.set(f"Hotkeys: {hk_status}  |  Typing: {typing_status}")
        self.root.after(250, self._periodic_update)

    def _on_close(self):
        if self.hotkeys_obj:
            self.hotkeys_obj.stop()
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()
