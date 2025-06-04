from datetime import datetime
from tkinter import filedialog, messagebox
import pandas as pd
import re
import os
from PySide6.QtWidgets import QFileDialog, QMessageBox

class ExcelAndTxtToTxtController():
    
    def __init__(self, view):
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
            self.excel_df = pd.read_excel(excel_file).astype(str)
            
            # Clear Combobox of columns when selecting new file
            self.view.columns_select.clear()
            
            ### Set columns as string because some data is saved using scientific notation
            # Fill Combobox with columns obtained from selected excel
            return {"files_abstract_text": f"""<p>Detalles del Excel Seleccionado:<br>
Nombre: {os.path.basename(excel_file)}<br>
Tamaño: {os.path.getsize(excel_file) / (1024 * 1024):.2f} MB<br>
Ultima modificación: {datetime.fromtimestamp(os.path.getmtime(excel_file)).strftime("%Y-%m-%D")}<br>
Total de registros: {len(self.excel_df)}</p>""", 
                    "columns_list": self.excel_df.columns.tolist()}
            
            
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
            with open(txt_file, "r", encoding="cp1252", newline="") as txt:
                self.txt_data = []
                self.txt_data = txt.readlines()
                self.txt_data = [line.replace("\r\n", "\n") for line in self.txt_data]
            return {"files_abstract_text": f"""<p>Detalles del Txt Seleccionado:<br>
Nombre: {os.path.basename(txt_file)}<br>
Tamaño: {os.path.getsize(txt_file) / (1024 * 1024):.2f} MB<br>
Ultima modificación: {datetime.fromtimestamp(os.path.getmtime(txt_file)).strftime("%Y-%m-%D")}<br>
Total de lineas: {len(self.txt_data)}</p>"""}
        else:
            print("No se seleccionó ningun archivo.")
            return     
            

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