import tkinter as tk
from tkinter import ttk
from controllers.excel_and_txt_to_txt_controller import ExcelAndTxtToTxtController
import tkintertools as tkt
import customtkinter as ctk
import re
from tkinter import messagebox
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QTextEdit, QHBoxLayout, QComboBox, QLabel, QMessageBox, QTextBrowser
from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QTextCursor
from PySide6.QtGui import QIntValidator
from views.errors_details_view import ErrorsDetailsView


class ExcelAndTxtToTxtView(QWidget):
    """
    Cross data operation view
    This view contains all widgets needed to execute cross data operation.
    It uses ExcelAndTxtToTxtController to perform several processes.
    """
    def __init__(self, main_frame):
        super().__init__(main_frame)
        
        self.controller = ExcelAndTxtToTxtController(self)
        self.controller.txt_loaded_signal.connect(self.on_txt_loaded)
        self.controller.excel_loaded_signal.connect(self.on_excel_loaded)
        self.controller.process_files_finished_signal.connect(self.on_process_files_finished)
        self.controller.analyze_files_finished_signal.connect(self.on_analyze_files_finished)
        self.excel_details = None
        self.txt_details = None
        # Variables for error control
        self.process_result_details = {}
        self.files_abstract_structure = {}
        self.analysis_result_details = {}
        self.files_abstract_structure["excel_text"] = ""
        self.files_abstract_structure["txt_text"] = ""
        self.files_abstract_structure["excel_wrong_data_rows"] = ""
        self.files_abstract_structure["txt_wrong_data_rows"] = ""
        #Setting ID to use in styles
        self.setObjectName("ExcelAndTxtToTxtView")

        self.setStyleSheet("""
            #ExcelAndTxtToTxtView {
                background-color: 'red'
            }
        """)
        
        #Main container Layout
        main_contaniner = QVBoxLayout()
        main_contaniner.setSpacing(10)
        main_contaniner.setContentsMargins(0,0,0,0)
        
        #Title
        title = QLabel("Cruce de Datos Excel - Txt y Generación de Txt")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        
        # Open files button section
        open_files_layout = QHBoxLayout()
        open_files_container = QWidget(self)
        open_excel_button = QPushButton("Abrir Excel") 
        open_excel_button.setAutoDefault(True)
        open_txt_button =  QPushButton("Abrir Txt")
        open_txt_button.setAutoDefault(True)
        open_files_layout.addWidget(open_excel_button)
        open_files_layout.addWidget(open_txt_button)
        open_files_container.setLayout(open_files_layout)
        open_excel_button.setCursor(Qt.PointingHandCursor)
        open_txt_button.setCursor(Qt.PointingHandCursor)
        
        # region Inputs Section
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
        self.columns_select.currentTextChanged.connect(self.on_combo_box_changed)
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
        
        self.txt_start_position_input.textChanged.connect(self.on_position_input_changed)
        
        
        position_inputs_layout.addWidget(txt_start_position_container)
        position_inputs_layout.addWidget(txt_end_position_container)
        position_inputs_container.setLayout(position_inputs_layout)
        position_inputs_layout.setSpacing(20)
        
        inputs_layout.addWidget(columns_options_container, 0, 0, alignment=Qt.AlignTop)
        inputs_layout.addWidget(position_inputs_container, 0, 1)
        inputs_layout.setColumnStretch(0, 1)
        inputs_layout.setColumnStretch(1, 1)
        inputs_container.setLayout(inputs_layout)
        #endregion
        
        # Process Files Button Section
        self.process_files_button = QPushButton("Procesar archivos")
        self.process_files_button.setAutoDefault(True)
        self.process_files_button.setStyleSheet("""
            background-color: #702525;
            color: #ffffff;
            padding: 5px, 10px, 10px, 10px;
            font-size: 16px 
        """)
        self.process_files_button.setCursor(Qt.PointingHandCursor)
        self.process_files_button.clicked.connect(self.on_process_files_button_click)
        self.process_files_button.setDisabled(True)
        self.process_files_button.setStyleSheet(
            """
            QPushButton {
                font-size: 16px; 
                color: white; 
                background-color: #702525;
                padding: 5px, 10px, 10px, 10px; 
            }
            
            QPushButton:disabled {
                background-color: #c16666;
                color: black;
            }
            """)
        
                # Process Files Button Section
        self.analyze_files_button = QPushButton("Analizar archivos")
        self.analyze_files_button.setAutoDefault(True)
        self.analyze_files_button.setStyleSheet("""
            background-color: #702525;
            color: #ffffff;
            padding: 5px, 10px, 10px, 10px;
            font-size: 16px 
        """)
        self.analyze_files_button.setCursor(Qt.PointingHandCursor)
        self.analyze_files_button.clicked.connect(self.on_analyze_files_button_click)
        self.analyze_files_button.setDisabled(True)
        self.analyze_files_button.setStyleSheet(
            """
            QPushButton {
                font-size: 16px; 
                color: white; 
                background-color: #702525;
                padding: 5px, 10px, 10px, 10px; 
            }
            
            QPushButton:disabled {
                background-color: #c16666;
                color: black;
            }
            """)
        
        #Container Details Files Analysis Text
        self.analysis_result_text_browser = QTextBrowser()
        self.analysis_result_text_browser.setText("")
        self.analysis_result_text_browser.setReadOnly(True)
        self.analysis_result_text_browser.setTextInteractionFlags(Qt.TextBrowserInteraction) 
        self.analysis_result_text_browser.anchorClicked.connect(self.show_error_details)
        self.analysis_result_text_browser.setPlaceholderText("Aqui se mostraran los datos de los archvos")
        self.analysis_result_text_browser.setStyleSheet("""
            min-height: 150px;
            max-height: 300px;
        """)

        #Container Details Files Text
        self.files_abstract = QLabel()
        self.files_abstract.setText("Coincidencias encontradas: ")
        #self.files_abstract.setReadOnly(True)
        #self.files_abstract.setTextInteractionFlags(Qt.TextBrowserInteraction) 
        #self.files_abstract.anchorClicked.connect(self.show_error_details)
        #self.files_abstract.setPlaceholderText("Procese los archivos para ver información.")
        self.files_abstract.setStyleSheet("""
            min-height: 50px;
            max-height: 300px;
            font-size: 24px;
            color: white;
        """)

        # Open Files Button Styles
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
        
        # Save Result in File Button
        self.save_file_button = QPushButton("Guardar") 
        self.save_file_button.setAutoDefault(True)
        self.save_file_button.setCursor(Qt.PointingHandCursor)
        #self.save_file_button.setDisabled(True)
        
        self.save_file_button.setStyleSheet("""
            QPushButton {
                font-size: 16px; 
                color: #000000; 
                background-color: #ffffff;
                padding: 5px, 10px, 10px, 10px;
                width: 200px;
                border-radius: 5px;       
                }
            
            QPushButton:disabled {
                background-color: #918e8e;
                color: #f2f2f2;
            }
            """)
        self.save_file_button.setMinimumWidth(200)
        self.save_file_button.setMaximumWidth(200)
        self.save_file_button.clicked.connect(self.on_save_result_button_click)
        main_contaniner.addWidget(title)
        main_contaniner.addWidget(open_files_container)
        main_contaniner.addWidget(inputs_container)
        #main_contaniner.addStretch()
        main_contaniner.addWidget(self.analyze_files_button)
        main_contaniner.addWidget(self.analysis_result_text_browser)
        main_contaniner.addWidget(self.process_files_button)
        main_contaniner.addWidget(self.files_abstract, alignment=Qt.AlignCenter)
        #main_contaniner.addStretch()
        main_contaniner.addWidget(self.save_file_button, alignment=Qt.AlignCenter)
        #main_contaniner.addStretch()
        
        self.setLayout(main_contaniner)
        QWidget.setTabOrder(self.columns_select, open_txt_button)
        QWidget.setTabOrder(open_txt_button, self.txt_start_position_input)
        QWidget.setTabOrder(self.txt_start_position_input, self.txt_end_position_input)
        QWidget.setTabOrder(self.txt_end_position_input, self.process_files_button)
        QWidget.setTabOrder(self.process_files_button, self.save_file_button)
        main_frame.layout().addWidget(self)
        
    ### Utils       
    def verify_column_only_numbers(self):
        return re.match("^[0-9]+", self.columns_options.get())
    
    def on_open_excel_button_click(self):
        self.controller.open_excel()
        
    def on_open_txt_button_click(self):
        self.controller.open_txt()
    
    def on_excel_loaded(self, excel_loaded_info):
        if excel_loaded_info is None:
            QMessageBox.warning(self, "Informacion", "No se pudo cargar el archivo de Excel.")
            return
        self.excel_details = excel_loaded_info["resume"]
        self.files_abstract_structure["excel_text"] = excel_loaded_info["resume"]
        
        self.columns_select.addItems(excel_loaded_info["columns_list"])
        
        self.save_file_button.setDisabled(True)
        self.process_files_button.setDisabled(True)
        self.files_abstract.setText("Coincidencias encontradas: ")
        self.analysis_result_details = {}
        self.files_abstract_structure["excel_wrong_data_rows"] = ""
        self.files_abstract_structure["txt_wrong_data_rows"] = ""
        self.update_files_details_text()
        #self.check_if_save_button_available()
        self.check_if_analyze_button_available()
        self.analysis_result_text_browser.moveCursor(QTextCursor.End)
        
    def on_txt_loaded(self, txt_loaded_info):
        
        if txt_loaded_info is None:
            QMessageBox.warning(self, "Informacion", "No se pudo cargar el archivo de texto.")
            return
        self.txt_details = txt_loaded_info["resume"]
        self.files_abstract_structure["txt_text"] = self.txt_details

        self.save_file_button.setDisabled(True)
        self.process_files_button.setDisabled(True)
        self.files_abstract.setText("Coincidencias encontradas: ")
        self.analysis_result_details = {}
        self.files_abstract_structure["excel_wrong_data_rows"] = ""
        self.files_abstract_structure["txt_wrong_data_rows"] = ""
        self.update_files_details_text()
        #self.update_files_details_text(txt_loaded_info["files_abstract_text"])
        #self.check_if_save_button_available()
        self.check_if_analyze_button_available()
        self.analysis_result_text_browser.moveCursor(QTextCursor.End)
        
    def on_analyze_files_button_click(self):
        # TODO Analyze files turn on process files button
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
        self.files_abstract.setText("Coincidencias encontradas: ")
        self.save_file_button.setDisabled(True)
        self.controller.analyze_files()
    
    def on_analyze_files_finished(self, analyze_result_info):
        self.process_files_button.setDisabled(False)
        self.analysis_result_details["excel_wrong_data_rows"] = analyze_result_info["excel_wrong_data_rows"]
        self.analysis_result_details["txt_wrong_data_rows"] = analyze_result_info["txt_wrong_data_rows"]
        self.files_abstract_structure["excel_wrong_data_rows"] = f"Errores encontrados en el Excel: {len(analyze_result_info["excel_wrong_data_rows"])}  <a href='show_excel_errors_details'>Ver Detalles</a><br>"
        self.files_abstract_structure["txt_wrong_data_rows"] = f"Errores encontrados en el Txt: {len(analyze_result_info["txt_wrong_data_rows"])}  <a href='show_txt_errors_details'>Ver Detalles</a><br>"
        self.update_files_details_text()
        self.analysis_result_text_browser.moveCursor(QTextCursor.End)

    def on_process_files_button_click(self):
        # Alerts 
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
        
        self.controller.process_files()
    
    def on_process_files_finished(self, process_result_info):
        if process_result_info is not None:
            self.save_file_button.setDisabled(False)
        self.process_result_details = process_result_info
        # Set Process Files Text
        #self.files_abstract_structure["coincidences_found"] = f"Coincidencias encontradas: {len(self.process_result_details["coincidences"])}<br>"
        # self.files_abstract_structure["excel_wrong_data_rows"] = f"Errores encontrados en el Excel: {len(self.process_result_details["excel_wrong_data_rows"])}  <a href='show_excel_errors_details'>Ver Detalles</a><br>"
        # self.files_abstract_structure["txt_wrong_data_rows"] = f"Errores encontrados en el Txt: {len(self.process_result_details["txt_wrong_data_rows"])}  <a href='show_txt_errors_details'>Ver Detalles</a><br>"
        #self.update_files_details_text()
        self.files_abstract.setText(f"Coincidencias encontradas: {len(process_result_info["coincidences"])}")
        #self.files_abstract.setHtml(f"Coincidencias encontradas: {len(process_result_info["coincidences"])}")
        
        
        
    def update_files_details_text(self):
        self.analysis_result_text_browser.setText("")
        text = ""
        text += self.files_abstract_structure["excel_text"]
        text += self.files_abstract_structure["txt_text"]
        text += self.files_abstract_structure["excel_wrong_data_rows"]
        text += self.files_abstract_structure["txt_wrong_data_rows"]
        self.analysis_result_text_browser.setHtml(text)
        # for i in self.files_abstract_structure:
        #     text += self.files_abstract_structure[i]
        # self.analysis_result_text_browser.setHtml(text)
        
    def on_save_result_button_click(self):
        if not self.process_result_details:
            return
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
        self.errors_details_window = ErrorsDetailsView("Errores en el Excel", "Excel", self.analysis_result_details["excel_wrong_data_rows"])
        self.errors_details_window.exec()
        self.analysis_result_text_browser.moveCursor(QTextCursor.End)

    def show_txt_error_details(self):
        self.errors_details_window = ErrorsDetailsView("Errores en el Txt", "Txt", self.analysis_result_details["txt_wrong_data_rows"])
        self.errors_details_window.exec()
        self.analysis_result_text_browser.moveCursor(QTextCursor.End)
    
    # def check_if_save_button_available(self):
    #     if self.excel_details and self.txt_details:
    #         self.process_files_button.setDisabled(False)
            
    def check_if_analyze_button_available(self):
        if self.excel_details and self.txt_details:
            self.analyze_files_button.setDisabled(False)
    
    def on_position_input_changed(self):
        self.save_file_button.setDisabled(True)
        self.process_files_button.setDisabled(True)
    
    def on_combo_box_changed(self):
        self.save_file_button.setDisabled(True)
        self.process_files_button.setDisabled(True)