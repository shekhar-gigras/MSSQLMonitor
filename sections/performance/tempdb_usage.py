from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_tempdb_usage_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("TempDB File Storage")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(2)
    table.setHorizontalHeaderLabels(["TempDB File Name", "Total Size (MB)"])
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    
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
    query = """
        SELECT 
            name AS FileName,
            CAST(size * 8.0 / 1024 AS DECIMAL(10,2)) AS TotalSizeMB
        FROM sys.master_files
        WHERE database_id = 2;
    """
    results = db.execute_query(query)
    
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        fname = str(record.get('FileName') or record.get('filename') or '')
        tsize = str(record.get('TotalSizeMB') or record.get('totalsizemb') or '0')
        
        table.setItem(row, 0, QTableWidgetItem(fname))
        table.setItem(row, 1, QTableWidgetItem(tsize))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget