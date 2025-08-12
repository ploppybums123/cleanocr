#!/usr/bin/env python3.11
import sys
import os
from io import BytesIO  # <-- Important: This new import is required
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                           QPushButton, QTextEdit, QFileDialog, QLabel,
                           QStatusBar, QWidget, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageEnhance
import pytesseract

class OCRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR HIGH QUALITY")
        self.setMinimumSize(800, 600)

        # Central widget
        central = QWidget()
        layout = QVBoxLayout()

        # Image display
        self.image_label = QLabel("Open an image to begin...") # Added initial text
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(600, 400)
        layout.addWidget(self.image_label)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_open = QPushButton("Open Image")
        self.btn_open.clicked.connect(self.open_image)
        btn_layout.addWidget(self.btn_open)

        self.btn_copy = QPushButton("Copy Text")
        self.btn_copy.setEnabled(False)
        self.btn_copy.clicked.connect(self.copy_text)
        btn_layout.addWidget(self.btn_copy)

        layout.addLayout(btn_layout)

        # Text output
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        layout.addWidget(self.text_output)

        central.setLayout(layout)
        self.setCentralWidget(central)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # NOTE: Removed the hardcoded Tesseract path.
        # It's better to ensure Tesseract is in your system's PATH.
        # pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )

        if path:
            try:
                # Load original image for processing
                img = Image.open(path)

                # --- MODIFIED SECTION FOR DISPLAYING THE PREVIEW ---
                # Create a copy for the preview display
                preview = img.copy()
                preview.thumbnail((600, 600))  # Resize for display

                # Save the preview image to an in-memory buffer
                buffer = BytesIO()
                preview.save(buffer, "PNG")  # Use PNG format for the buffer

                # Create a QPixmap and load it from the binary data in the buffer
                pixmap = QPixmap()
                pixmap.loadFromData(buffer.getvalue())

                # Set the pixmap on the label
                self.image_label.setPixmap(pixmap)
                # --- END OF MODIFIED SECTION ---

                # Pre-process the original, full-quality image for better OCR
                img = self.preprocess_image(img)

                # Perform OCR on the processed, high-quality image
                self.status.showMessage("Processing...")
                QApplication.processEvents()  # Keep UI responsive

                custom_config = r'--oem 3 --psm 6'  # OEM 3 = LSTM, PSM 6 = Assume uniform block
                text = pytesseract.image_to_string(img, config=custom_config)

                self.text_output.setPlainText(text)
                self.btn_copy.setEnabled(bool(text.strip()))
                self.status.showMessage(f"Ready - {os.path.basename(path)}")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to process image:\n{str(e)}")

    def preprocess_image(self, img):
        """Enhance image for better OCR results"""
        # Convert to grayscale (better for OCR)
        img = img.convert('L')

        # Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)  # 2.0 = 200% contrast boost

        return img

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_output.toPlainText())
        self.status.showMessage("Text copied!", 2000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Verify Tesseract exists by checking the version
    try:
        pytesseract.get_tesseract_version()
    except pytesseract.TesseractNotFoundError:
        # This gives a more user-friendly error than checking the path directly
        QMessageBox.critical(None, "Error",
            "Tesseract not found!\n\nPlease install Tesseract OCR and ensure it is in your system's PATH.\n\nOn macOS with Homebrew: brew install tesseract")
        sys.exit(1)

    window = OCRApp()
    window.show()
    sys.exit(app.exec_())
