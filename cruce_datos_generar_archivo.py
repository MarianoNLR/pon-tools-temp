import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pon_tools
import pandas as pd

class CruceDatosGenerarArchivo:
    ### Mostrar Frame de Opcion 1
    def __init__(self, main_frame):
        for frame in main_frame.winfo_children():
            frame.destroy()
        
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
        txt_start_position = tk.Entry(self.txt_controllers, validate="key", validatecommand=(self.validate_position_txt, '%P'))
        txt_end_position = tk.Entry(self.txt_controllers,  validate="key", validatecommand=(self.validate_position_txt, '%P'))
        
        txt_start_position.grid(row=1, column=0, sticky="n")
        txt_end_position.grid(row=1, column=0)
        
        self.columns_options = ttk.Combobox(self.excel_controllers, state="readonly")
        # columns_options.place(x=50, y=50)
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
        
    def validate_position_txt(self, value):
        if value == "" or value.isdigit():
            return True
        return False
        
    def on_open_excel_button_click(self):
        self.excel_file = filedialog.askopenfilename(title="Selecciona una archivo")
        if self.excel_file:
            print(f"Archivo: {self.excel_file}")
        else:
            print("No se seleccionó ningun archivo.")
        # Leer excel y cargar en data frame
        self.excel_df = pd.read_excel(self.excel_file)
        self.excel_df["DNI"] = self.excel_df["DNI"].astype(str)
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
        pon_tools.create_excel(self.excel_df, self.txt_data)