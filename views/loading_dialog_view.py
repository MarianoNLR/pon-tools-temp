from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class LoadingDialogView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cargando...")
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(300, 100)

        self.label = QLabel("Cargando, por favor espere...", self)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)