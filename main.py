import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from components.sidebar import Sidebar

class MainApp:
    
    def __init__(self):
        
        ### Config ventana principal
        self.root = tk.Tk(screenName="PON Tools")
        self.root.title("PON Tools")
        self.root.geometry("900x900")
        self.root.minsize(width=800, height=900)
        
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
        self.sidebar = Sidebar(self.root, self.main_content)
        
        #open_excel_button = ttk.Button(text="Seleccionar Excel", command=on_open_excel_button_click)
        #open_excel_button.place(x=50, y=50)
        
        self.root.mainloop()
        #root.withdraw()
    
    ### Mostrar Frame de Bienvenida
    def show_welcome_frame(self):
        welcome_frame = tk.Frame(self.main_content, bg="#212121", height=300)
        welcome_frame.grid(row=0, column=0, sticky="nsew")
        welcome_frame.grid_rowconfigure(0, weight=1)
        
        welcome_frame.grid_columnconfigure(0, weight=1)
        
        label = tk.Label(welcome_frame, text="Bienvenido a PON Tools", font=("Arial", 40), wraplength=400, bg="#212121", fg="white")
        label.grid(row=0, column=0, sticky="nsew")
        

if __name__ == "__main__":
    app = MainApp()