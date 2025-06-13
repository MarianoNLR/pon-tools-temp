from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt

class LoadingDialogView(QDialog):
    """
        Dialog used as a feedback to user to indicate a file is being loaded.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cargando...")
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(300, 100)
        self.setModal(True)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setWindowModality(Qt.ApplicationModal)

        self.label = QLabel("Cargando, por favor espere...", self)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.label)
        layout.addWidget(cancel_button)
        self.setLayout(layout)