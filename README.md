# SCT_CS_2
Simple Image Encryption Tool
A simple image encryption and decryption tool built using Python that demonstrates how pixel-level manipulation can be used to hide visual information in images. This project is designed for educational and internship purposes to explore the fundamentals of image data handling, reversible transformations, and key-based encryption logic.

> This tool is meant for educational and demonstrative purposes only. It does not offer real-world cryptographic security.

## Features
- Upload .jpg or .png image
- Encrypt using:
    - Pixel Swapping (based on password-derived).
    - Bitwise XOR encryption.
- Decrypt the image with the same password
- Saved encrypted and decrypted image with a timestamp filename
- View encryption and decryption history on the board 
- user-friendly interface with tkinter

## Tech Stack

- **Language**: Python 3.x  
- **Libraries Used**:
  - `Tkinter` - for GUI
  - `PIL (Pillow)` - for image handling
  - `NumPy` - for pixel data manipulation
  - `hashlib` - for password hashing (SHA-256)

## How It Works

1. **Upload Image**: Opens a `.jpg` or `.png` and standardizes it to RGB.
2. **Password Entry**: The password is hashed using SHA-256 and sliced into:
   - XOR Key – modifies pixel values.
   - Swap Key – scrambles pixel positions.
3. **Encryption**:
   - Pixels are shuffled based on the swap key.
   - Each pixel value is XOR-encrypted using the XOR key.
4. **Decryption**:
   - XOR is reversed using the same key.
   - Pixels are unshuffled to their original positions.

### Prerequisites

- Python 3.x installed

### Installation

```bash
git clone  "https://github.com/nidraoo/SCT_CS_2.git"      
cd PixelCrypt      
pip install pillow numpy