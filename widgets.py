from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel

class KPICard(QFrame):
    def __init__(self, title, value, unit="", parent=None):
        super().__init__(parent)
        self.setObjectName("kpiCard")
        self.setStyleSheet("""
            QFrame#kpiCard {
                background-color: #ffffff;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #64748b; font-size: 13px; font-weight: bold;")
        
        self.value_label = QLabel(f"{value} {unit}")
        self.value_label.setStyleSheet("color: #0f172a; font-size: 24px; font-weight: bold;")
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

    def update_value(self, value, unit=""):
        self.value_label.setText(f"{value} {unit}")