import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from components.sidebar import Sidebar
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from resource_path import resource_path

class MainApp(QMainWindow):
    """
    Main Window of the App
    Contains Sidebar and a main frame to display options/operations availables in the app
    """
    
    def __init__(self):
        super().__init__()
        # Main Window Configuration
        self.setWindowTitle("PON Tools")
        self.setGeometry(100, 100, 1300, 800)
        self.setMinimumSize(800, 700)

        # Main widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main Window's Layout
        self.main_layout = QHBoxLayout(central_widget)

        # Main content container
        bg_img_path = resource_path("assets/prism.png")
        self.main_content = QWidget(self)
        self.main_content.setObjectName("main_content")
        self.main_content.setStyleSheet("background-color: #212121; color: white;")
        self.main_content.setMinimumHeight(300)
        self.main_content.setStyleSheet(f"""
            #main_content {{
                background-image: url("{bg_img_path.replace("\\", "/")}");
            }}
        """)
        
        # Sidebar creation
        self.sidebar = Sidebar(self, self.main_content)

        # Content container's layout
        main_content_layout = QVBoxLayout(self.main_content)
        main_content_layout.setSpacing(0)
        # Showing welcome frame when app initialize
        self.show_welcome_frame(main_content_layout)

        # Adding widgets 
        self.main_layout.addWidget(self.sidebar, stretch=1)
        self.main_layout.addWidget(self.main_content, stretch=4)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
    
    def show_welcome_frame(self, layout):
        """
        Show a simple welcome message in the main frame besides sidebar
        """
        welcome_frame = QFrame(self.main_content)
        
        layout.addWidget(welcome_frame)

        # Welcome frame Layout
        welcome_layout = QVBoxLayout(welcome_frame)

        # Welcome Label
        label = QLabel("Bienvenido a PON Tools", self)
        label.setStyleSheet("color: white; font-size: 40px;")
        label.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(label)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())