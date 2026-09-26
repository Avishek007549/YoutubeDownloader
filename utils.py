import tkinter as tk
import threading
from tkinter import filedialog, ttk

from config import APP_TITLE, DEFAULT_OUTPUT_DIR, QUALITY_CHOICES
from downloader import download_from_input


class DownloadApp:
    """Small Tkinter interface for downloading YouTube videos or audio."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("720x420")
        self.root.minsize(620, 340)
        self.setup_ui()

    def setup_ui(self):
        main = ttk.Frame(self.root, padding=18)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="YouTube URL", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(8, 4))
        self.url_var = tk.StringVar()
        ttk.Entry(main, textvariable=self.url_var, width=80).pack(fill="x", pady=(0, 10))

        toolbar = ttk.Frame(main)
        toolbar.pack(fill="x", pady=(0, 12))
        ttk.Label(toolbar, text="Save to:").pack(side="left")
        self.output_dir = tk.StringVar(value=DEFAULT_OUTPUT_DIR)
        ttk.Entry(toolbar, textvariable=self.output_dir, width=38).pack(side="left", padx=8)
        ttk.Button(toolbar, text="Browse", command=self.choose_directory).pack(side="left")

        options = ttk.Frame(main)
        options.pack(fill="x", pady=(0, 12))
        ttk.Label(options, text="Quality:").pack(side="left")
        self.quality_var = tk.StringVar(value=QUALITY_CHOICES[0])
        ttk.Combobox(options, textvariable=self.quality_var, values=QUALITY_CHOICES, state="readonly", width=12).pack(side="left", padx=(8, 16))
        self.audio_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options, text="Audio only", variable=self.audio_var).pack(side="left")

        self.download_btn = ttk.Button(main, text="Download", command=self.start_download)
        self.download_btn.pack(anchor="w", pady=(0, 12))
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main, textvariable=self.status_var, foreground="#1f5f8c", wraplength=640).pack(anchor="w")
        self.progress = ttk.Progressbar(main, mode="determinate", length=640)
        self.progress.pack(fill="x", pady=(12, 0))

    def choose_directory(self):
        directory = filedialog.askdirectory(initialdir=self.output_dir.get() or DEFAULT_OUTPUT_DIR)
        if directory:
            self.output_dir.set(directory)

    def start_download(self):
        url = self.url_var.get().strip()
        if not url:
            self.set_status("Please enter a YouTube URL.")
            return
        self.download_btn.config(state="disabled")
        self.progress["value"] = 0
        self.set_status("Starting download...")
        threading.Thread(target=self._download_task, args=(url,), daemon=True).start()

    def _download_task(self, url):
        try:
            path = download_from_input(url, self.output_dir.get().strip() or DEFAULT_OUTPUT_DIR, self.quality_var.get(), self.audio_var.get())
            self.root.after(0, lambda: self.progress.config(value=100))
            self.root.after(0, lambda: self.set_status(f"Download complete: {path}"))
        except Exception as exc:
            self.root.after(0, lambda: self.set_status(f"Download failed: {exc}"))
        finally:
            self.root.after(0, lambda: self.download_btn.config(state="normal"))

    def set_status(self, message):
        self.status_var.set(message)

    def run(self):
        self.root.mainloop()
