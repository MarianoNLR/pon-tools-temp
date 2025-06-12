from PySide6.QtWidgets import QFileDialog, QMessageBox
from enum import Enum
import pandas as pd
import os
from controllers.task_manager import TaskManager
from views.loading_dialog_view import LoadingDialogView
from views.processing_dialog_view import ProcessingDialogView
from PySide6.QtCore import Signal, QObject

class SupportedFileTypes(Enum):
    XLSX = "xlsx",
    XLS = "xls",
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

class DeleteDuplicatesController(QObject):
    FILE_TYPE_SETTINGS = {
        SupportedFileTypes.TXT: {
            "default_name": "",
            "default_filter": "Archivos de texto (*.txt)",
            "extension": "txt"
        },
        SupportedFileTypes.XLSX: {
            "default_name": "",
            "default_filter": "Archivos Excel (*.xls, *.xlsx)",
            "extension": "xlsx"
        },
        SupportedFileTypes.XLS: {
            "default_name": "",
            "default_filter": "Archivos Excel (*.xls, *.xlsx)",
            "extension": "xls"
        }
    }
    
    file_loaded_signal = Signal(list)
    process_finished_signal = Signal(list)
    task_manager = TaskManager()
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.file_data = None
        self.file_path = None
        self.duplicates_removed = 0
        self.file_data_without_duplicates = None
    
    def open_file(self):
        extensions = SupportedFileTypes.get_supported_extensions()
        self.file_path, _ = QFileDialog.getOpenFileName(
        self.view,
        "Seleccionar archivo",
        "",
        f"Archivos Permitidos ({' '.join(f"*{ext}" for ext in extensions)})"
        )
        
        if not self.file_path:
            return None
        print("extensions: ", extensions)
        ext = self.file_path.split('.')[-1].lower()
        print("ext: ", ext in extensions)
        if ext not in extensions:
            QMessageBox.warning(self.view, "Archivo inválido", "Tipo de archivo no soportado.")
            return None
        loading_dialog = LoadingDialogView(self.view)
        loading_dialog.show()

        self.task_manager.run_task(
            task_func=DeleteDuplicatesController.read_file,
            args=(self.file_path,),
            on_result=self.file_loaded,
            on_error=None,
            on_finished=loading_dialog.close
        )
        
    # Using static method to avoid self and prevent issues if the instance is garbage collected during thread execution.
    @staticmethod
    def read_file(file_path):
        file_data = {}
        file_data["file_type"] = SupportedFileTypes.get_file_extension(file_path)
        if file_data["file_type"] == SupportedFileTypes.XLS or file_data["file_type"] == SupportedFileTypes.XLSX:
            file_data["data"] = pd.read_excel(file_path).astype(str)
        elif file_data["file_type"] == SupportedFileTypes.TXT:
            with open(file_path, "r", encoding="utf-8", newline="") as txt:
                file_data["data"] = txt.readlines()
                file_data["data"] = [line.replace("\r\n", "\n") for line in file_data["data"]]
                print(type(file_data))
        return file_data
                
    def file_loaded(self, file_data):
        self.file_data = file_data
        self.file_loaded_signal.emit(file_data)
        
    
    def process_file(self):
        if self.file_data is None:
            self.view.process_details.setText("No se ha cargado ningún archivo.")
            return
        
        processing_dialog = ProcessingDialogView(self.view)
        processing_dialog.show()
        self.task_manager.run_task(
            task_func=DeleteDuplicatesController.remove_duplicates,
            args=(self.file_data,),
            on_result=self.on_removed_duplicates,
            on_error=None,
            on_finished=processing_dialog.close
        )
        
    def on_load_file_error(self, error_message):
        self.loading_dialog.close()
        QMessageBox.critical(self.view, "Error al cargar el archivo", error_message)
        
    # Using static method to avoid self and prevent issues if the instance is garbage collected during thread execution. 
    @staticmethod
    def remove_duplicates(file_data):
        result = None
        if isinstance(file_data["data"], pd.DataFrame):
            # Process DataFrame to remove duplicates
            result["data"] = file_data["data"].drop_duplicates()
            duplicates_removed = len(file_data["data"]) - len(result)
            if not duplicates_removed:
                duplicates_removed = 0
            
        elif isinstance(file_data["data"], list):
            # Process list to remove duplicates
            # unique_lines = list(set(self.file_data))
            
            # this way if the order of lines must be the same
            result = {}
            result["data"] = {}
            for line in file_data["data"]:
                result["data"][line] = None
            #file_data["data"] = unique_lines
        if result is not None: 
            result["duplicates_removed"] = len(file_data["data"]) - len(result["data"])
        return result
    
    def on_removed_duplicates(self, file_data):
        self.file_data_without_duplicates = file_data["data"]
        self.duplicates_removed = file_data["duplicates_removed"]
        self.process_finished_signal.emit(self.file_data_without_duplicates)
    
    
    def save_result(self):
        # if self.file_data["file_type"] == SupportedFileTypes.EXCEL:
        #     default_filter = "Archivos Excel (*.xls, *.xlsx)"
        # elif self.file_data["file_type"] == SupportedFileTypes.TXT:
        #     default_filter = "Archivos de texto (*.txt)"
        # else:
        #     default_filter = "Todos los archivo (*)"
        file_type = self.file_data["file_type"]
        print(file_type)
        
        settings = self.FILE_TYPE_SETTINGS.get(file_type)
        print(settings)
        save_path, _ = QFileDialog.getSaveFileName(
                self.view,
                "Guardar archivo",
                "",
                "Archivos de texto (*.txt);; Archivos Excel (*.xls, *.xlsx);;Todos los archivos (*)",
                settings["default_filter"]
            )
        
        if save_path:
            if self.file_data["file_type"] == SupportedFileTypes.XLS or self.file_data["file_type"] == SupportedFileTypes.XLSX:
                self.file_data_without_duplicates.to_excel(save_path, index=False)
            elif self.file_data["file_type"] == SupportedFileTypes.TXT:
                with open(save_path, "w", encoding="utf-8", newline="\n") as file:
                    for line in self.file_data_without_duplicates:
                        file.write(f"{line}")
            else:
                QMessageBox.warning("Error al guardar el archivo.", "El tipo de archivo destino no está soportado.")
                return
        
        if save_path:
            os.startfile(save_path)