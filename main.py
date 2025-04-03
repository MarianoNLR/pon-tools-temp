import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pon_tools

excel_file = None
txt_file = None
txt_data = None
excel_df = None

def on_open_excel_button_click():
    global excel_file
    global excel_df
    excel_file = filedialog.askopenfilename(title="Selecciona una archivo")
    if excel_file:
        print(f"Archivo: {excel_file}")
    else:
        print("No se seleccionó ningun archivo.")
    # Leer excel y cargar en data frame
    excel_df = pd.read_excel(excel_file)
    excel_df["DNI"] = excel_df["DNI"].astype(str)
    
def on_open_txt_button_click():
    global txt_file
    global txt_data
    txt_file = filedialog.askopenfilename(title="Selecciona una archivo")
    if txt_file:
        print(f"Archivo: {txt_file}")
    else:
        print("No se seleccionó ningun archivo.")
    # Leer txt y cargar en data frame
    with open(txt_file, "r") as txt:
        txt_data = []
        # Leer archivo de texto linea por linea
        for line in txt:
            txt_data.append(line.strip())

def on_process_files_button_click():
    # Obtener las coincidencias entre excel y txt por DNI
    pon_tools.create_excel(excel_df, txt_data)

### Mostrar Frame de Bienvenida
def show_welcome_frame():
    welcome_frame = tk.Frame(main_content, bg="#212121", height=300)
    welcome_frame.grid(row=0, column=0, sticky="nsew")
    welcome_frame.grid_rowconfigure(0, weight=1)
    
    welcome_frame.grid_columnconfigure(0, weight=1)
    welcome_frame.grid_columnconfigure(1, weight=1)
    
    label = tk.Label(welcome_frame, text="Bienvenido a PON Tools", font=("Arial", 40), wraplength=400, bg="#212121", fg="white")
    label.grid(row=0, column=0, sticky="nsew")
    
### Mostrar Frame de Opcion 1
def show_option1_frame():
    for frame in main_content.winfo_children():
        frame.destroy()
    
    # Creacion de frames
    opcion1_frame =tk.Frame(main_content, bg="#212121", height=300)
    opcion1_frame.grid(row=0, column=0, sticky="nsew")
    
    # Configuracion de grid opcion 1
    opcion1_frame.grid_rowconfigure(0, weight=1)
    opcion1_frame.grid_rowconfigure(1, weight=1)
    opcion1_frame.grid_rowconfigure(2, weight=3)
    opcion1_frame.grid_columnconfigure(0, weight=1)
    opcion1_frame.grid_columnconfigure(1, weight=1)
    
    ### Contenido principal frame opcion 1
    # Botones de seleccion de archivos
    open_excel_button = tk.Button(opcion1_frame ,text="Seleccionar Excel", command=on_open_excel_button_click, relief="flat", bg="#eb2b2b", fg="white", height=3, font=("Arial", 12))
    open_txt_button = tk.Button(opcion1_frame, text="Seleccionar Txt", command=on_open_txt_button_click, relief="flat", bg="#eb2b2b", fg="white", height=3, font=("Arial", 12))
    open_excel_button.grid(row=1, column=0)
    open_txt_button.grid(row=1, column=1)
    
    # Titulo del frame
    label = tk.Label(opcion1_frame, text="Bienvenido a la Opcion 1", wraplength=350, font=("Arial", 40), bg="#212121", fg="white")
    label.grid(row=0, column=0, columnspan=2, sticky="nsew")
    
    # Botón para procesar archivos
    process_files_button = tk.Button(opcion1_frame, text="Procesar archivos", command=on_process_files_button_click, relief="flat", bg="#ffffff", fg="#000000", height=3, font=("Arial", 12))
    process_files_button.grid(row=2, columnspan=2)
    
### Mostrar Frame de Opcion 2
def show_option2_frame():
    for frame in main_content.winfo_children():
        frame.destroy()
    
    # Creacion de frames
    opcion2_frame =tk.Frame(main_content, bg="#212121", height=300)
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
def show_option3_frame():
    for frame in main_content.winfo_children():
        frame.destroy()
    
    # Creacion de frames
    opcion3_frame =tk.Frame(main_content, bg="#212121", height=300)
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
def show_option4_frame():
    for frame in main_content.winfo_children():
        frame.destroy()
    
    # Creacion de frames
    opcion4_frame =tk.Frame(main_content, bg="#212121", height=300)
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
    ### Config ventana principal
    root = tk.Tk(screenName="PON Tools")
    root.title("PON Tools")
    root.geometry("400x300")
    
    # Configuracion grid ventana principal
    root.grid_columnconfigure(0, weight=1, uniform="equal")
    root.grid_columnconfigure(1, weight=4, uniform="equal")
    
    root.grid_rowconfigure(0, weight=1)
    
    ### Contenedor de contenido principal
    main_content = tk.Frame(root, bg="#212121", height=300)
    main_content.grid(row=0, column=1, sticky="nsew")
    main_content.grid_rowconfigure(0, weight=1)
    main_content.grid_columnconfigure(0, weight=1)
    
    # Inicializar frame de bienvenida en contenedor main
    show_welcome_frame()
    
    ### Barra lateral izquierda
    sidebar = tk.Frame(root, bg="#eb2b2b")
    sidebar.grid(row=0, column=0, sticky="nsew")
    
    ### Barra lateral izquierda opciones
    sidebar_opt1 = tk.Button(sidebar, text="Opcion 1", relief="flat", height=2, foreground="white", bg="#eb2b2b", font=("Arial", 12), command=show_option1_frame)
    sidebar_opt2 = tk.Button(sidebar, text="Opcion 2", relief="flat", height=2, foreground="white", bg="#eb2b2b", font=("Arial", 12), command=show_option2_frame)
    sidebar_opt3 = tk.Button(sidebar, text="Opcion 3", relief="flat", height=2, foreground="white", bg="#eb2b2b", font=("Arial", 12), command=show_option3_frame)
    sidebar_opt4 = tk.Button(sidebar, text="Opcion 4", relief="flat", height=2, foreground="white", bg="#eb2b2b", font=("Arial", 12), command=show_option4_frame)
    
    sidebar_opt1.pack(fill="x", pady=0)
    sidebar_opt2.pack(fill="x", pady=1)
    sidebar_opt3.pack(fill="x", pady=1)
    sidebar_opt4.pack(fill="x", pady=1)
    
    
    #open_excel_button = ttk.Button(text="Seleccionar Excel", command=on_open_excel_button_click)
    #open_excel_button.place(x=50, y=50)
    
    root.mainloop()
    #root.withdraw()