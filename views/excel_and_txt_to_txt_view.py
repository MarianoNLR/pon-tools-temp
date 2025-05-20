import tkinter as tk
from tkinter import ttk
from controllers.excel_and_txt_to_txt_controller import ExcelAndTxtToTxtController
import tkintertools as tkt
import customtkinter as ctk
import re
from tkinter import messagebox
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QTextEdit, QHBoxLayout, QComboBox, QLabel, QMessageBox, QTextBrowser
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from views.errors_details_view import ErrorsDetailsView


class ExcelAndTxtToTxtView(QWidget):
    ### Mostrar Frame de ExcelAndTxtToTxtView
    def __init__(self, main_frame):
        super().__init__(main_frame)
        
        self.controller = ExcelAndTxtToTxtController(self)
        self.excel_details = None
        self.txt_details = None
        # Variables para control de errores
        self.process_result_details = {}
        self.files_abstract_structure = {}
        self.setObjectName("ExcelAndTxtToTxtView")  # Para usar en QSS

        self.setStyleSheet("""
            #ExcelAndTxtToTxtView {
                background-color: 'red'
            }
        """)
                
        main_contaniner = QVBoxLayout()
        main_contaniner.setSpacing(10)
        main_contaniner.setContentsMargins(0,0,0,0)
        
        #Titulo
        title = QLabel("Cruce de Datos Excel - Txt y Generación de Txt")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 24px")
        # Contenedor archivos
        open_files_layout = QHBoxLayout()
        open_files_container = QWidget(self)
        open_excel_button = QPushButton("Abrir Excel") 
        open_txt_button =  QPushButton("Abrir Txt")
        open_files_layout.addWidget(open_excel_button)
        open_files_layout.addWidget(open_txt_button)
        open_files_container.setLayout(open_files_layout)
        open_excel_button.setCursor(Qt.PointingHandCursor)
        open_txt_button.setCursor(Qt.PointingHandCursor)
        # Contenedor inputs
        inputs_layout = QGridLayout()
        inputs_container = QWidget(self)
        open_excel_button.clicked.connect(self.on_open_excel_button_click)
        open_txt_button.clicked.connect(self.on_open_txt_button_click)
        
        columns_options_layout = QVBoxLayout()
        columns_options_container = QWidget(inputs_container)
        columns_select_container = QWidget(columns_options_container)
        columns_select_layout = QVBoxLayout()
        columns_select_label = QLabel("Columnas:")
        self.columns_select = QComboBox()
        columns_select_layout.addWidget(columns_select_label)
        columns_select_layout.addWidget(self.columns_select)
        columns_select_container.setLayout(columns_select_layout)
        
        columns_options_layout.addWidget(columns_select_container)
        columns_options_container.setLayout(columns_options_layout)
        columns_select_label.setStyleSheet("font-size: 16px; color: #ffffff")
        self.columns_select.setStyleSheet("""
            background-color: #ffffff;
            color: #000000;
            font-size: 16px;
            padding: 3px                     
        """)
        
        position_inputs_layout = QVBoxLayout()
        position_inputs_container = QWidget(inputs_container)
        txt_start_position_label = QLabel("Posicion inicio:")
        self.txt_start_position_input = QLineEdit()
        txt_start_position_layout = QVBoxLayout()
        txt_start_position_layout.addWidget(txt_start_position_label)
        txt_start_position_layout.addWidget(self.txt_start_position_input)
        txt_start_position_container = QWidget()
        txt_start_position_container.setLayout(txt_start_position_layout)
        self.txt_start_position_input.setValidator(QIntValidator())
        txt_start_position_label.setStyleSheet("font-size: 16px; color: #ffffff")
        
        txt_end_position_label = QLabel("Posicion fin:")
        self.txt_end_position_input = QLineEdit()
        txt_end_position_layout = QVBoxLayout()
        txt_end_position_layout.addWidget(txt_end_position_label)
        txt_end_position_layout.addWidget(self.txt_end_position_input)
        txt_end_position_container = QWidget(inputs_container)
        txt_end_position_container.setLayout(txt_end_position_layout)
        self.txt_end_position_input.setValidator(QIntValidator())
        txt_end_position_label.setStyleSheet("font-size: 16px; color: #ffffff")
        
        position_inputs_layout.addWidget(txt_start_position_container)
        position_inputs_layout.addWidget(txt_end_position_container)
        position_inputs_container.setLayout(position_inputs_layout)
        position_inputs_layout.setSpacing(20)
        
        inputs_layout.addWidget(columns_options_container, 0, 0, alignment=Qt.AlignTop)
        inputs_layout.addWidget(position_inputs_container, 0, 1)
        inputs_layout.setColumnStretch(0, 1)
        inputs_layout.setColumnStretch(1, 1)
        inputs_container.setLayout(inputs_layout)
        
        # Boton de procesar archivos
        process_files_button = QPushButton("Procesar archivos")
        process_files_button.setStyleSheet("""
            background-color: #702525;
            color: #ffffff;
            padding: 5px, 10px, 10px, 10px;
            font-size: 16px 
        """)
        process_files_button.setCursor(Qt.PointingHandCursor)
        process_files_button.clicked.connect(self.on_process_files_button_click)
        
        # Contenedor Texto detalles de archivos
        self.files_abstract = QTextBrowser()
        self.files_abstract.setText("")
        self.files_abstract.setReadOnly(True)
        self.files_abstract.setTextInteractionFlags(Qt.TextBrowserInteraction) 
        self.files_abstract.anchorClicked.connect(self.show_error_details)
        self.files_abstract.setPlaceholderText("Seleccione los archivos y proceselos para ver la información.")
        self.files_abstract.setStyleSheet("""
            max-height: 300px;
        """)

        
        open_excel_button.setStyleSheet("background-color: #702525; color: #ffffff; padding: 10px, 10px, 10px, 10px; font-size: 16px;") 
        open_txt_button.setStyleSheet("background-color: #702525; color: #ffffff; padding: 10px, 10px, 10px, 10px; font-size: 16px;")
        self.txt_start_position_input.setStyleSheet("""
            background-color: #ffffff;
            color: #000000;
            padding: 5px;
            font-size: 16px                              
        """)
        self.txt_end_position_input.setStyleSheet("""
            background-color: #ffffff;
            color: #000000;
            padding: 5px;
            font-size: 16px 
        """)
        # Boton de guardar archivo
        save_file_button = QPushButton("Guardar") 
        save_file_button.setCursor(Qt.PointingHandCursor)
        save_file_button.setStyleSheet("""
            background-color: #ffffff;
            color: #000000;
            padding: 5px, 10px, 10px, 10px;
            font-size: 16px ;
            border-radius: 5px;
        """)
        save_file_button.setMinimumWidth(200)
        save_file_button.setMaximumWidth(200)
        save_file_button.clicked.connect(self.on_save_result_button_click)
        main_contaniner.addWidget(title)
        main_contaniner.addWidget(open_files_container)
        main_contaniner.addWidget(inputs_container)
        main_contaniner.addWidget(process_files_button)
        #main_contaniner.addStretch()
        main_contaniner.addWidget(self.files_abstract)
        #main_contaniner.addStretch()
        main_contaniner.addWidget(save_file_button, alignment=Qt.AlignCenter)
        #main_contaniner.addStretch()
        
        self.setLayout(main_contaniner)
        main_frame.layout().addWidget(self)
        
    ### Utils
    def update_start_position_txt(self, value):
        print(value)
        print(self.txt_start_position.get())
            
    def update_end_position_txt(self, value):
        print(value)
        print(self.txt_end_position["value"])
            
    def validate_position_txt(self, value):
        print(value)
        return value == "" or value.isdigit()
    
    def on_combobox_change(self, event):    
        print(self.columns_options.get())
              
    def verify_column_only_numbers(self):
        return re.match("^[0-9]+", self.columns_options.get())
    
    def on_open_excel_button_click(self):
        self.excel_details = self.controller.open_excel()
        if self.excel_details == None:
            return
        self.columns_select.addItems(self.excel_details['columns_list'])
        self.files_abstract_structure["excel_text"] = self.excel_details["files_abstract_text"]
        self.update_files_details_text()
        #self.update_files_details_text(self.excel_details["files_abstract_text"])
        
    def on_open_txt_button_click(self):
        self.txt_details = self.controller.open_txt()
        if self.txt_details == None:
            return
        self.files_abstract_structure["txt_text"] = self.txt_details["files_abstract_text"]
        self.update_files_details_text()
        #self.update_files_details_text(self.txt_details["files_abstract_text"])
        
    def on_process_files_button_click(self):
        if not self.excel_details:
            QMessageBox.warning(self, "Informacion", "No has seleccionado una Planilla Excel.")
            return
        if not self.txt_details:
            QMessageBox.warning(self, "Informacion", "No has seleccionado un Documento de Texto.")
            return
        if self.columns_select.currentText() == "Selecciona una columna":
            QMessageBox.warning(self, "Informacion", "Debes seleccionar una columna del Excel para analizar.")
            return
        if not self.txt_start_position_input.text():
            QMessageBox.warning(self, "Informacion", "Debes indicar la posicion de inicio para el Documento de texto.")
            return
        if not self.txt_end_position_input.text():
            QMessageBox.warning(self, "Informacion", "Debes indicar la posicion de fin para el Documento de texto.")
            return
        if int(self.txt_start_position_input.text()) > int(self.txt_end_position_input.text()):
            QMessageBox.warning(self, "Informacion", "La posición de inicio no puede ser mayor a la posicion de fin para analizar el documento de texto.")
            return
        
        self.process_result_details = self.controller.process_files()
        
        #self.files_abstract.append(f"Coincidencias encontradas: {self.process_result_details["coincidences"]}")
        #self.files_abstract.append(f"Errores encontrados en el Excel: {len(self.process_result_details["excel_wrong_data_rows"])}")
        #self.files_abstract.append(f"Errores encontrados en el Txt: {len(self.process_result_details["txt_wrong_data_rows"])}")
        # self.label_excel_wrong_data_rows = QLabel(
        #     f"Errores encontrados en el Excel: {len(self.process_result_details["excel_wrong_data_rows"])}  <a href='#'>Ver Detalles</a>"
        # )
        # self.label_excel_wrong_data_rows.setOpenExternalLinks(False)
        # self.label_excel_wrong_data_rows.setTextInteractionFlags(Qt.TextBrowserInteraction)
        # self.label_excel_wrong_data_rows.linkActivated.connect(self.show_excel_error_details)
        
        # self.label_txt_wrong_data_rows = QLabel(
        #     f"Errores encontrados en el Txt: {len(self.process_result_details["txt_wrong_data_rows"])}  <a href='#'>Ver Detalles</a>"
        # )
        # self.label_txt_wrong_data_rows.setOpenExternalLinks(False)
        # self.label_txt_wrong_data_rows.setTextInteractionFlags(Qt.TextBrowserInteraction)
        # self.label_txt_wrong_data_rows.linkActivated.connect(self.show_txt_error_details)
        
        self.files_abstract_structure["coincidences_found"] = f"Coincidencias encontradas: {self.process_result_details["coincidences"]}<br>"
        self.files_abstract_structure["excel_wrong_data_rows"] = f"Errores encontrados en el Excel: {len(self.process_result_details["excel_wrong_data_rows"])}  <a href='show_excel_errors_details'>Ver Detalles</a><br>"
        self.files_abstract_structure["txt_wrong_data_rows"] = f"Errores encontrados en el Txt: {len(self.process_result_details["txt_wrong_data_rows"])}  <a href='show_txt_errors_details'>Ver Detalles</a><br>"
        self.update_files_details_text()
        
        
    def update_files_details_text(self):
        self.files_abstract.setText("")
        text = ""
        for i in self.files_abstract_structure:
            print(self.files_abstract_structure[i])
            text += self.files_abstract_structure[i]
        self.files_abstract.setHtml(text)
        
    def on_save_result_button_click(self):
       self.controller.write_txt()
    
    
    def show_error_details(self, url):
        link = url.toString()
        if link == "show_excel_errors_details":
            self.show_excel_error_details() 
        elif link == "show_txt_errors_details":
            self.show_txt_error_details()
        
        #Update files and process details if not text is cleared
        self.update_files_details_text()
    
    def show_excel_error_details(self):
        self.errors_details_window = ErrorsDetailsView("Errores en el Excel", "Excel", self.process_result_details["excel_wrong_data_rows"])
        self.errors_details_window.exec()

    def show_txt_error_details(self):
        self.errors_details_window = ErrorsDetailsView("Errores en el Txt", "Txt", self.process_result_details["txt_wrong_data_rows"])
        self.errors_details_window.exec()