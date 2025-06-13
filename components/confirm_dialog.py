from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout

class ConfirmDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Confirmar acción")

        self.label = QLabel("Hay filas con datos no numericos en el filtro seleccionado. Quiere descartar dichas filas?")
        
        # Botones
        self.option_yes_btn = QPushButton("Si")
        self.option_no_btn = QPushButton("No")
        

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.option_yes_btn)
        layout.addWidget(self.option_no_btn)
        self.setLayout(layout)

        self.option_no_btn.clicked.connect(lambda: self.done(1))
        self.option_yes_btn.clicked.connect(lambda: self.done(2))