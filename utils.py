import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk

from config import APP_TITLE, DEFAULT_OUTPUT_DIR, QUALITY_CHOICES
from downloader import download_from_input


class DownloadApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("720x420")
        self.root.minsize(620, 340)

        self.setup_ui()

    def setup_ui(self):
        main = ttk.Frame(self.root, padding=18)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="YouTube Video URL", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(8, 4))
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(main, textvariable=self.url_var, width=80)
        self.url_entry.pack(fill="x", pady=(0, 10))

        toolbar = ttk.Frame(main)
        toolbar.pack(fill="x", pady=(0, 12))

        ttk.Label(toolbar, text="Save to:").pack(side="left")
        self.output_dir = tk.StringVar(value=DEFAULT_OUTPUT_DIR)
        ttk.Entry(toolbar, textvariable=self.output_dir, width=38).pack(side="left", padx=(8, 8))
        ttk.Button(toolbar, text="Browse", command=self.choose_directory).pack(side="left")

        options = ttk.Frame(main)
        options.pack(fill="x", pady=(0, 12))

        ttk.Label(options, text="Quality:").pack(side="left")
        self.quality_var = tk.StringVar(value=QUALITY_CHOICES[0])
        self.quality_combo = ttk.Combobox(options, textvariable=self.quality_var, values=QUALITY_CHOICES, state="readonly", width=12)
        self.quality_combo.pack(side="left", padx=(8, 16))

        self.audio_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options, text="Audio only", variable=self.audio_var).pack(side="left")

        button_row = ttk.Frame(main)
        button_row.pack(fill="x", pady=(0, 12))
        self.download_btn = ttk.Button(button_row, text="Download", command=self.start_download)
        self.download_btn.pack(side="left")

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main, textvariable=self.status_var, foreground="#1f5f8c", wraplength=640, justify="left").pack(anchor="w", pady=(8, 0))

        self.progress = ttk.Progressbar(main, orient="horizontal", mode="determinate", length=640)
        self.progress.pack(fill="x", pady=(12, 0))
        self.progress['value'] = 0

    def choose_directory(self):
        directory = filedialog.askdirectory(initialdir=self.output_dir.get() or DEFAULT_OUTPUT_DIR)
        if directory:
            self.output_dir.set(directory)

    def start_download(self):
        url = self.url_var.get().strip()
        output_dir = self.output_dir.get().strip() or DEFAULT_OUTPUT_DIR
        quality = self.quality_var.get()
        audio_only = self.audio_var.get()

        if not url:
            self.set_status("Please enter a YouTube video URL.")
            return

        self.download_btn.config(state="disabled")
        self.progress['value'] = 0
        self.set_status("Starting download...")

        thread = threading.Thread(
            target=self._download_task,
            args=(url, output_dir, quality, audio_only),
            daemon=True,
        )
        thread.start()

    def _download_task(self, url, output_dir, quality, audio_only):
        try:
            output_path = download_from_input(url, output_dir=output_dir, quality=quality, audio_only=audio_only)
            self.root.after(0, lambda: self.set_status(f"Download complete: {output_path}"))
            self.root.after(0, lambda: self.progress.config(value=100))
        except Exception as exc:
            self.root.after(0, lambda: self.set_status(f"Download failed: {exc}"))
        finally:
            self.root.after(0, lambda: self.download_btn.config(state="normal"))

    def set_status(self, message):
        self.status_var.set(message)

    def run(self):
        self.root.mainloop()
