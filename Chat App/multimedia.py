from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

def preview_file(file_path):
    label = QLabel()
    pixmap = QPixmap(file_path)
    label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
    return label
