import tkinter as tk
from tkinter import ttk
from controllers.excel_and_txt_to_txt_controller import ExcelAndTxtToTxtController
import tkintertools as tkt
import customtkinter as ctk
import re
from tkinter import messagebox


class ExcelAndTxtToTxtView():
    ### Mostrar Frame de ExcelAndTxtToTxtView
    def __init__(self, main_frame):
        self.main_frame = main_frame
        for frame in main_frame.winfo_children():
            frame.destroy()
        
        self.controller = ExcelAndTxtToTxtController(self)
        self.excel_details = None
        self.txt_details = None
        # Variables para control de errores
        self.process_result_details = {}
        
        # Creacion de frames
        self.cruce_datos_generar_archivo_frame = tk.Frame(main_frame, bg="#212121", height=300)
        self.cruce_datos_generar_archivo_frame.grid(row=0, column=0, sticky="nsew")
        
        # Titulo del frame
        label = tk.Label(self.cruce_datos_generar_archivo_frame, text="Cruce de Datos Excel - Txt y Generación de Txt", wraplength=500, font=("Arial", 40), bg="#212121", fg="white")
        label.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        #### Configuracion de grid ExcelAndTxtToTxtView
        self.cruce_datos_generar_archivo_frame.grid_rowconfigure(0, weight=1)
        self.cruce_datos_generar_archivo_frame.grid_rowconfigure(1, weight=1, minsize=300)
        self.cruce_datos_generar_archivo_frame.grid_rowconfigure(2, weight=3)
        self.cruce_datos_generar_archivo_frame.grid_rowconfigure(3, weight=3, minsize=300)
        self.cruce_datos_generar_archivo_frame.grid_rowconfigure(4, weight=1, minsize=100)
        self.cruce_datos_generar_archivo_frame.grid_columnconfigure(0, weight=1)
        self.cruce_datos_generar_archivo_frame.grid_columnconfigure(1, weight=1)
        
        # Seccion Excel
        self.excel_controllers = tk.Frame(self.cruce_datos_generar_archivo_frame, bg="#212121")
        self.excel_controllers.grid(row=1, column=0, sticky="nsew")
        
        self.excel_controllers.rowconfigure(0, weight=1)
        self.excel_controllers.rowconfigure(1, weight=1)
        self.excel_controllers.rowconfigure(2, weight=1)
        self.excel_controllers.rowconfigure(3, weight=1)
        self.excel_controllers.rowconfigure(4, weight=1)
        self.excel_controllers.columnconfigure(0, weight=1)
        
        open_excel_button = tk.Button(self.excel_controllers ,text="Seleccionar Excel", command=self.on_open_excel_button_click, relief="flat", bg="#eb2b2b", fg="white", height=3, font=("Arial", 12))
        
        self.columns_options_label =tk.Label(self.excel_controllers, text="Columnas: ", fg="white", bg="#212121", font=("Arial", 15))
        self.columns_options = ttk.Combobox(self.excel_controllers, state="readonly")
        self.columns_options.set("Selecciona una columna")
        self.columns_options.bind("<<ComboboxSelected>>", self.on_combobox_change)
        self.columns_options_label.grid(row=1, column=0, sticky="s")
        self.columns_options.grid(row=2, column=0, sticky="n")
        
        # Seccion Txt
        self.txt_controllers = tk.Frame(self.cruce_datos_generar_archivo_frame, bg="#212121")
        self.txt_controllers.grid(row=1, column=1, sticky="nsew")
        open_excel_button.grid(row=0, column=0, sticky="n")
        
        self.txt_controllers.rowconfigure(0, weight=1)
        self.txt_controllers.rowconfigure(1, weight=1)
        self.txt_controllers.rowconfigure(2, weight=1)
        self.txt_controllers.rowconfigure(3, weight=1)
        self.txt_controllers.rowconfigure(4, weight=1)
        self.txt_controllers.rowconfigure(5, weight=1)
        self.txt_controllers.columnconfigure(0, weight=1)
        
        self.validate_position_txt = self.cruce_datos_generar_archivo_frame.register(self.validate_position_txt)
        # self.update_start_position_txt = self.cruce_datos_generar_archivo_frame.register(self.update_start_position_txt)
        # self.update_end_position_txt = self.cruce_datos_generar_archivo_frame.register(self.update_end_position_txt)
        self.txt_start_position = tk.Entry(self.txt_controllers, validate="key", validatecommand=(self.validate_position_txt, '%P'))
        self.txt_end_position = tk.Entry(self.txt_controllers,  validate="key", validatecommand=(self.validate_position_txt, '%P'))

        self.txt_start_position_label = tk.Label(self.txt_controllers, text="Posición inicio: ", fg="white", bg="#212121", font=("Arial", 15))
        self.txt_start_position_label.grid(row=2, column=0, sticky="s")
        self.txt_end_position_label = tk.Label(self.txt_controllers, text="Posición fin: ", fg="white", bg="#212121", font=("Arial", 15))
        self.txt_end_position_label.grid(row=4, column=0, sticky="s")
        self.txt_start_position.grid(row=3, column=0, sticky="n")
        self.txt_end_position.grid(row=5, column=0, sticky="n")
        
        open_txt_button = tk.Button(self.txt_controllers, text="Seleccionar Txt", command=self.on_open_txt_button_click, relief="flat", bg="#eb2b2b", fg="white", height=3, font=("Arial", 12))
        open_txt_button.grid(row=0, column=0, sticky="n")
        
        # Botón para procesar archivos
        process_files_button = tk.Button(self.cruce_datos_generar_archivo_frame, text="Procesar archivos", command=self.on_process_files_button_click, relief="flat", bg="#ffffff", fg="#000000", height=3, font=("Arial", 12))
        process_files_button.grid(row=2, columnspan=2)
        
        # Seccion de resumen archivos
        self.files_abstract = ctk.CTkTextbox(self.cruce_datos_generar_archivo_frame)
        self.files_abstract.grid(row=3, columnspan=2, padx=20, pady=20 ,sticky="nsew")
        self.files_abstract.insert("1.0", "Cargue los archivos para ver los detalles.")
        self.files_abstract.configure(state="disabled")
        
        self.scrollbar = ctk.CTkScrollbar(self.cruce_datos_generar_archivo_frame, command=self.files_abstract.yview, bg_color="white")
        self.scrollbar.grid(row=3, column=1, padx=25, pady=20, sticky="nse")
        
        self.files_abstract.configure(yscrollcommand=self.scrollbar.set)
        
        # Boton para guardar resultado
        self.save_result_button = tk.Button(self.cruce_datos_generar_archivo_frame, text="Guardar resultado", command=self.on_save_result_button_click, relief="flat", bg="#ffffff", fg="#000000", height=3, font=("Arial", 12))
        self.save_result_button.grid(row=4, columnspan=2)
        
    ### Utils
    def update_start_position_txt(self, value):
        print(value)
        print(self.txt_start_position.get())
            
    def update_end_position_txt(self, value):
        print(value)
        print(self.txt_end_position["value"])
            
    def validate_position_txt(self, value):
        print(value)
        return value == "" or value.isdigit()
    
    def on_combobox_change(self, event):    
        print(self.columns_options.get())
              
    def verify_column_only_numbers(self):
        return re.match("^[0-9]+", self.columns_options.get())
    
    def on_open_excel_button_click(self):
        print(self.columns_options.get())
        self.excel_details = self.controller.open_excel()
        self.columns_options["values"] = self.excel_details["columns_list"]
        self.columns_options.set(self.columns_options["values"][0])
        self.update_files_details_text(self.excel_details["files_abstract_text"])
        
    def on_open_txt_button_click(self):
        self.txt_details = self.controller.open_txt()
        self.update_files_details_text(self.txt_details["files_abstract_text"])
        
    def on_process_files_button_click(self):
        if not self.excel_details:
            messagebox.showwarning(title="Archivo no seleccionado.", message="No has seleccionado una Planilla Excel.")
            return
        if not self.txt_details:
            messagebox.showwarning(title="Archivo no seleccionado", message="No has seleccionado un Documento de Texto.")
            return
        if self.columns_options.get() == "Selecciona una columna":
            messagebox.showwarning(title="Columna no seleccionada.", message="Debes seleccionar una columna del Excel para analizar.")
            return
        if not self.txt_start_position.get():
            messagebox.showwarning(title="Error posicion de inicio txt", message="Debes indicar la posicion de inicio para el Documento de texto.")
            return
        if not self.txt_end_position.get():
            messagebox.showwarning(title="Error posicion de fin txt", message="Debes indicar la posicion de fin para el Documento de texto.")
            return
        if self.txt_start_position.get() > self.txt_end_position.get():
            messagebox.showwarning(title="Error posiciones ingresadas para txt", message="La posición de inicio no puede ser mayor a la posicion de fin para analizar el documento de texto.")
            return
        
        self.process_result_details = self.controller.process_files()
        self.files_abstract.configure(state="normal")
        self.files_abstract.insert("end", f"Coincidencias encontradas: {self.process_result_details["coincidences"]}\r\n")
        self.files_abstract.insert("end", f"Errores encontrados en el Excel: {len(self.process_result_details["excel_wrong_data_rows"])}\r\n")
        self.files_abstract.insert("end", f"Errores encontrados en el Txt: {len(self.process_result_details["txt_wrong_data_rows"])}\r\n")
        self.files_abstract.configure(state="disabled")
        
    def update_files_details_text(self, msg):
        self.files_abstract.configure(state="normal")
        if self.files_abstract.get("1.0", "end").strip() == "Cargue los archivos para ver los detalles.":
            self.files_abstract.delete("1.0", "end")
        self.files_abstract.insert("end", f"{msg}")
        self.files_abstract.configure(state="disabled")
        
    def on_save_result_button_click(self):
       self.controller.write_txt()