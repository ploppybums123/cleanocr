# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CleanOCR is a PyQt5-based desktop application for optical character recognition (OCR). It provides a simple GUI for loading images and extracting text using Tesseract OCR.

## Setup and Development

### Environment Setup
```bash
# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR (required external dependency)
brew install tesseract  # On macOS
# apt-get install tesseract-ocr  # On Ubuntu/Debian
# choco install tesseract  # On Windows
```

### Running the Application
```bash
# Development mode
python ocr_final.py

# Or with explicit Python version
python3.11 ocr_final.py
```

### Building macOS Application
```bash
# Build standalone .app using PyInstaller
pyinstaller OCR-HQ.spec

# Output will be in dist/OCR-HQ.app
```

## Architecture

**Single-file application** (`ocr_final.py`): All functionality is contained in one Python file.

### Key Components

- **OCRApp** (main class): QMainWindow-based GUI application
  - **Image handling**: Loads images, creates preview thumbnails using PIL
  - **OCR processing**: Uses pytesseract with custom config (LSTM engine, uniform block mode)
  - **Image preprocessing** (`preprocess_image`): Converts to grayscale and enhances contrast (2.0x) for better OCR accuracy

### Image Processing Pipeline

1. Load image with PIL
2. Create thumbnail preview (600x600) for display
3. Preprocess full-quality image:
   - Convert to grayscale (`img.convert('L')`)
   - Enhance contrast (200% boost)
4. Run Tesseract with config: `--oem 3 --psm 6`
   - OEM 3 = LSTM neural network engine
   - PSM 6 = Assume uniform block of text

## Dependencies

- **PyQt5**: GUI framework
- **Pillow (PIL)**: Image processing
- **pytesseract**: Python wrapper for Tesseract OCR
- **Tesseract OCR**: External binary (must be in system PATH)

## Important Notes

- Tesseract must be installed separately and available in system PATH
- Application expects Python 3.11 (see shebang in ocr_final.py)
- PyInstaller spec file (`OCR-HQ.spec`) configured for macOS .app bundle with custom icon
