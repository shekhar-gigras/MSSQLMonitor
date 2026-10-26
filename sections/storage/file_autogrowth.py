from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_file_autogrowth_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Database File Auto-Growth & Restrictions")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Database Name", "Logical File Name", "Growth Type", "Growth Value"])
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
            CASE mf.is_percent_growth WHEN 1 THEN 'Percentage (%)' ELSE 'Size (MB)' END AS GrowthType,
            CASE mf.is_percent_growth 
                WHEN 1 THEN CAST(mf.growth AS VARCHAR(10)) + '%' 
                ELSE CAST(CAST(mf.growth * 8.0 / 1024 AS DECIMAL(10,2)) AS VARCHAR(20)) + ' MB' 
            END AS GrowthValue
        FROM sys.databases d
        JOIN sys.master_files mf ON d.database_id = mf.database_id
        WHERE d.database_id > 4;
    """
    results = db.execute_query(query)
    
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        dbname = str(record.get('DatabaseName') or record.get('databasename') or '')
        fname = str(record.get('LogicalFileName') or record.get('logicalfilename') or '')
        gtype = str(record.get('GrowthType') or record.get('growthtype') or '')
        gval = str(record.get('GrowthValue') or record.get('growthvalue') or '')
        
        table.setItem(row, 0, QTableWidgetItem(dbname))
        table.setItem(row, 1, QTableWidgetItem(fname))
        table.setItem(row, 2, QTableWidgetItem(gtype))
        table.setItem(row, 3, QTableWidgetItem(gval))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget