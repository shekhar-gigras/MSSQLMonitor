from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_error_logs_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("SQL Server Error Log Viewer")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["Log Date", "Process Info", "Error Message Text"])
    table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
    
    table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    
    table.setStyleSheet("""
        QTableWidget {
            background-color: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            color: #0f172a;
            gridline-color: #e2e8f0;
        }
        QHeaderView::section {
            background-color: #f1f5f9;
            color: #334155;
            font-weight: bold;
            border: 1px solid #cbd5e1;
            padding: 4px;
        }
    """)
    
    db = DatabaseManager()
    query = "EXEC xp_readerrorlog 0, 1;"
    try:
        results = db.execute_query(query)
        results = results[:35] if results else [] # Limit to recent 35 records
    except Exception:
        results = []
        
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        ldate = str(record.get('LogDate') or record.get('logdate') or '')
        pinfo = str(record.get('ProcessInfo') or record.get('processinfo') or '')
        txt = str(record.get('Text') or record.get('text') or '')
        
        table.setItem(row, 0, QTableWidgetItem(ldate))
        table.setItem(row, 1, QTableWidgetItem(pinfo))
        table.setItem(row, 2, QTableWidgetItem(txt))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget