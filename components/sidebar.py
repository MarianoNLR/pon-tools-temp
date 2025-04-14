import tkinter as tk
from views.excel_and_txt_to_txt_view import ExcelAndTxtToTxtView
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtCore import Qt

class Sidebar(QWidget):
    def __init__(self, root, main_content):
        super().__init__(root)
        
        self.root = root
        self.main_content = main_content
        # Barra lateral izquierda
        self.setMaximumWidth(350)
        
        # Layout para los botones de la barra lateral
        sidebar_layout = QVBoxLayout()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("sidebar")

        self.setAutoFillBackground(True)
        # palette = self.palette()  
        # palette.setColor(self.backgroundRole(), QColor("#eb2b2b"))
        # self.setPalette(palette)
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
                
        # Crear los botones de la barra lateral
        self.sidebar_opt1 = QPushButton("Excel - Txt a Txt", self)
        self.sidebar_opt1.setStyleSheet("color: white; font-size: 20px;")
        self.sidebar_opt1.clicked.connect(self.on_click_option1)
        self.sidebar_opt1.setProperty("sidebar_option_button", True)
        
        self.sidebar_opt2 = QPushButton("Opcion 2", self)
        self.sidebar_opt2.setProperty("sidebar_option_button", True)
        self.sidebar_opt2.setStyleSheet("color: white; font-size: 20px;")
        self.sidebar_opt2.clicked.connect(self.show_option2_frame)

        self.sidebar_opt3 = QPushButton("Opcion 3", self)
        self.sidebar_opt3.setProperty("sidebar_option_button", True)
        self.sidebar_opt3.setStyleSheet("color: white; font-size: 20px;")
        self.sidebar_opt3.clicked.connect(self.show_option3_frame)

        self.sidebar_opt4 = QPushButton("Opcion 4", self)
        self.sidebar_opt4.setProperty("sidebar_option_button", True)
        self.sidebar_opt4.setStyleSheet("color: white; font-size: 20px;")
        self.sidebar_opt4.clicked.connect(self.show_option4_frame)
        
        
        buttons = self.findChildren(QPushButton)
        
        # Aplicar el cursor de puntero a todos los botones
        for button in buttons:
            button.setCursor(Qt.PointingHandCursor)
        
        # Añadir los botones al layout
        sidebar_layout.addWidget(self.sidebar_opt1)
        sidebar_layout.addWidget(self.sidebar_opt2)
        sidebar_layout.addWidget(self.sidebar_opt3)
        sidebar_layout.addWidget(self.sidebar_opt4)
        
        self.setLayout(sidebar_layout)
        self.setStyleSheet("""
            #sidebar {
                background-image: url("D:/Projects/PON-Tools - pyside/components/prism_red.png");     
                background-color: #de4c47;
            }
            
            QPushButton[sidebar_option_button="true"] {
                background-color: transparent;
                padding: 10px;
            }
            
            QPushButton[sidebar_option_button="true"]:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        
    def on_click_option1(self):
        self.clear_main_content()
        ExcelAndTxtToTxtView(self.main_content)
        
    ### Mostrar Frame de Opcion 2
    def show_option2_frame(self):
        self.clear_main_content()  # Limpiar contenido anterior

        opcion2_frame = QFrame(self.main_content)
        opcion2_frame.setStyleSheet("background-color: #212121; height: 300px;")
        self.main_content.layout().addWidget(opcion2_frame)

        label = QLabel("Bienvenido a la Opcion 2", opcion2_frame)
        label.setStyleSheet("color: white; font-size: 40px;")
        label.setAlignment(Qt.AlignCenter)
        opcion2_frame.layout().addWidget(label)
        
    ### Mostrar Frame de Opcion 3
    def show_option3_frame(self):
        self.clear_main_content()  # Limpiar contenido anterior

        opcion3_frame = QFrame(self.main_content)
        opcion3_frame.setStyleSheet("background-color: #212121; height: 300px;")
        self.main_content.layout().addWidget(opcion3_frame)

        label = QLabel("Bienvenido a la Opcion 3", opcion3_frame)
        label.setStyleSheet("color: white; font-size: 40px;")
        label.setAlignment(Qt.AlignCenter)
        opcion3_frame.layout().addWidget(label)
        
    ### Mostrar Frame de Opcion 4
    def show_option4_frame(self):
        self.clear_main_content()  # Limpiar contenido anterior

        opcion4_frame = QFrame(self.main_content)
        opcion4_frame.setStyleSheet("background-color: #212121; height: 300px;")
        self.main_content.layout().addWidget(opcion4_frame)

        label = QLabel("Bienvenido a la Opcion 4", opcion4_frame)
        label.setStyleSheet("color: white; font-size: 40px;")
        label.setAlignment(Qt.AlignCenter)
        opcion4_frame.layout().addWidget(label)
        
    def clear_main_content(self):
        # Limpiar el contenido previo del área principal
        for i in reversed(range(self.main_content.layout().count())):
            widget_to_remove = self.main_content.layout().itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)