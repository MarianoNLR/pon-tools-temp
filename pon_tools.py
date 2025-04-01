import pandas as pd
import openpyxl

def create_excel(df):
    #Crear libro de excel
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Hoja"
    
    #print(wb.sheetnames)
    
    #print(df.columns)
    sheet.append(tuple(df.columns))

    # Agregar coincidencias al nuevo excel
    for item in coincidences.itertuples(index=False):
        if item.index == 0:
            continue
        sheet.append(tuple(item))
    
    return wb

if __name__ == "__main__":
    # Leer excel y cargar en data frame
    df = pd.read_excel("./example.xlsx")
    df["DNI"] = df["DNI"].astype(str)
    
    #Leer archivo de texto
    with open("./example_txt.txt", "r") as txt:
        data = []
        # Leer archivo de texto linea por linea
        for line in txt:
            data.append(line.strip())

    # Obtener las coincidencias entre excel y txt por DNI
    coincidences = df[df['DNI'].isin(data)]
    wb = create_excel(df)
    wb.save('./result.xlsx')