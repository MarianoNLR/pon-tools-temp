import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pon_tools
from cruce_datos_generar_archivo import CruceDatosGenerarArchivo

class MainApp:
    
    def __init__(self):
        self.excel_file = None
        self.txt_file = None
        self.txt_data = None
        self.excel_df = None
        
        ### Config ventana principal
        self.root = tk.Tk(screenName="PON Tools")
        self.root.title("PON Tools")
        self.root.geometry("500x600")
        self.root.minsize(width=500, height=600)
        
        # Configuracion grid ventana principal
        self.root.grid_columnconfigure(0, weight=1, uniform="equal")
        self.root.grid_columnconfigure(1, weight=4, uniform="equal")
        
        self.root.grid_rowconfigure(0, weight=1)
        
            
        ### Contenedor de contenido principal
        self.main_content = tk.Frame(self.root, bg="#212121", height=300)
        self.main_content.grid(row=0, column=1, sticky="nsew")
        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)
        
        # Inicializar frame de bienvenida en contenedor main
        self.show_welcome_frame()
        self.create_sidebar()
        
        #open_excel_button = ttk.Button(text="Seleccionar Excel", command=on_open_excel_button_click)
        #open_excel_button.place(x=50, y=50)
        
        self.root.mainloop()
        #root.withdraw()
    
    def create_sidebar(self):
        ### Barra lateral izquierda
        self.sidebar = tk.Frame(self.root, bg="#eb2b2b")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ### Barra lateral izquierda opciones
        self.sidebar_opt1 = tk.Button(self.sidebar, text="Opcion 1", relief="flat", height=2, foreground="white", bg="#eb2b2b", font=("Arial", 12), command=self.on_click_option1)
        self.sidebar_opt2 = tk.Button(self.sidebar, text="Opcion 2", relief="flat", height=2, foreground="white", bg="#eb2b2b", font=("Arial", 12), command=self.show_option2_frame)
        self.sidebar_opt3 = tk.Button(self.sidebar, text="Opcion 3", relief="flat", height=2, foreground="white", bg="#eb2b2b", font=("Arial", 12), command=self.show_option3_frame)
        self.sidebar_opt4 = tk.Button(self.sidebar, text="Opcion 4", relief="flat", height=2, foreground="white", bg="#eb2b2b", font=("Arial", 12), command=self.show_option4_frame)
        
        self.sidebar_opt1.pack(fill="x", pady=0)
        self.sidebar_opt2.pack(fill="x", pady=1)
        self.sidebar_opt3.pack(fill="x", pady=1)
        self.sidebar_opt4.pack(fill="x", pady=1)

    ### Mostrar Frame de Bienvenida
    def show_welcome_frame(self):
        welcome_frame = tk.Frame(self.main_content, bg="#212121", height=300)
        welcome_frame.grid(row=0, column=0, sticky="nsew")
        welcome_frame.grid_rowconfigure(0, weight=1)
        
        welcome_frame.grid_columnconfigure(0, weight=1)
        welcome_frame.grid_columnconfigure(1, weight=1)
        
        label = tk.Label(welcome_frame, text="Bienvenido a PON Tools", font=("Arial", 40), wraplength=400, bg="#212121", fg="white")
        label.grid(row=0, column=0, sticky="nsew")
        
    def on_click_option1(self):
        option1 = CruceDatosGenerarArchivo(self.main_content)
        
    ### Mostrar Frame de Opcion 2
    def show_option2_frame(self):
        for frame in self.main_content.winfo_children():
            frame.destroy()
        
        # Creacion de frames
        opcion2_frame =tk.Frame(self.main_content, bg="#212121", height=300)
        opcion2_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configuracion de grid opcion 2
        opcion2_frame.grid_rowconfigure(0, weight=1)
        opcion2_frame.grid_rowconfigure(1, weight=1)
        opcion2_frame.grid_rowconfigure(2, weight=3)
        opcion2_frame.grid_columnconfigure(0, weight=1)
        opcion2_frame.grid_columnconfigure(1, weight=1)
        
        ### Contenido principal frame opcion 2
        # # Botones de seleccion de archivos
        # open_excel_button = tk.Button(opcion1_frame ,text="Seleccionar Excel", command=on_open_excel_button_click, relief="flat", bg="#eb2b2b", fg="white", height=3, font=("Arial", 12))
        # open_txt_button = tk.Button(opcion1_frame, text="Seleccionar Txt", command=on_open_txt_button_click, relief="flat", bg="#eb2b2b", fg="white", height=3, font=("Arial", 12))
        # open_excel_button.grid(row=1, column=0)
        # open_txt_button.grid(row=1, column=1)
        
        # Titulo del frame
        label = tk.Label(opcion2_frame, text="Bienvenido a la Opcion 2", wraplength=350, font=("Arial", 40), bg="#212121", fg="white")
        label.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        # Botón para procesar archivos
        # process_files_button = tk.Button(opcion1_frame, text="Procesar archivos", command=on_process_files_button_click, relief="flat", bg="#ffffff", fg="#000000", height=3, font=("Arial", 12))
        # process_files_button.grid(row=2, columnspan=2)
        
    ### Mostrar Frame de Opcion 3
    def show_option3_frame(self):
        for frame in self.main_content.winfo_children():
            frame.destroy()
        
        # Creacion de frames
        opcion3_frame =tk.Frame(self.main_content, bg="#212121", height=300)
        opcion3_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configuracion de grid opcion 3
        opcion3_frame.grid_rowconfigure(0, weight=1)
        opcion3_frame.grid_rowconfigure(1, weight=1)
        opcion3_frame.grid_rowconfigure(2, weight=3)
        opcion3_frame.grid_columnconfigure(0, weight=1)
        opcion3_frame.grid_columnconfigure(1, weight=1)
        
        ### Contenido principal frame opcion 3
        # # Botones de seleccion de archivos
        # open_excel_button = tk.Button(opcion1_frame ,text="Seleccionar Excel", command=on_open_excel_button_click, relief="flat", bg="#eb2b2b", fg="white", height=3, font=("Arial", 12))
        # open_txt_button = tk.Button(opcion1_frame, text="Seleccionar Txt", command=on_open_txt_button_click, relief="flat", bg="#eb2b2b", fg="white", height=3, font=("Arial", 12))
        # open_excel_button.grid(row=1, column=0)
        # open_txt_button.grid(row=1, column=1)
        
        # Titulo del frame
        label = tk.Label(opcion3_frame, text="Bienvenido a la Opcion 3", wraplength=350, font=("Arial", 40), bg="#212121", fg="white")
        label.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        # # Botón para procesar archivos
        # process_files_button = tk.Button(opcion1_frame, text="Procesar archivos", command=on_process_files_button_click, relief="flat", bg="#ffffff", fg="#000000", height=3, font=("Arial", 12))
        # process_files_button.grid(row=2, columnspan=2)
        
    ### Mostrar Frame de Opcion 4
    def show_option4_frame(self):
        for frame in self.main_content.winfo_children():
            frame.destroy()
        
        # Creacion de frames
        opcion4_frame =tk.Frame(self.main_content, bg="#212121", height=300)
        opcion4_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configuracion de grid opcion 4
        opcion4_frame.grid_rowconfigure(0, weight=1)
        opcion4_frame.grid_rowconfigure(1, weight=1)
        opcion4_frame.grid_rowconfigure(2, weight=3)
        opcion4_frame.grid_columnconfigure(0, weight=1)
        opcion4_frame.grid_columnconfigure(1, weight=1)
        
        ### Contenido principal frame opcion 4
        # # Botones de seleccion de archivos
        # open_excel_button = tk.Button(opcion1_frame ,text="Seleccionar Excel", command=on_open_excel_button_click, relief="flat", bg="#eb2b2b", fg="white", height=3, font=("Arial", 12))
        # open_txt_button = tk.Button(opcion1_frame, text="Seleccionar Txt", command=on_open_txt_button_click, relief="flat", bg="#eb2b2b", fg="white", height=3, font=("Arial", 12))
        # open_excel_button.grid(row=1, column=0)
        # open_txt_button.grid(row=1, column=1)
        
        # Titulo del frame
        label = tk.Label(opcion4_frame, text="Bienvenido a la Opcion 4", wraplength=350, font=("Arial", 40), bg="#212121", fg="white")
        label.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        # # Botón para procesar archivos
        # process_files_button = tk.Button(opcion1_frame, text="Procesar archivos", command=on_process_files_button_click, relief="flat", bg="#ffffff", fg="#000000", height=3, font=("Arial", 12))
        # process_files_button.grid(row=2, columnspan=2)

if __name__ == "__main__":
    app = MainApp()