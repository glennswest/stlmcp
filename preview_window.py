#!/usr/bin/env python3
"""
Standalone preview window that runs as a separate process.
This file is launched as a subprocess to avoid tkinter threading issues.
"""

import tkinter as tk
from PIL import Image, ImageTk
import sys
import os
import time
import signal

class PreviewWindow:
    """Standalone tkinter window for displaying STL views"""

    def __init__(self, image_dir):
        self.image_dir = image_dir
        self.root = tk.Tk()
        self.root.title("STL Viewer - Live Preview")
        self.root.geometry("800x600")

        # Create canvas for displaying images
        self.canvas = tk.Canvas(self.root, bg='gray')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Add label for instructions
        info_label = tk.Label(
            self.root,
            text="Live view of 3D scene - updates automatically",
            bg='lightgray'
        )
        info_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Track current image
        self.photo_image = None
        self.last_image_path = None
        self.last_mtime = None

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Schedule periodic check for new images
        self.check_for_updates()

    def check_for_updates(self):
        """Check for new preview image"""
        try:
            preview_file = os.path.join(self.image_dir, "current_preview.png")

            if os.path.exists(preview_file):
                # Check if file has been modified
                mtime = os.path.getmtime(preview_file)

                if self.last_mtime is None or mtime > self.last_mtime:
                    self.last_mtime = mtime
                    self.update_image(preview_file)

        except Exception as e:
            print(f"Error checking for updates: {e}", file=sys.stderr)

        # Schedule next check
        self.root.after(100, self.check_for_updates)

    def update_image(self, image_path: str):
        """Update the displayed image"""
        try:
            # Load image
            image = Image.open(image_path)

            # Resize to fit window while maintaining aspect ratio
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            if canvas_width > 1 and canvas_height > 1:
                # Calculate scaling factor
                scale = min(canvas_width / image.width, canvas_height / image.height)
                new_width = int(image.width * scale)
                new_height = int(image.height * scale)

                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert to PhotoImage and display
            self.photo_image = ImageTk.PhotoImage(image)

            # Clear canvas and display new image
            self.canvas.delete("all")
            self.canvas.create_image(
                canvas_width // 2,
                canvas_height // 2,
                image=self.photo_image,
                anchor=tk.CENTER
            )

        except Exception as e:
            print(f"Error updating image: {e}", file=sys.stderr)

    def on_close(self):
        """Handle window close"""
        self.root.quit()
        self.root.destroy()

    def run(self):
        """Start the main loop"""
        self.root.mainloop()


def main():
    if len(sys.argv) < 2:
        print("Usage: preview_window.py <image_directory>", file=sys.stderr)
        sys.exit(1)

    image_dir = sys.argv[1]

    # Handle SIGTERM gracefully
    def signal_handler(signum, frame):
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)

    try:
        window = PreviewWindow(image_dir)
        window.run()
    except Exception as e:
        print(f"Error running preview window: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
