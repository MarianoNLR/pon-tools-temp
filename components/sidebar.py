import tkinter as tk
from views.excel_and_txt_to_txt_view import ExcelAndTxtToTxtView
from views.delete_duplicates_view import DeleteDuplicateView
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtCore import Qt
from resource_path import resource_path

class Sidebar(QWidget):
    """
    Graphic Component that works as a sidebar of the application.
    It contains the available options and it is placed inside main container ('root')
    
    Args:
        root (QWidget): Father which contains Sidebar.
        main_content (QWidget): Reference to main content to interact from sidebar.
    """
    def __init__(self, root, main_content):
        super().__init__(root)
        
        self.root = root
        self.main_content = main_content
        # Left Sidebar
        self.setMaximumWidth(350)
           
        # Sidebar Buttons Layout
        sidebar_layout = QVBoxLayout()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("sidebar")

        self.setAutoFillBackground(True)
        # palette = self.palette()  
        # palette.setColor(self.backgroundRole(), QColor("#eb2b2b"))
        # self.setPalette(palette)
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
                
        #region Creating Sidebar Buttons
        self.sidebar_excel_and_txt_to_txt = QPushButton("Cruce de Datos", self)
        self.sidebar_excel_and_txt_to_txt.setStyleSheet("color: white; font-size: 20px;")
        self.sidebar_excel_and_txt_to_txt.clicked.connect(self.on_click_excel_and_txt_to_txt)
        self.sidebar_excel_and_txt_to_txt.setProperty("sidebar_option_button", True)
        
        self.delete_duplicates = QPushButton("Eliminar Duplicados", self)
        self.delete_duplicates.setProperty("sidebar_option_button", True)
        self.delete_duplicates.setStyleSheet("color: white; font-size: 20px;")
        self.delete_duplicates.clicked.connect(self.on_click_delete_duplicates)
        
        buttons = self.findChildren(QPushButton)
        
        # Aplicar el cursor de puntero a todos los botones
        for button in buttons:
            button.setCursor(Qt.PointingHandCursor)
        
        # Añadir los botones al layout
        sidebar_layout.addWidget(self.sidebar_excel_and_txt_to_txt)
        sidebar_layout.addWidget(self.delete_duplicates)
        #endregion
        
        self.setLayout(sidebar_layout)
        
        # Sidebar Styles
        bg_img_path = resource_path("assets/prism_red.png")
        self.setStyleSheet(f"""
            #sidebar {{
                background-image: url("{bg_img_path.replace("\\", "/")}");     
                background-color: #de4c47;
            }}
            
            QPushButton[sidebar_option_button="true"] {{
                background-color: transparent;
                padding: 10px;
            }}
            
            QPushButton[sidebar_option_button="true"]:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
        """)
        
    def on_click_excel_and_txt_to_txt(self):
        self.clear_main_content()
        ExcelAndTxtToTxtView(self.main_content)
        
    ### Mostrar Frame de Opcion 2
    def on_click_delete_duplicates(self):
        self.clear_main_content()  # Limpiar contenido anterior
        DeleteDuplicateView(self.main_content)
        
    def clear_main_content(self):
        # Clear previous content in main container
        for i in reversed(range(self.main_content.layout().count())):
            widget_to_remove = self.main_content.layout().itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)