from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidgetItem, QListWidget, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush
from resource_path import resource_path

class ErrorsDetailsView(QDialog):
    def __init__(self, title, file_type, error_data):
        super().__init__()
        self.setWindowTitle(title)
        self.setMinimumSize(500, 400)
        
        bg_img_path = resource_path("assets/prism.png")
        self.setStyleSheet(f"background-image: url('{bg_img_path.replace("\\", "/")}'); background-color: #de4c47;")
        layout = QVBoxLayout()
        title_label = QLabel(f"Errores en el archivo {file_type}")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px; color: white")
        layout.addWidget(title_label)
        
        error_list = QListWidget()
        error_list.setStyleSheet("""
            QListWidget {
                color: white;
                border: 1px solid white;
                font-size: 12px;
                padding: 5px
            }
            
            QListWidget::item {
                padding: 3px;
            }

            QListWidget::item:selected {
                background-color: #333;
                color: #00ffff;
            }

            QScrollBar:vertical {
                background: #2e2e2e;
                width: 10px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background: #555;
                min-height: 20px;
                border-radius: 4px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
                                 """)
        if error_data:
            for error in error_data:
                item = QListWidgetItem(str(error["msg"]))
                item.setForeground(QBrush(QColor("white")))
                error_list.addItem(item)
        else:
            QListWidgetItem("No se encontraron errores.", error_list)
        
        layout.addWidget(error_list)
        
        self.setLayout(layout)