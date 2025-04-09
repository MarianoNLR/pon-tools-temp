from datetime import datetime
from tkinter import filedialog, messagebox
import pandas as pd
import re
import os

class ExcelAndTxtToTxtController():
    
    def __init__(self, view):
        self.view = view
        self.coincidences = []
        self.process_result_info = {}
        pass
        
    def open_excel(self):
            self.excel_file = filedialog.askopenfilename(title="Selecciona una archivo")
            if self.excel_file:
                print(f"Archivo: {self.excel_file}")
            else:
                print("No se seleccionó ningun archivo.")
                
            # Leer excel y cargar en data frame
            
            ### Cargo las columnas como String por el momento porque sino
            ### algunos datos se guardan con notación cientifica en el nuevo excel ###
            self.excel_df = pd.read_excel(self.excel_file).astype(str)
            #Cargar combobox con columnas del excel seleccionado
            return {"files_abstract_text": f"""Detalles del Excel Seleccionado:\r
Nombre: {os.path.basename(self.excel_file)}\r
Tamaño: {os.path.getsize(self.excel_file) / (1024 * 1024):.2f} MB\r
Ultima modificación: {datetime.fromtimestamp(os.path.getmtime(self.excel_file)).strftime("%Y-%m-%D")}\r
Total de registros: {len(self.excel_df)}\n\n""", 
                    "columns_list": self.excel_df.columns.tolist()}
            
            
    def open_txt(self):
        self.txt_file = filedialog.askopenfilename(title="Selecciona una archivo")
        if self.txt_file:
            print(f"Archivo: {self.txt_file}")
        else:
            print("No se seleccionó ningun archivo.")
        # Leer txt y cargar en data frame
        with open(self.txt_file, "r", encoding="cp1252", newline="") as txt:
            self.txt_data = []
            self.txt_data = txt.readlines()
            self.txt_data = [line.replace("\r\n", "\n") for line in self.txt_data]
        return {"files_abstract_text": f"""Detalles del Txt Seleccionado:\r
Nombre: {os.path.basename(self.txt_file)}\r
Tamaño: {os.path.getsize(self.txt_file) / (1024 * 1024):.2f} MB\r
Ultima modificación: {datetime.fromtimestamp(os.path.getmtime(self.txt_file)).strftime("%Y-%m-%D")}\r
Total de lineas: {len(self.txt_data)}\n\n"""}
            

    def process_files(self):
            txt_data_between_entry_index = []
            # Obtener las coincidencias entre excel y txt por DNI
            # Verificar si en la columna de excel son numeros
            self.process_result_info["excel_wrong_data_rows"] = []
            self.process_result_info["txt_wrong_data_rows"] = []
            self.process_result_info["coincidences"] = []
            for i, row in self.excel_df.iterrows():
                if not re.match("^[0-9]+$", row[self.view.columns_options.get()]):
                    self.process_result_info["excel_wrong_data_rows"].append({"msg": f"Fila {i+1}: El valor no es numérico.", "row": i+1})
   
            # Controlar las lineas en txt
            # Posibilidad de mejora: controlar al cargar el archivo en memoria para 
            # no volver a recorrerlo
            # el problema es que al cargar no tengo las posiciones aún
            for i, line in enumerate(self.txt_data, start=0):
                if not re.match("^[0-9]+$", line[int(self.view.txt_start_position.get())-1:int(self.view.txt_end_position.get())]):
                    self.process_result_info["txt_wrong_data_rows"].append({"msg": f"Fila {i+1}: El valor entre las posiciones ingresadas ({self.view.txt_start_position.get()}, {self.view.txt_end_position.get()}) no es numérico.", "row": i+1})
            
            # Recorrer txt y cada linea comparar con los dni del excel
            for row in self.txt_data:
                        if (row[int(self.view.txt_start_position.get())-1:int(self.view.txt_end_position.get())] 
                            in self.excel_df[self.view.columns_options.get()].astype(str).tolist()): 
                            
                            self.coincidences.append(row)
            
            # Seteo de objeto de errores para enviar a la vista
            self.process_result_info["coincidences"] = len(self.coincidences)
            return self.process_result_info
            
    def write_txt(self):
            # Agregar coincidencias al nuevo txt              
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Guardar archivo"
            )
            
            if save_path:
                with open(save_path, 'w', encoding="utf-8", errors="ignore", newline="\n") as file:
                    #print(self.excel_df[self.coincidences][self.view.columns_options.get()].to_list())
                    for row in self.coincidences:
                        file.write(f"{row}")
            
            if save_path:
                os.startfile(save_path)