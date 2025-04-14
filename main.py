import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from components.sidebar import Sidebar
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

class MainApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        # Configuración de la ventana principal
        self.setWindowTitle("PON Tools")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(800, 700)

        # Crear el widget principal
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout principal de la ventana
        self.main_layout = QHBoxLayout(central_widget)

        # Contenedor principal de contenido
        self.main_content = QWidget(self)
        self.main_content.setObjectName("main_content")
        self.main_content.setStyleSheet("background-color: #212121; color: white;")
        self.main_content.setMinimumHeight(300)
        self.main_content.setStyleSheet("""
            #main_content {
                background-image: url("prism.png");
            }
        """)
        
        # Crear la barra lateral
        self.sidebar = Sidebar(self, self.main_content)

        # Layout para el contenedor de contenido
        main_content_layout = QVBoxLayout(self.main_content)
        main_content_layout.setSpacing(0)
        # Agregar el frame de bienvenida
        self.show_welcome_frame(main_content_layout)

        # Agregar la barra lateral y el contenido principal al layout
        self.main_layout.addWidget(self.sidebar, stretch=1)
        self.main_layout.addWidget(self.main_content, stretch=4)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
    
    ### Mostrar Frame de Bienvenida
    def show_welcome_frame(self, layout):
        welcome_frame = QFrame(self.main_content)
        
        layout.addWidget(welcome_frame)

        # Layout del frame de bienvenida
        welcome_layout = QVBoxLayout(welcome_frame)

        # Agregar etiqueta de bienvenida
        label = QLabel("Bienvenido a PON Tools", self)
        label.setStyleSheet("color: white; font-size: 40px;")
        label.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(label)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())