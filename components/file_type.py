from enum import Enum
import os

class FileType(Enum):
    pass
    # TXT = ".txt",
    # EXCEL = (".xlsx", ".xls")
    
    # def get_file_extension(file_path):
    #     ext = os.path.splitext(file_path)[1].lower()
    #     for file_type in FileType:
    #         if ext in file_type.value:
    #             return file_type
    #     else:
    #         raise ValueError("Tipo de archivo no soportado.")