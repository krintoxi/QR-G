# Modern QR Code Generator
# Optimized for Ubuntu/Linux with a contemporary style.
#
# Required libraries:
# - tkinter (system): sudo apt install python3-tk
# - qrcode: python3 -m pip install "qrcode[pil]"
# - requests: python3 -m pip install requests

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
import qrcode.image.svg
from PIL import Image
from PIL import ImageTk 
import os
import base64
from io import BytesIO
import webbrowser
import requests

# --- Constants ---
APP_TITLE = """InterCuba.Net QR Code Generator - Linux Edition (Debian Tested)
                """""
WINDOW_SIZE = "700x750" # Window height reduced since the URL input is gone
HARDCODED_LOGO_URL = "https://www.maestrosdelweb.com/images/actualidad/ima_cubalinux.jpg" # The logo URL is now FIXED here.

# --- App Icon (Base64 encoded - same as before) ---
ICON_DATA = b"""
iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAEcElEQVR4nO2by4sVVRjGn/fOuffMnYkzl
yQaH5rgRhceKqUg6MIlXYhuRAnu3LhR8A+4E2/iRkARwY1gV5tuBEGE3Ysuws7l4UYXpWgmRzMzmTOfe+7
Uqe4prprp6Z6q3vVp/2Bp1VXVb/1v+qsqn/dAwRBEARBEARBEARBEARBEARB8J8gqNVq6Xa722y2Wq1uNJ
ttN/p8Pv8/YGb7fX9brVbrtNvtNpvNbrfbfT5fjMbD/BqDwQDP56PRaPR7/Vwud7PZjMfjJicn+n0+M6/W
6/Wi0SgSicBut2s0Gg6HA4vFok6ns9lsVqs1n89jsVg0Go0wDAwGA4VCIRqNGo1GDocDlmXR6XQajSYYDM
jlcplMJpfL5XK5zGaz2+0ajcZisfC9RqOByWTC8zxVVVVVdf7P3P92fX39/Pz80NDQwMCAgICAgIDg5eUl
JibGxsZGJpMJBAKEw+FAICAYDAaDwYDAeDwaDIbFYjEYDFp7enra2tpiY2OjoqIiLy8vMDBQp9MZDAZptV
qpVOJ5ngzDIBgM0el0kiThwWBQq9UajYbL5TJbLAaDAYfDAZ7nJ0+ePHr06KNHj548efLXr1+Ojo7asmXL
unXrli5d2rp16+PHj58+ffrkyZMnT548+e/XrwMCAvLysqioKC8vDwkJ0ev1MpnMZrNpNBqfz+fxeAoLCx
MTE7Ozs5OTk5OTk2NjY2NjYxMTEwsLC/Pz83fv3l2/fv2DRs2bNiQnZ1dUlKSk5Pz4sWLp0+fvnv37tOn
T1++fPnu3buHDx8+f/789evXv//+u3Dhwr1793bu3Llz584DBw4cO3asurpaU1NTWlpaXV3d0NBQbW1tZW
VlRUVFYWFhYWHhwMBAVVXV1NTU3NzcysoqvG/YsGF1dfX+/ftXr1598uTJEyZM2Lp1a2VlpcjISHx8fGBg
IH19fWZmZnZ2dnZ2NiAgwGaz8Xq9rutGo5HNZnM4HLqum0wmm82Wz+ep1WqDwSAej+N5/vTp08ePH8/Pz0
9PT4+Ojj5//vzhw4fn5+fXr18PDw8PDg729fXduXPH3r17d+7c6XA4cnNza2pqCgsLGxoaqqur5+bmoNPp
oNfrlUoldrvd6/WazWYqlcqCgoKCgoKgoCBVVVVeXl5tbW1sbGxoaGhtbW1ramppaWltbW1jY2NtbQ19ff
2TJ0+ePXv25MmTX19fr127duPGjVOnTq1Zs6awsPD8+fPnz58/efLk/Pz88vJyXl7e/fv3jx8/Pjg4GBsb
u3DhQm1tbVFREalUSkdHR2VlZWpqamFhYXt7+/z8/P7+fkBAAE3TlmVZlmVZlmVd13Vd13Vd13VdVavVzW
aTTqfT6bTValWr1Wq1Wq1Wu67rur/ruq5pmsaZpmkaZpqm6bqum6ZpGub/jGkaZp7n+TzPc3w+nyzLsixb
VVXVNE03DMNgMBhVVU0mkwzDMMsajUatViORSCRSqVSpVEomk5qm+Tz/H+C3v/W1A/i/36PRuGmavq7ruq
7ruq5pmsaZpmme5/k8n8/n8/V63e/3+/0+nuf1ej0+n89kMsEwvK6q1+tVVVVVVRVNU9d1nucpFAqVSiUej
eN5/q8KgiAIgiAIgiAIgiAIgiAIgvhf+QfXn4aM/0rP/AAAAABJRU5ErkJggg==
"""

