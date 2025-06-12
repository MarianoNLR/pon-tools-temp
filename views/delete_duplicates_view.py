from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PySide6.QtCore import Qt
from controllers.delete_duplicates_controller import DeleteDuplicatesController
import pandas as pd
import os
from datetime import datetime

class DeleteDuplicateView(QWidget):
    def __init__(self, main_frame):
        super().__init__(main_frame)
        self.delete_duplicates_controller = DeleteDuplicatesController(self)
        self.delete_duplicates_controller.file_loaded_signal.connect(self.on_file_opened)
        self.delete_duplicates_controller.process_finished_signal.connect(self.on_process_finished)
        main_contaniner = QVBoxLayout()
        main_contaniner.setSpacing(10)
        main_contaniner.setContentsMargins(0,0,0,0)

        # Layout
        #layout = QVBoxLayout(self)

        # Label
        self.title = QLabel("Borrar duplicados", self)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        #layout.addWidget(self.title, alignment = Qt.AlignTop | Qt.AlignHCenter)
        
        # Select File Button
        self.file_details_layout = QVBoxLayout()
        self.file_details_container = QWidget(self)
        self.select_file_button = QPushButton("Seleccionar archivo", self)
        self.select_file_button.setStyleSheet("""
            QPushButton {
                font-size: 16px; 
                color: white; 
                background-color: #702525;
                padding: 5px, 10px, 10px, 10px;
            }
        """)
        # #layout.addWidget(self.select_file_button, alignment = Qt.AlignTop | Qt.AlignHCenter)
        self.select_file_button.clicked.connect(self.open_file)
        self.file_details_layout.addWidget(self.select_file_button, alignment = Qt.AlignHCenter)
        self.select_file_button.setCursor(Qt.PointingHandCursor)
        # # File Detailes title and details
        
        self.file_details_title = QLabel("Detalles del archivo", self)
        self.file_details_title.setStyleSheet("font-size: 18px; color: white; font-weight: bold;")
        self.file_details_layout.addWidget(self.file_details_title)
        
        self.file_details = QLabel("No se ha seleccionado ningún archivo.", self)
        self.file_details.setStyleSheet("font-size: 16px; color: white;")
        
        self.file_details_layout.addWidget(self.file_details)
        self.file_details_container.setLayout(self.file_details_layout)
        
        # File Process Button
        self.process_button = QPushButton("Procesar archivo", self)
        self.process_button.setStyleSheet(
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
        #layout.addWidget(self.process_button, alignment = Qt.AlignTop | Qt.AlignHCenter)
        self.process_button.clicked.connect(self.on_click_process_button)
        self.process_button.setDisabled(True)
        self.process_button.setCursor(Qt.PointingHandCursor)
        
        # # File Process Details
        self.process_details = QTextEdit("Detalles del proceso aparecerán aquí.", self)
        self.process_details.setDisabled(True)
        self.process_details.setStyleSheet(
            """
            QTextEdit {
                font-size: 16px; 
                max-height: 300px;
            }
            """)
        #layout.addWidget(self.process_details, alignment = Qt.AlignTop)
        
        # Save Result Button
        self.save_result_button = QPushButton("Guardar resultado", self)
        self.save_result_button.setStyleSheet(
            """
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
        #layout.addWidget(self.save_result_button, alignment = Qt.AlignTop | Qt.AlignHCenter)
        self.save_result_button.clicked.connect(self.on_save_result_button_clicked)
        self.process_button.setDisabled(True)
        self.save_result_button.setDisabled(True)
        self.save_result_button.setCursor(Qt.PointingHandCursor)
        
        # Set the layout for the widget
        
        #self.process_details.setFixedHeight(300)
        main_contaniner.addWidget(self.title, alignment=Qt.AlignCenter)
        main_contaniner.addWidget(self.select_file_button, alignment=Qt.AlignTop)
        main_contaniner.addWidget(self.file_details_container)
        main_contaniner.addStretch()
        main_contaniner.addWidget(self.process_button)
        main_contaniner.addWidget(self.process_details)
        main_contaniner.addWidget(self.save_result_button, alignment=Qt.AlignCenter)
        QWidget.setTabOrder(self.select_file_button, self.process_button)
        QWidget.setTabOrder(self.process_button, self.save_result_button)
        self.select_file_button.setAutoDefault(True)
        self.process_button.setAutoDefault(True)
        self.save_result_button.setAutoDefault(True)
        self.setLayout(main_contaniner)
        main_frame.layout().addWidget(self)
    
    def open_file(self):
        self.delete_duplicates_controller.open_file()
    
    def on_file_opened(self, file_data):
        if file_data is not None:
            self.update_file_details()
            self.process_button.setDisabled(False)
    
    def on_click_process_button(self):
        self.delete_duplicates_controller.process_file()
        
    
    def on_process_finished(self):
        self.process_details.setText(f"Registros duplicados encontrados: {self.delete_duplicates_controller.duplicates_removed}")
        if self.delete_duplicates_controller.file_data is not None:
            self.save_result_button.setDisabled(False)
    
    def update_file_details(self):
        file_path = self.delete_duplicates_controller.file_path
        file_data = self.delete_duplicates_controller.file_data["data"]
        self.file_details.setText(f"""Nombre del archivo: {os.path.basename(file_path)}\n
Tamaño: {os.path.getsize(file_path) / (1024 * 1024):.2f} MB\n
Ultima modificación: {datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%D")}\n
Total de lineas: {len(file_data)}""")
    
    def on_save_result_button_clicked(self):
        if self.delete_duplicates_controller.file_data is not None:
            self.delete_duplicates_controller.save_result()
        else:
            self.process_details.setText("No hay datos para guardar.")
        
        
        
    