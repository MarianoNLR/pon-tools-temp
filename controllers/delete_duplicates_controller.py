from PySide6.QtWidgets import QFileDialog
from enum import Enum
import pandas as pd
import os

class SupportedFileTypes(Enum):
    EXCEL = ("xlsx", "xls")
    TXT = "txt",
    
    def get_supported_extensions():
        extensions = []
        
        for ext in SupportedFileTypes:
           extensions.extend(ext.value)
           
        return extensions

    def get_file_extension(file_path):
        ext = file_path.split('.')[-1].lower()
        for file_type in SupportedFileTypes:
            if ext in file_type.value:
                return file_type
        else:
            raise ValueError("Tipo de archivo no soportado.")

class DeleteDuplicatesController:
    def __init__(self, view):
        self.view = view
        self.file_data = None
        self.file_path = None
        self.duplicates_removed = 0
    
    def read_file(self):
        extensions = SupportedFileTypes.get_supported_extensions()
        self.file_path, _ = QFileDialog.getOpenFileName(
        self.view,
        "Seleccionar archivo Excel",
        "",
        f"Archivos Permitidos ({' '.join(f"*{ext}" for ext in extensions)})"
        )
        
        if not self.file_path:
            return None
        
        self.file_type = SupportedFileTypes.get_file_extension(self.file_path)
        if self.file_type == SupportedFileTypes.EXCEL:
            self.file_data = pd.read_excel(self.file_path).astype(str)
        elif self.file_type == SupportedFileTypes.TXT:
            with open(self.file_path, "r", encoding="utf-8", newline="") as txt:
                self.file_data = txt.readlines()
                self.file_data = [line.replace("\r\n", "\n") for line in self.file_data]
                
    
    def process_file(self):
        if self.file_data is None:
            self.view.process_details.setText("No se ha cargado ningún archivo.")
            return

        self.remove_duplicates()
        
    
    def remove_duplicates(self):
        if isinstance(self.file_data, pd.DataFrame):
            # Process DataFrame to remove duplicates
            df_filtered = self.file_data.drop_duplicates()
            self.duplicates_removed = len(self.file_data) - len(df_filtered)
            if not self.duplicates_removed:
                self.duplicates_removed = 0
            
        elif isinstance(self.file_data, list):
            # Process list to remove duplicates
            # unique_lines = list(set(self.file_data))
            
            # this way if the order of lines must be the same
            unique_lines = {}
            for line in self.file_data:
                unique_lines[line] = None
            self.duplicates_removed = len(self.file_data) - len(unique_lines)
            self.file_data = unique_lines
            
    
    def save_result(self):
        save_path, _ = QFileDialog.getSaveFileName(
                self.view,
                "Guardar archivo",
                "",
                "Archivos de texto (*.txt, *.xls, *.xlsx);;Todos los archivos (*)"
            )
        
        if save_path:
            if self.file_type == SupportedFileTypes.EXCEL:
                self.file_data.to_excel(save_path, index=False)
            elif self.file_type == SupportedFileTypes.TXT:
                with open(save_path, "w", encoding="utf-8", newline="\n") as file:
                    for line in self.file_data:
                        file.write(f"{line}")
        
        if save_path:
            os.startfile(save_path)