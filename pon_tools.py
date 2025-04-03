import pandas as pd
import openpyxl
import tkinter as tk
from tkinter import filedialog
import os

def create_excel(df, data):
    #Crear libro de excel
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Hoja"
    
    #print(wb.sheetnames)
    
    #print(df.columns)
    sheet.append(tuple(df.columns))

    # Agregar coincidencias al nuevo excel
    coincidences = df[df['DNI'].isin(data)]
    for item in coincidences.itertuples(index=False):
        if item.index == 0:
            continue
        sheet.append(tuple(item))
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Text files", "*.xlsx"), ("All files", "*.*")],
        title="Guardar archivo"
    )
    
    wb.save(file_path)
    
    if file_path:
        os.startfile(file_path)
    #return wb    