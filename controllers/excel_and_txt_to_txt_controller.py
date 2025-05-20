from datetime import datetime
from tkinter import filedialog, messagebox
import pandas as pd
import re
import os
from PySide6.QtWidgets import QFileDialog

class ExcelAndTxtToTxtController():
    
    def __init__(self, view):
        self.view = view
        self.coincidences = []
        self.process_result_info = {}
        
    def open_excel(self):
        excel_file, _ = QFileDialog.getOpenFileName(
        self.view,
        "Seleccionar archivo Excel",
        "",
        "Archivos de Excel (*.xlsx *.xls);;Todos los archivos (*)"
        )
        
        if excel_file:
            # Leer excel y cargar en data frame
            self.excel_df = pd.read_excel(excel_file).astype(str)
            
            # Limpio el combobox de columnas cuando se selecciona un nuevo archivo
            self.view.columns_select.clear()
            ### Cargo las columnas como String por el momento porque sino
            ### algunos datos se guardan con notación cientifica en el nuevo excel ###
            #Cargar combobox con columnas del excel seleccionado
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
            "Archivo de Texto (*.txt);;Todos los archivos (*)"
        )
        if txt_file:
            print(f"Archivo: {txt_file}")
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
            # Obtener las coincidencias entre excel y txt por DNI
            # Verificar si en la columna de excel son numeros
            self.process_result_info["excel_wrong_data_rows"] = []
            self.process_result_info["txt_wrong_data_rows"] = []
            self.process_result_info["coincidences"] = []
            self.coincidences = []
            for i, row in self.excel_df.iterrows():
                if not re.match("^[0-9]+$", row[self.view.columns_select.currentText()]):
                    self.process_result_info["excel_wrong_data_rows"].append({"msg": f"Fila {i+1}: El valor no es numérico.", "row": i+1})
   
            # Controlar las lineas en txt
            # Posibilidad de mejora: controlar al cargar el archivo en memoria para 
            # no volver a recorrerlo
            # el problema es que al cargar no tengo las posiciones aún
            for i, line in enumerate(self.txt_data, start=0):
                if not re.match("^[0-9]+$", line[int(self.view.txt_start_position_input.text())-1:int(self.view.txt_end_position_input.text())]):
                    self.process_result_info["txt_wrong_data_rows"].append({"msg": f"Fila {i+1}: El valor entre las posiciones ingresadas ({self.view.txt_start_position_input.text()}, {self.view.txt_end_position_input.text()}) no es numérico.", "row": i+1})
            
            # Recorrer txt y cada linea comparar con los dni del excel
            for row in self.txt_data:
                        if (row[int(self.view.txt_start_position_input.text())-1:int(self.view.txt_end_position_input.text())] 
                            in self.excel_df[self.view.columns_select.currentText()].astype(str).tolist()): 
                            
                            self.coincidences.append(row)
            
            # Seteo de objeto de errores para enviar a la vista
            self.process_result_info["coincidences"] = len(self.coincidences)
            return self.process_result_info
            
    def write_txt(self):
            # Agregar coincidencias al nuevo txt              
            save_path, _ = QFileDialog.getSaveFileName(
                self.view,
                "Guardar archivo",
                "",
                "Archivos de texto (*.txt);;Todos los archivos (*)"
            )
            
            if save_path:
                with open(save_path, 'w', encoding="utf-8", errors="ignore", newline="\n") as file:
                    #print(self.excel_df[self.coincidences][self.view.columns_options.get()].to_list())
                    for row in self.coincidences:
                        file.write(f"{row}")
            
            if save_path:
                os.startfile(save_path)