import pandas as pd
import openpyxl

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
    wb.save("./result.xlsx")
    #return wb    