from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_file_space_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Database File Space Utilization (Data & Log)")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Database Name", "Logical File Name", "File Type", "Size (MB)"])
    table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
    
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
            d.name AS DatabaseName,
            mf.name AS LogicalFileName,
            CASE mf.type_desc WHEN 'ROW' THEN 'Data (.mdf)' ELSE 'Log (.ldf)' END AS FileType,
            CAST(mf.size * 8.0 / 1024 AS DECIMAL(10,2)) AS SizeMB
        FROM sys.databases d
        JOIN sys.master_files mf ON d.database_id = mf.database_id
        WHERE d.database_id > 4
        ORDER BY SizeMB DESC;
    """
    results = db.execute_query(query)
    
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        dbname = str(record.get('DatabaseName') or record.get('databasename') or '')
        fname = str(record.get('LogicalFileName') or record.get('logicalfilename') or '')
        ftype = str(record.get('FileType') or record.get('filetype') or '')
        fsize = str(record.get('SizeMB') or record.get('sizemb') or '0')
        
        table.setItem(row, 0, QTableWidgetItem(dbname))
        table.setItem(row, 1, QTableWidgetItem(fname))
        table.setItem(row, 2, QTableWidgetItem(ftype))
        table.setItem(row, 3, QTableWidgetItem(fsize))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget