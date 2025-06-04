from datetime import datetime
from tkinter import filedialog, messagebox
import pandas as pd
import re
import os
from PySide6.QtWidgets import QFileDialog, QMessageBox
from views.loading_dialog_view import LoadingDialogView
from components.file_loader_thread import FileLoaderThread
from PySide6.QtCore import Signal, QObject

class ExcelAndTxtToTxtController(QObject):
    txt_loaded_signal = Signal(dict)
    excel_loaded_signal = Signal(dict)
    excel_df = pd.DataFrame()
    txt_data = None
    def __init__(self, view):
        
        super().__init__()
        self.view = view
        self.coincidences = {}
        self.process_result_info = {}
        
    def open_excel(self):
        excel_file, _ = QFileDialog.getOpenFileName(
        self.view,
        "Seleccionar archivo Excel",
        "",
        "Archivos de Excel (*.xlsx *.xls)"
        )
        
        if excel_file:
             # Control extension to limit type of file
            extension = os.path.splitext(excel_file)[1].lower()
            if extension not in [".xlsx", ".xls"]:
                QMessageBox.warning(self.view, "Archivo inválido", "Debe seleccionar una rchivo Excel (.xlsx o .xls)")
                return None
            # Read excel and set dataframe
            self.loading_dialog = LoadingDialogView(self.view)
            self.loading_dialog.show()
            self.loader_thread = FileLoaderThread(excel_file)
            self.loader_thread.finished.connect(self.on_excel_loaded)
            self.loader_thread.error.connect(self.on_excel_load_error)
            self.loading_dialog.rejected.connect(self.cancel_file_loading)
            self.loader_thread.start()
                   
    def open_txt(self):
        txt_file, _ = QFileDialog.getOpenFileName(
            self.view,
            "Seleccionar Archivo de Texto",
            "",
            "Archivo de Texto (*.txt)"
        )
        if txt_file:
            # Control extension to limit type of file
            extension = os.path.splitext(txt_file)[1].lower()
            if extension not in [".txt"]:
                QMessageBox.warning(self.view, "Archivo inválido", "Debe seleccionar una rchivo Excel (.xlsx o .xls)")
                return None
            print(f"Archivo: {txt_file}")
            
            # Read file
            self.loading_dialog = LoadingDialogView(self.view)
            self.loading_dialog.show()
            self.loader_thread = FileLoaderThread(txt_file)
            self.loader_thread.finished.connect(self.on_txt_loaded)
            self.loader_thread.error.connect(self.on_txt_load_error)
            self.loading_dialog.rejected.connect(self.cancel_file_loading)
            self.loader_thread.start()
        else:
            print("No se seleccionó ningun archivo.")
            return     
        
    def cancel_file_loading(self):
        if self.loader_thread and self.loader_thread.isRunning():
                self.loader_thread.terminate()
            
        if self.loading_dialog and self.loading_dialog.isVisible():
            self.loading_dialog.close()
         
    def on_txt_loaded(self, txt_loaded_info):
        print("Archivo TXT cargado correctamente.")

        self.txt_data = txt_loaded_info["txt_data"]
        self.txt_loaded_signal.emit(txt_loaded_info)
        self.loading_dialog.close()
        
    def on_txt_load_error(self, error_message):
        self.loading_dialog.close()
        QMessageBox.critical(self.view, "Error al cargar el archivo", error_message)
    
    def on_excel_loaded(self, excel_loaded_info):
        self.view.columns_select.clear()
        self.excel_df = excel_loaded_info["excel_df"]
        self.excel_loaded_signal.emit(excel_loaded_info)
        self.loading_dialog.close()
        
    
    def on_excel_load_error(self, error_message):
        self.loading_dialog.close()
        QMessageBox.critical(self.view, "Error al cargar el archivo", error_message)
    
    def process_files(self):
            # Get coincidences between excel and txt 
            # Verify if column selected from excel is numeric
            self.process_result_info["excel_wrong_data_rows"] = []
            self.process_result_info["txt_wrong_data_rows"] = []
            self.process_result_info["coincidences"] = []
            self.coincidences = {}
            for i, row in self.excel_df.iterrows():
                if not re.match("^[0-9]+$", row[self.view.columns_select.currentText()]):
                    self.process_result_info["excel_wrong_data_rows"].append({"msg": f"Fila {i+1}: El valor no es numérico.", "row": i+1})

            # Control lines in txt
            for i, line in enumerate(self.txt_data, start=0):
                if not re.match("^[0-9]+$", line[int(self.view.txt_start_position_input.text())-1:int(self.view.txt_end_position_input.text())]):
                    self.process_result_info["txt_wrong_data_rows"].append({"msg": f"Fila {i+1}: El valor entre las posiciones ingresadas ({self.view.txt_start_position_input.text()}, {self.view.txt_end_position_input.text()}) no es numérico.", "row": i+1})
            
            # Run through txt to compare with excel
            for row in self.txt_data:
                selected_column = self.view.columns_select.currentText()
                dni_txt = row[int(self.view.txt_start_position_input.text())-1:int(self.view.txt_end_position_input.text())]
                
                if dni_txt in self.excel_df[selected_column].astype(str).tolist():
                    if dni_txt not in self.coincidences:
                        self.coincidences[dni_txt] = row
                    #self.coincidences.append(row)
            
            # Set length coincidences
            self.process_result_info["coincidences"] = len(self.coincidences)
            return self.process_result_info
            
    def write_txt(self):
            # Save coincidences in new txt              
            save_path, _ = QFileDialog.getSaveFileName(
                self.view,
                "Guardar archivo",
                "",
                "Archivos de texto (*.txt);;Todos los archivos (*)"
            )
            
            if save_path:
                with open(save_path, 'w', encoding="utf-8", errors="ignore", newline="\n") as file:
                    #print(self.excel_df[self.coincidences][self.view.columns_options.get()].to_list())
                    for row in self.coincidences.values():
                        file.write(f"{row}")
            
            if save_path:
                os.startfile(save_path)