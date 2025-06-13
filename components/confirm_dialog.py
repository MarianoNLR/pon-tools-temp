from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout

class ConfirmDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Confirmar acción")

        self.label = QLabel("Hay filas con datos no numericos en el filtro seleccionado. Quiere descartar dichas filas?")
        
        # Botones
        self.continuar_btn = QPushButton("Si")
        self.descartar_btn = QPushButton("No")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.continuar_btn)
        layout.addWidget(self.descartar_btn)
        self.setLayout(layout)

        self.continuar_btn.clicked.connect(lambda: self.done(1))
        self.descartar_btn.clicked.connect(lambda: self.done(2))