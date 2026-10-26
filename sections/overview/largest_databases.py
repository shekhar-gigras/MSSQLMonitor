from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_largest_databases_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("All User Databases")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #334155;")
    
    table = QTableWidget()
    table.setColumnCount(2)
    table.setHorizontalHeaderLabels(["Database Name", "Size (MB)"])
    
    # Enable Interactive resizing so horizontal scroll appears if needed
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
    table.horizontalHeader().setStretchLastSection(True)
    
    # Ensure Scrollbars appear automatically as needed
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
            CAST(SUM(mf.size) * 8.0 / 1024 AS DECIMAL(10,2)) AS SizeMB
        FROM sys.databases d
        JOIN sys.master_files mf ON d.database_id = mf.database_id
        WHERE d.database_id > 4 
        GROUP BY d.name
        ORDER BY SizeMB DESC;
    """
    results = db.execute_query(query)
    
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        db_name = str(record.get('DatabaseName') or record.get('databasename') or list(record.values())[0])
        size_val = record.get('SizeMB') if 'SizeMB' in record else record.get('sizemb', list(record.values())[1])
        size_mb = f"{size_val} MB"
        
        table.setItem(row, 0, QTableWidgetItem(db_name))
        table.setItem(row, 1, QTableWidgetItem(str(size_mb)))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget