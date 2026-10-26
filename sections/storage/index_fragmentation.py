from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_index_fragmentation_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("High Index Fragmentation (> 30%)")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Database Name", "Table Name", "Object ID", "Fragmentation (%)"])
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
    # Fetching Database Name, resolved Table Name, Object ID, and Fragmentation %
    query = """
        SELECT TOP 20
            DB_NAME(ps.database_id) AS DatabaseName,
            OBJECT_NAME(ps.object_id, ps.database_id) AS TableName,
            ps.object_id AS ObjectID,
            CAST(ps.avg_fragmentation_in_percent AS DECIMAL(5,2)) AS FragmentationPct
        FROM sys.dm_db_index_physical_stats(NULL, NULL, NULL, NULL, 'LIMITED') ps
        WHERE ps.avg_fragmentation_in_percent > 30 
          AND ps.database_id > 4
          AND ps.object_id IS NOT NULL
        ORDER BY ps.avg_fragmentation_in_percent DESC;
    """
    results = db.execute_query(query)
    
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        dbname = str(record.get('DatabaseName') or record.get('databasename') or 'N/A')
        tablename = str(record.get('TableName') or record.get('tablename') or 'N/A')
        objid = str(record.get('ObjectID') or record.get('objectid') or '')
        frag = f"{str(record.get('FragmentationPct') or record.get('fragmentationpct') or '0')} %"
        
        table.setItem(row, 0, QTableWidgetItem(dbname))
        table.setItem(row, 1, QTableWidgetItem(tablename))
        table.setItem(row, 2, QTableWidgetItem(objid))
        table.setItem(row, 3, QTableWidgetItem(frag))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget