# InterCuba.Net QR Code Generator

A modern **Python 3 Tkinter application** for creating QR codes from URLs.  
Easily generate **PNG (digital use)** or **SVG (print use)** QR codes, with optional logo embedding at the center.
_________________________________________________
1.Enter the URL you want to encode.
2.(Optional) Choose a logo image to embed.
3.Select output format: PNG or SVG.
4.Click Generate QR Code and save the file.
5.Share the QR code—anyone can scan it forever!
_________________________________________________
## ✨ Features
- Clean and modern Tkinter UI
- Generate QR codes from any URL
- Export formats:
  - **PNG** (with optional logo overlay in the center)
  - **SVG** (scalable, print-ready)
- Logo preview before embedding
- Right-click paste support in URL input
- Persistent QR codes (forever valid as long as the link is live)
- Status bar and error handling
_________________________________________________
## 📦 Requirements
Python 3.7+
qrcode
Pillow (PIL)

- pip install -r requirements.txt
____________________________________________

## 🚀 Installation
____________________________________________

1. Download zip or clone using Git.
2. Install Requirements.txt (pip install -r requirements.txt)
3. Run using : python3 QR-G.py
____________________________________________
## 💡 Notes
PNG with logo requires high error correction, already built in.
SVG output does not support logos.
The QR code itself never expires, but the link must remain active.