import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import threading

class LogViewer:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LogViewer, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.root = None
        self.text_area = None
        self.is_visible = False
        self._create_window()
    
    def _create_window(self):
        self.root = tk.Tk()
        self.root.title("Log Viewer")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")
        self.root.protocol("WM_DELETE_WINDOW", self.hide)

        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Scrolled text area for logs
        self.text_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            height=20,
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#333333",
            state='disabled'
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))

        # Clear button
        clear_button = ttk.Button(
            button_frame,
            text="Clear Logs",
            command=self.clear_logs
        )
        clear_button.pack(side=tk.RIGHT)

        self.root.withdraw()  # Hide window initially

    def _ensure_thread_safe(self, func):
        def wrapper(*args, **kwargs):
            if self.root is None:
                return
            if threading.current_thread() is threading.main_thread():
                func(*args, **kwargs)
            else:
                self.root.after(0, func, *args, **kwargs)
        return wrapper

    def show(self):
        @self._ensure_thread_safe
        def _show():
            if not self.is_visible:
                self.root.deiconify()
                self.is_visible = True
        _show()

    def hide(self):
        @self._ensure_thread_safe
        def _hide():
            if self.is_visible:
                self.root.withdraw()
                self.is_visible = False
        _hide()

    def log(self, message, level="INFO"):
        @self._ensure_thread_safe
        def _log():
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] {level}: {message}\n"
            self.text_area.configure(state='normal')
            self.text_area.insert(tk.END, log_message)
            self.text_area.see(tk.END)
            self.text_area.configure(state='disabled')
        _log()

    def clear_logs(self):
        @self._ensure_thread_safe
        def _clear():
            self.text_area.configure(state='normal')
            self.text_area.delete(1.0, tk.END)
            self.text_area.configure(state='disabled')
        _clear()

    def destroy(self):
        @self._ensure_thread_safe
        def _destroy():
            if self.root:
                self.root.destroy()
                self.root = None
                self.text_area = None
                self.is_visible = False
                LogViewer._instance = None
        _destroy()

# Exported functions
def show_log_viewer():
    print('Atharva')
    viewer = LogViewer()
    viewer.show()

def hide_log_viewer():
    viewer = LogViewer()
    viewer.hide()

def log_message(message, level="INFO"):
    viewer = LogViewer()
    viewer.log(message, level)

def clear_log_viewer():
    viewer = LogViewer()
    viewer.clear_logs()

def destroy_log_viewer():
    viewer = LogViewer()
    viewer.destroy()
