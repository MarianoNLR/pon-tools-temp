import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import openpyxl
import pandas as pd
import re
from error import Error
from tkinter import messagebox

class CruceDatosGenerarArchivo():
    ### Mostrar Frame de Opcion 1
    def __init__(self, main_frame):
        self.main_frame = main_frame
        for frame in main_frame.winfo_children():
            frame.destroy()
            
        # Variables para control de errores
        self.txt_errors = []
        self.excel_errors = []
        
        # Creacion de frames
        self.opcion1_frame = tk.Frame(main_frame, bg="#212121", height=300)
        self.opcion1_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configuracion de grid opcion 1
        self.opcion1_frame.grid_rowconfigure(0, weight=1)
        self.opcion1_frame.grid_rowconfigure(1, weight=1, minsize=300)
        self.opcion1_frame.grid_rowconfigure(2, weight=3)
        self.opcion1_frame.grid_columnconfigure(0, weight=1)
        self.opcion1_frame.grid_columnconfigure(1, weight=1)
        
        self.excel_controllers = tk.Frame(self.opcion1_frame, bg="#212121")
        self.excel_controllers.grid(row=1, column=0, sticky="nsew")
        
        self.excel_controllers.rowconfigure(0, weight=1)
        self.excel_controllers.rowconfigure(1, weight=1)
        self.excel_controllers.rowconfigure(2, weight=1)
        self.excel_controllers.columnconfigure(0, weight=1)
        
        self.txt_controllers = tk.Frame(self.opcion1_frame, bg="#212121")
        self.txt_controllers.grid(row=1, column=1, sticky="nsew")
        
        self.txt_controllers.rowconfigure(0, weight=1)
        self.txt_controllers.rowconfigure(1, weight=1)
        self.txt_controllers.rowconfigure(2, weight=1)
        self.txt_controllers.columnconfigure(0, weight=1)
        
        self.validate_position_txt = self.opcion1_frame.register(self.validate_position_txt)
        self.update_start_position_txt = self.opcion1_frame.register(self.update_start_position_txt)
        self.update_end_position_txt = self.opcion1_frame.register(self.update_end_position_txt)
        self.txt_start_position = tk.Entry(self.txt_controllers, validate="key", validatecommand=(self.validate_position_txt, '%P'))
        self.txt_end_position = tk.Entry(self.txt_controllers,  validate="key", validatecommand=(self.validate_position_txt, '%P'))

        self.txt_start_position.grid(row=1, column=0, sticky="n")
        self.txt_end_position.grid(row=1, column=0)
        
        self.columns_options = ttk.Combobox(self.excel_controllers, state="readonly")
        self.columns_options.bind("<<ComboboxSelected>>", self.on_combobox_change)
        
        self.columns_options.grid(row=1, column=0, sticky="n")
        
        ### Contenido principal frame opcion 1
        # Botones de seleccion de archivos
        open_excel_button = tk.Button(self.excel_controllers ,text="Seleccionar Excel", command=self.on_open_excel_button_click, relief="flat", bg="#eb2b2b", fg="white", height=3, font=("Arial", 12))
        open_txt_button = tk.Button(self.txt_controllers, text="Seleccionar Txt", command=self.on_open_txt_button_click, relief="flat", bg="#eb2b2b", fg="white", height=3, font=("Arial", 12))
        open_excel_button.grid(row=0, column=0, sticky="n")
        open_txt_button.grid(row=0, column=0, sticky="n")
        
        # Titulo del frame
        label = tk.Label(self.opcion1_frame, text="Bienvenido a la Opcion 1", wraplength=350, font=("Arial", 40), bg="#212121", fg="white")
        label.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        # Botón para procesar archivos
        process_files_button = tk.Button(self.opcion1_frame, text="Procesar archivos", command=self.on_process_files_button_click, relief="flat", bg="#ffffff", fg="#000000", height=3, font=("Arial", 12))
        process_files_button.grid(row=2, columnspan=2)
        
    def update_start_position_txt(self, value):
        print(value)
        print(self.txt_start_position.get())
        # if self.validate_position_txt(value):
        #     self.txt_start_position = value
        
    def update_end_position_txt(self, value):
        # if self.validate_position_txt(value):
        #     self.txt_end_position = value
        print(value)
        print(self.txt_end_position["value"])
        
    def validate_position_txt(self, value):
        print(value)
        return value == "" or value.isdigit()
        
    def on_open_excel_button_click(self):
        self.excel_file = filedialog.askopenfilename(title="Selecciona una archivo")
        if self.excel_file:
            print(f"Archivo: {self.excel_file}")
        else:
            print("No se seleccionó ningun archivo.")
            
        # Leer excel y cargar en data frame
        
        ### Cargo las columnas como String por el momento porque sino
        ### algunos datos se guardan con notación cientifica en el nuevo excel ###
        self.excel_df = pd.read_excel(self.excel_file).astype(str)
        #self.excel_df["DNI"] = self.excel_df["DNI"].astype(str)
        
        #Cargar combobox con columnas del excel seleccionado
        self.columns_options['values'] = self.excel_df.columns.tolist()
        
        
    def on_open_txt_button_click(self):
        self.txt_file = filedialog.askopenfilename(title="Selecciona una archivo")
        if self.txt_file:
            print(f"Archivo: {self.txt_file}")
        else:
            print("No se seleccionó ningun archivo.")
        # Leer txt y cargar en data frame
        with open(self.txt_file, "r") as txt:
            self.txt_data = []
            # Leer archivo de texto linea por linea
            for line in txt:
                self.txt_data.append(line.strip())

    def on_process_files_button_click(self):
        # Obtener las coincidencias entre excel y txt por DNI
        # Verificar si en la columna de excel son numeros
        result_match_excel = self.excel_df[self.columns_options.get()].astype(str).str.match("^[0-9]+$")
        if (self.excel_df[~result_match_excel].shape[0] >= 1):
            messagebox.showwarning("Alerta", f"""En el archivo excel existen {self.excel_df[~result_match_excel].shape[0]} filas que en la columna {self.columns_options.get()} no contienen solo números!""")
        
        # Controlar las lineas en txt
        # Posibilidad de mejora: controlar al cargar el archivo en memoria para 
        # no volver a recorrerlo
        # el problema es que al cargar no tengo las posiciones aún
        for i, line in enumerate(self.txt_data, start=0):
            line = line.strip()
            # line[int(self.txt_start_position.get())-1:int(self.txt_end_position.get())].str.match("^[0-9]+$")
            if not re.match("^[0-9]+$", line[int(self.txt_start_position.get())-1:int(self.txt_end_position.get())]):
                self.txt_errors.append({"msg": f"Fila {i+1}: El valor entre las posiciones ingresadas ({self.txt_start_position.get()}, {self.txt_end_position.get()}) no es numérico.", "row": i+1})
        
        print(self.txt_errors)
        
    def write_excel(self):
        #Crear libro de excel
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "Hoja"

        sheet.append(tuple(self.excel_df.columns))

        # Agregar coincidencias al nuevo excel
        txt_data_between_entry_index = []
        for i in self.txt_data:
            txt_data_between_entry_index.append(i[int(self.txt_start_position.get())-1:int(self.txt_end_position.get())])
        
        coincidences = [self.excel_df[self.columns_options.get()].astype("str").isin(txt_data_between_entry_index)]

        for item in self.excel_df[coincidences[0]].itertuples(index=False):
            print(item, type(item))
            sheet.append(tuple(item))
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Text files", "*.xlsx"), ("All files", "*.*")],
            title="Guardar archivo"
        )
        
        wb.save(file_path)
        
        if file_path:
            os.startfile(file_path)
        
    def on_combobox_change(self, event):    
        print(self.columns_options.get())
        
    
    def verify_column_only_numbers(self):
        return re.match("^[0-9]+", self.columns_options.get())