# --- Color and Font Palette (Modern, clean, and Linux-compatible) ---
COLOR_BACKGROUND = "#ffffff"
COLOR_FRAME = "#ffffff"
COLOR_TEXT = "#1d1d1f"
COLOR_TEXT_SECONDARY = "#6e6e73"
COLOR_ACCENT = "#007aff"
COLOR_ACCENT_TEXT = "#ffffff"
COLOR_ERROR = "#ff3b30"

# Using Cantarell, a modern, highly available Linux font
FONT_NAME = "Cantarell" 

FONT_PRIMARY = (FONT_NAME, 14)
FONT_BUTTON = (FONT_NAME, 14, "bold")
FONT_ENTRY = (FONT_NAME, 14)
FONT_STATUS = (FONT_NAME, 12)
FONT_TITLE = (FONT_NAME, 24, "bold")

class QRCodeApp(tk.Tk):
    """
    The main application class for the QR Code Generator.
    It sets up the UI and handles the QR code generation logic.
    """
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.resizable(False, False)
        self.configure(bg=COLOR_BACKGROUND)
        self._set_app_icon()

        # --- Style Configuration ---
        self._setup_styles()

        # --- Tkinter Variables ---
        self.url_var = tk.StringVar()
        self.logo_path_var = tk.StringVar()
        self.output_format_var = tk.StringVar(value="PNG (Digital)")
        self.status_var = tk.StringVar(value="Enter a URL to begin.")
        self.logo_image = None
        self.app_icon = None
        self.header_logo_image = None

        # --- UI Creation ---
        self._create_widgets()
        
        # Call the logo loader immediately using the hardcoded URL
        self._load_header_logo(HARDCODED_LOGO_URL)

    def _set_app_icon(self):
        """Sets the application icon from base64 data."""
        try:
            image_data = base64.b64decode(ICON_DATA)
            image = Image.open(BytesIO(image_data))
            self.app_icon = ImageTk.PhotoImage(image)
            self.iconphoto(True, self.app_icon)
        except Exception as e:
            print(f"Error setting app icon: {e}") 

    def _setup_styles(self):
        """Configures ttk styles for a modern, flat appearance."""
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('.', background=COLOR_FRAME, foreground=COLOR_TEXT,
                        fieldbackground=COLOR_FRAME, borderwidth=0, focuscolor='none') 
        style.configure('TFrame', background=COLOR_FRAME)
        style.configure('TLabel', background=COLOR_FRAME, font=FONT_PRIMARY)
        style.configure('Secondary.TLabel', foreground=COLOR_TEXT_SECONDARY, font=(FONT_NAME, 12))
        style.configure('TEntry', font=FONT_ENTRY, borderwidth=1, relief="flat", padding=5)
        style.map('TEntry', bordercolor=[('focus', COLOR_ACCENT), ('!focus', '#d8d8d8')])
        style.configure('TCombobox', font=FONT_ENTRY, borderwidth=1, relief="flat", padding=5)
        style.map('TCombobox', bordercolor=[('focus', COLOR_ACCENT), ('!focus', '#d8d8d8')])
        style.configure('TButton', font=FONT_PRIMARY, padding=(15, 10), relief="flat")
        style.configure('Accent.TButton', background=COLOR_ACCENT, foreground=COLOR_ACCENT_TEXT,
                        font=FONT_BUTTON, borderwidth=0) 
        style.map('Accent.TButton', background=[('active', '#005bb5')]) 

    def _load_header_logo(self, url):
        """Downloads and displays the small logo in the header."""
        # Check if the URL is set. If not, do nothing.
        if not url:
            self.header_logo_label.config(image='', text="")
            self.header_logo_image = None
            return

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status() # Raise exception for bad status codes

            img = Image.open(BytesIO(response.content))
            img.thumbnail((50, 50)) 
            
            self.header_logo_image = ImageTk.PhotoImage(img) 
            self.header_logo_label.config(image=self.header_logo_image, text="", padding=5)
        
        except requests.exceptions.RequestException as e:
            # Failed to load logo (connection error, 404, etc.). Show nothing.
            print(f"Failed to load logo from URL: {e}")
            self.header_logo_label.config(image='', text="")
            self.header_logo_image = None
        except Exception as e:
            # Invalid image format or other processing errors. Show nothing.
            print(f"Image processing error: {e}")
            self.header_logo_label.config(image='', text="")
            self.header_logo_image = None


    def _create_widgets(self):
        """Creates and lays out all the UI widgets in the main window."""
        
        # --- Header Logo Frame (No URL Input) ---
        header_frame = ttk.Frame(self, style='TFrame', height=60)
        header_frame.pack(fill='x', padx=20, pady=(20, 0))
        header_frame.columnconfigure(0, weight=1)

        # Centered label for the logo (now just a placeholder for the image)
        self.header_logo_label = ttk.Label(header_frame, text="", style='TLabel', anchor='center')
        self.header_logo_label.grid(row=0, column=0, sticky='nsew', pady=(0, 10))
        
        # --- Main content frame ---
        main_frame = ttk.Frame(self, padding=(30, 25), style='TFrame')
        main_frame.pack(expand=True, fill='both', padx=20, pady=(10, 20))

        # --- App Title Header ---
        ttk.Label(main_frame, text="QR Code Generator", font=FONT_TITLE).grid(
            row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))
        ttk.Label(main_frame, text="Create and customize your QR codes in seconds.", style='Secondary.TLabel').grid(
            row=1, column=0, columnspan=2, sticky='w', pady=(0, 30))

        # --- URL Input (Content) ---
        ttk.Label(main_frame, text="URL / Content", font=(FONT_NAME, 14, 'bold')).grid(
            row=2, column=0, columnspan=2, sticky='w', pady=(0, 5))
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=40)
        url_entry.grid(row=3, column=0, columnspan=2, sticky='ew')
        url_entry.focus()

        # URL Input Context Menu (for right-click paste)
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Paste", command=lambda: url_entry.event_generate('<<Paste>>'))
        def show_context_menu(event):
            context_menu.tk_popup(event.x_root, event.y_root)
        url_entry.bind("<Button-3>", show_context_menu) 

        # --- Logo Selection (Embedded QR Code) ---
        ttk.Label(main_frame, text="Logo Overlay (Embedded)", font=(FONT_NAME, 14, 'bold')).grid(
            row=4, column=0, sticky='w', pady=(25, 5))
        ttk.Label(main_frame, text="(Optional, PNG output only)", style='Secondary.TLabel').grid(
            row=4, column=1, sticky='w', pady=(25, 5), padx=(5,0))

        # Use a sub-frame for entry and button alignment
        logo_frame = ttk.Frame(main_frame, style='TFrame')
        logo_frame.grid(row=5, column=0, columnspan=2, sticky='ew')
        logo_frame.columnconfigure(0, weight=3)
        logo_frame.columnconfigure(1, weight=1)

        self.logo_path_entry = ttk.Entry(logo_frame, textvariable=self.logo_path_var, state='readonly')
        self.logo_path_entry.grid(row=0, column=0, sticky='ew')

        self.browse_button = ttk.Button(logo_frame, text="Browse...", command=self._select_logo)
        self.browse_button.grid(row=0, column=1, sticky='ew', padx=(10, 0))

        # --- Logo Preview ---
        self.logo_preview_label = ttk.Label(main_frame, text="No logo selected", style='Secondary.TLabel', anchor='center')
        self.logo_preview_label.grid(row=6, column=0, columnspan=2, pady=(15, 10), sticky='ewns')
        main_frame.grid_rowconfigure(6, minsize=80) 

        # --- Output Type Selection ---
        ttk.Label(main_frame, text="Output Format", font=(FONT_NAME, 14, 'bold')).grid(
            row=7, column=0, columnspan=2, sticky='w', pady=(25, 5))
        output_combo = ttk.Combobox(main_frame, textvariable=self.output_format_var,
                                     values=["PNG (Digital)", "SVG (Print)"], state='readonly')
        output_combo.grid(row=8, column=0, columnspan=2, sticky='ew') 
        output_combo.bind("<<ComboboxSelected>>", self._toggle_logo_state)
        
        # --- Generate Button ---
        generate_button = ttk.Button(main_frame, text="Generate QR Code", style='Accent.TButton', command=self._generate_qr)
        generate_button.grid(row=9, column=0, columnspan=2, sticky='ew', pady=(40, 10))

        # --- Status Bar ---
        status_label = ttk.Label(self, textvariable=self.status_var, font=FONT_STATUS,
                                 background=COLOR_BACKGROUND, foreground=COLOR_TEXT_SECONDARY,
                                 padding=(15, 8), anchor='center')
        status_label.pack(side='bottom', fill='x')

        # --- Footer Link ---
        link_label = tk.Label(self, text="Developed with ♥ by InterCuba.Net",
                              font=(FONT_NAME, 11),
                              fg=COLOR_ACCENT,
                              bg=COLOR_BACKGROUND,
                              cursor="hand2")
        link_label.pack(side='bottom', pady=(0, 10))
        link_label.bind("<Button-1>", lambda e: self._open_link("https://www.intercuba.net"))

        # Grid column configuration for proper spacing
        main_frame.grid_columnconfigure(0, weight=3)
        main_frame.grid_columnconfigure(1, weight=1)

    def _open_link(self, url):
        """Opens the given URL in the default web browser."""
        webbrowser.open_new(url)

    def _select_logo(self):
        """Opens a file dialog to select a logo image."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")]
        )
        if file_path:
            self.logo_path_var.set(file_path)
            self._update_logo_preview(file_path)
            self.status_var.set("Logo selected.")

    def _update_logo_preview(self, path):
        """Displays a small preview of the selected logo."""
        try:
            img = Image.open(path)
            img.thumbnail((70, 70)) 
            self.logo_image = ImageTk.PhotoImage(img) 
            self.logo_preview_label.config(image=self.logo_image, text="", borderwidth=0, relief="flat")
        except Exception:
            self.logo_path_var.set("") 
            self.logo_preview_label.config(image='', text="Invalid Image")

    def _toggle_logo_state(self, event=None):
        """Enables/disables the logo selection based on output format."""
        if self.output_format_var.get() == "SVG (Print)":
            self.browse_button.config(state='disabled')
            self.logo_path_entry.config(state='disabled')
            self.status_var.set("Logo is not supported for SVG output.")
            self.logo_preview_label.config(image='', text="Not available for SVG")
            self.logo_image = None
        else:
            self.browse_button.config(state='normal')
            self.logo_path_entry.config(state='readonly')
            self.status_var.set("Ready.")
            if self.logo_path_var.get():
                self._update_logo_preview(self.logo_path_var.get())

    def _generate_qr(self):
        """Validates input and generates the QR code."""
        url = self.url_var.get().strip()
        logo_path = self.logo_path_var.get()
        output_format = self.output_format_var.get()

        if not url:
            messagebox.showerror("Error", "URL or content cannot be empty.")
            self.status_var.set("Error: Content is required.")
            return

        self.status_var.set("Generating, please wait...")
        self.update_idletasks()

        try:
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=12,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            if output_format == "PNG (Digital)":
                self._save_png(qr, logo_path)
            elif output_format == "SVG (Print)":
                self._save_svg(qr)

        except Exception as e:
            messagebox.showerror("Generation Failed", f"An unexpected error occurred:\n{e}")
            self.status_var.set(f"Error: {e}")

    def _save_png(self, qr_instance, logo_path):
        """Creates and saves the QR code as a PNG file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile="qrcode.png"
        )
        if not file_path:
            self.status_var.set("Save operation cancelled.")
            return

        img = qr_instance.make_image(fill_color="black", back_color="white").convert('RGBA')

        if logo_path:
            try:
                logo = Image.open(logo_path).convert('RGBA')
                qr_width, _ = img.size
                logo_max_size = int(qr_width / 4)
                logo.thumbnail((logo_max_size, logo_max_size))
                pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
                img.paste(logo, pos, logo)
            except Exception as e:
                messagebox.showwarning("Logo Error", f"Could not embed logo. Ensure it's a valid image.\nError: {e}")
                self.status_var.set(f"Warning: Could not add logo. Saved without it.")
        
        img.save(file_path)
        self.status_var.set(f"Success! Saved as {os.path.basename(file_path)}")

    def _save_svg(self, qr_instance):
        """Creates and saves the QR code as an SVG file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".svg",
            filetypes=[("SVG files", "*.svg"), ("All files", "*.*")],
            initialfile="qrcode.svg"
        )
        if not file_path:
            self.status_var.set("Save operation cancelled.")
            return

        img = qr_instance.make_image(image_factory=qrcode.image.svg.SvgPathImage)
        img.save(file_path)
        self.status_var.set(f"Success! Saved as {os.path.basename(file_path)}")


if __name__ == "__main__":
    app = QRCodeApp()
    app.mainloop()
