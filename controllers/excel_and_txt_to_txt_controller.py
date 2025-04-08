from tkinter import filedialog, messagebox
import pandas as pd
import re
import os

class ExcelAndTxtToTxtController():
    
    def __init__(self, view):
        self.view = view
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
            return self.excel_df.columns.tolist()
            
            
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

    def process_files(self):
            # Obtener las coincidencias entre excel y txt por DNI
            # Verificar si en la columna de excel son numeros
            result_match_excel = self.excel_df[self.view.columns_options.get()].astype(str).str.match("^[0-9]+$")
            if (self.excel_df[~result_match_excel].shape[0] >= 1):
                messagebox.showwarning("Alerta", f"""En el archivo excel existen {self.excel_df[~result_match_excel].shape[0]} filas que en la columna {self.view.columns_options.get()} no contienen solo números!""")
            
            # Controlar las lineas en txt
            # Posibilidad de mejora: controlar al cargar el archivo en memoria para 
            # no volver a recorrerlo
            # el problema es que al cargar no tengo las posiciones aún
            for i, line in enumerate(self.txt_data, start=0):
                if not re.match("^[0-9]+$", line[int(self.view.txt_start_position.get())-1:int(self.view.txt_end_position.get())]):
                    self.view.txt_errors.append({"msg": f"Fila {i+1}: El valor entre las posiciones ingresadas ({self.view.txt_start_position.get()}, {self.view.txt_end_position.get()}) no es numérico.", "row": i+1})
            
            print(self.view.txt_errors)
            self.write_txt()
            
    def write_txt(self):
            # Agregar coincidencias al nuevo txt
            txt_data_between_entry_index = []
            for i in self.txt_data:
                txt_data_between_entry_index.append(i[int(self.view.txt_start_position.get())-1:int(self.view.txt_end_position.get())])
                
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Guardar archivo"
            )
            
            coincidences = self.excel_df[self.view.columns_options.get()].astype("str").isin(txt_data_between_entry_index)
            if save_path:
                with open(save_path, 'w', encoding="utf-8", errors="ignore", newline="\n") as file:
                    print(self.excel_df[coincidences][self.view.columns_options.get()].to_list())
                    for row in self.txt_data:
                        if row[int(self.view.txt_start_position.get())-1:int(self.view.txt_end_position.get())] in self.excel_df[coincidences][self.view.columns_options.get()].tolist(): 
                            file.write(f"{row}")
            
            if save_path:
                os.startfile(save_path)