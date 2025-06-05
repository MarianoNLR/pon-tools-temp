from PySide6.QtCore import QThread, Signal
import os
from datetime import datetime
import pandas as pd
from components.file_type import FileType
import time

class FileLoaderThread(QThread):
    finished = Signal(dict)
    error = Signal(str)
   
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.resume = {}
        self.cancelled = False

    def cancel(self):
        self.cancelled = True
    
    def run(self):
        try:
            if self.cancelled:
                return
            
            file_type = FileType.get_file_extension(self.file_path)
            if file_type == FileType.TXT:
                self.read_txt_file()
            if file_type == FileType.EXCEL:
                self.read_excel_file()
            
            if not self.cancelled:
                self.finished.emit(self.resume)
        except Exception as e:
            if not self.cancelled:
                self.error.emit(f"Error al cargar el archivo: {str(e)}")
            
    # Reads text file and stores its content
    def read_txt_file(self):
        try:
            if self.cancelled:
                return
            with open(self.file_path, "r", encoding="utf-8", newline="") as txt:
                self.txt_data = []
                self.txt_data = txt.readlines()
                self.txt_data = [line.replace("\r\n", "\n") for line in self.txt_data]
                self.resume["files_abstract_text"] = f"""<p>Detalles del Txt Seleccionado:<br>
Nombre: {os.path.basename(self.file_path)}<br>
Tamaño: {os.path.getsize(self.file_path) / (1024 * 1024):.2f} MB<br>
Ultima modificación: {datetime.fromtimestamp(os.path.getmtime(self.file_path)).strftime("%Y-%m-%D")}<br>
Total de lineas: {len(self.txt_data)}</p>"""
            self.resume["txt_data"] = self.txt_data
        except Exception as e:
            if not self.cancelled:
                raise ValueError(f"Error al leer el archivo: {str(e)}")
    
    # Reads Excel file and stores its content
    def read_excel_file(self):
        try:
            self.excel_df = pd.read_excel(self.file_path).astype(str)
            self.resume["files_abstract_text"] = f"""<p>Detalles del Excel Seleccionado:<br>
Nombre: {os.path.basename(self.file_path)}<br>
Tamaño: {os.path.getsize(self.file_path) / (1024 * 1024):.2f} MB<br>
Ultima modificación: {datetime.fromtimestamp(os.path.getmtime(self.file_path)).strftime("%Y-%m-%D")}<br>
Total de lineas: {len(self.excel_df)}</p>"""
            self.resume["columns_list"] = self.excel_df.columns.tolist()
            self.resume["excel_df"] = self.excel_df
        except Exception as e:
            raise ValueError(f"Error al leer el archivo Excel: {str(e)}")