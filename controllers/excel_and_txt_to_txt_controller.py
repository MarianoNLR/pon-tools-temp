from datetime import datetime
import pandas as pd
import re
import os
from PySide6.QtWidgets import QFileDialog, QMessageBox
from views.loading_dialog_view import LoadingDialogView
from views.processing_dialog_view import ProcessingDialogView
from PySide6.QtCore import Signal, QObject
from controllers.task_manager import TaskManager

class ExcelAndTxtToTxtController(QObject):
    txt_loaded_signal = Signal(dict)
    excel_loaded_signal = Signal(dict)
    process_files_finished_signal = Signal(dict)
    excel_df = pd.DataFrame()
    txt_data = {}
    task_manager = TaskManager()
    def __init__(self, view):
        
        super().__init__()
        self.resume = {}
        self.view = view
        self.coincidences = {}
        self.process_result_info = {}
    
    # Using static method to avoid self and prevent issues if the instance is garbage collected during thread execution.
    @staticmethod
    def load_excel(excel_file):
        try:
            excel_df = pd.read_excel(excel_file).astype(str)
            excel_data = {}
            excel_data["df"] = excel_df
            excel_data["file_path"] = excel_file
            return excel_data
        except Exception as e:
            raise ValueError(f"Error al leer el archivo Excel: {str(e)}")
        
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
                QMessageBox.warning(self.view, "Archivo inválido", "Debe seleccionar un archivo Excel (.xlsx o .xls)")
                return None
            
            self.loading_dialog = LoadingDialogView(self.view)
            self.loading_dialog.show()
            
            self.task_manager.run_task(
                task_func = ExcelAndTxtToTxtController.load_excel,
                args = (excel_file,),
                on_result = self.on_excel_loaded,
                on_error = self.on_excel_load_error,
                on_finished = self.loading_dialog.close
            )
            # Read excel and set dataframe
            
            # self.start_task("load_excel", excel_file)

    # Using static method to avoid self and prevent issues if the instance is garbage collected during thread execution.
    @staticmethod
    def load_txt(file_path):
        try:
            with open(file_path, "r", encoding="utf-8", newline="") as txt:
                txt_data = {}
                lines = txt.readlines()
                txt_data["txt_data"] = [line.replace("\r\n", "\n") for line in lines]
                txt_data["file_path"] = file_path
                return txt_data
        except Exception as e:
            raise ValueError(f"Error al leer el archivo Txt: {str(e)}")
                   
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
                QMessageBox.warning(self.view, "Archivo inválido", "Debe seleccionar un archivo Excel (.xlsx o .xls)")
                return None
            
            # Read file
            self.loading_dialog = LoadingDialogView(self.view)
            self.loading_dialog.show()
            
            self.task_manager.run_task(
                task_func = ExcelAndTxtToTxtController.load_txt,
                args = (txt_file,),
                on_result = self.on_txt_loaded,
                on_error = self.on_txt_load_error,
                on_finished = self.loading_dialog.close
            )
        else:
            print("No se seleccionó ningun archivo.")
            return    
        
    def cancel_file_loading(self):
        if self.loader_thread and self.loader_thread.isRunning():
                self.loader_thread.terminate()
            
        if self.loading_dialog and self.loading_dialog.isVisible():
            self.loading_dialog.close()
         
    def on_txt_loaded(self, txt_loaded_info):
        file_path = txt_loaded_info["file_path"]
        self.txt_data["txt_data"] = txt_loaded_info["txt_data"]
        self.txt_data["resume"] = f"""<p>Detalles del Txt Seleccionado:<br>
Nombre: {os.path.basename(file_path)}<br>
Tamaño: {os.path.getsize(file_path) / (1024 * 1024):.2f} MB<br>
Ultima modificación: {datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%D")}<br>
Total de lineas: {len(self.txt_data["txt_data"])}</p>"""
        self.txt_loaded_signal.emit(self.txt_data)
        self.loading_dialog.close()
        
    def on_txt_load_error(self, error_message):
        self.loading_dialog.close()
        QMessageBox.critical(self.view, "Error al cargar el archivo", error_message)
    
    def on_excel_loaded(self, excel_data):
        excel_file = excel_data["file_path"]
        self.excel_df = excel_data["df"]
        #self.resume["files_abstract_text"] = excel_loaded_info["resume"]
        self.resume["resume"] = f"""
            <p>Detalles del Excel Seleccionado:<br>
            Nombre: {os.path.basename(excel_file)}<br>
            Tamaño: {os.path.getsize(excel_file) / (1024 * 1024):.2f} MB <br>
            Última modificación: {datetime.fromtimestamp(os.path.getmtime(excel_file)).strftime("%Y-%m-%d")}<br>
            Total de líneas: {len(self.excel_df)}</p>"""
        self.resume["columns_list"] = self.excel_df.columns.tolist()
        self.resume["excel_path"] = excel_data["file_path"]
        self.view.columns_select.clear()
        self.excel_loaded_signal.emit(self.resume)
        self.loading_dialog.close()
        
    
    def on_excel_load_error(self, error_message):
        self.loading_dialog.close()
        QMessageBox.critical(self.view, "Error al cargar el archivo", error_message)
    
    # Using static method to avoid self and prevent issues if the instance is garbage collected during thread execution.
    @staticmethod
    def process_files_on_thread(excel_df, txt_data, view):
        process_result_info = {}
        excel_df = excel_df
        txt_data = txt_data["txt_data"]
        process_result_info["excel_wrong_data_rows"] = []
        process_result_info["txt_wrong_data_rows"] = []
        process_result_info["coincidences"] = []
        coincidences = {}
        for i, row in excel_df.iterrows():
            if not re.match("^[0-9]+$", row[view.columns_select.currentText()]):
                process_result_info["excel_wrong_data_rows"].append({"msg": f"Fila {i+1}: El valor no es numérico.", "row": i+1})

        # Control lines in txt
        for i, line in enumerate(txt_data, start=0):
            if not re.match("^[0-9]+$", line[int(view.txt_start_position_input.text())-1:int(view.txt_end_position_input.text())]):
                process_result_info["txt_wrong_data_rows"].append({"msg": f"Fila {i+1}: El valor entre las posiciones ingresadas ({view.txt_start_position_input.text()}, {view.txt_end_position_input.text()}) no es numérico.", "row": i+1})
        
        # Run through txt to compare with excel
        for row in txt_data:
            selected_column = view.columns_select.currentText()
            txt_text = row[int(view.txt_start_position_input.text())-1:int(view.txt_end_position_input.text())]
            
            if txt_text in excel_df[selected_column].astype(str).tolist():
                if txt_text not in coincidences:
                    coincidences[txt_text] = row
                #self.coincidences.append(row)
        
        # Set length coincidences
        process_result_info["coincidences"] = coincidences
        return process_result_info

    def on_process_files_finished(self, process_result_info):
        self.process_result_info = process_result_info
        self.process_files_finished_signal.emit(process_result_info)
    
    def process_files(self):
            # Get coincidences between excel and txt 
            # Verify if column selected from excel is numeric
            try:
                self.processing_dialog = ProcessingDialogView(self.view)
                self.processing_dialog.show()
                self.task_manager.run_task(
                    task_func=ExcelAndTxtToTxtController.process_files_on_thread,
                    args=(self.excel_df, self.txt_data, self.view,),
                    on_result=self.on_process_files_finished,
                    on_error=None,
                    on_finished=self.processing_dialog.close
                )
            except Exception as e:
                QMessageBox.warning(self, "Error", "Ocurrió un error al procesar los archivos.")
                return
                
                   
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
                    for row in self.process_result_info["coincidences"].values():
                        file.write(f"{row}")
            
            if save_path:
                os.startfile(save_path)