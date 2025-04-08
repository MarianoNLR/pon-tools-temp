import tkinter as tk
from views.excel_and_txt_to_txt_view import ExcelAndTxtToTxtView

class Sidebar():
    def __init__(self, root, main_content):
        self.root = root
        self.main_content = main_content
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
        
    def on_click_option1(self):
        ExcelAndTxtToTxtView(self.main_content)
        
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