from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_physical_drive_space_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Physical Drive / Volume Free Space")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Drive / Path", "Total Size (GB)", "Free Space (GB)", "Free (%)"])
    table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
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
            LEFT(mf.physical_name, 3) AS Drive,
            CAST(vs.total_bytes * 1.0 / 1024 / 1024 / 1024 AS DECIMAL(10,2)) AS TotalSizeGB,
            CAST(vs.available_bytes * 1.0 / 1024 / 1024 / 1024 AS DECIMAL(10,2)) AS FreeSpaceGB,
            CAST((vs.available_bytes * 100.0 / vs.total_bytes) AS DECIMAL(5,2)) AS FreePercentage
        FROM sys.master_files mf
        CROSS APPLY sys.dm_os_volume_stats(mf.database_id, mf.file_id) vs
        GROUP BY LEFT(mf.physical_name, 3), vs.total_bytes, vs.available_bytes;
    """
    results = db.execute_query(query)
    
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        drive = str(record.get('Drive') or record.get('drive') or 'N/A')
        total_gb = str(record.get('TotalSizeGB') or record.get('totalsizegb') or '0')
        free_gb = str(record.get('FreeSpaceGB') or record.get('freespacegb') or '0')
        free_pct = f"{str(record.get('FreePercentage') or record.get('freepercentage') or '0')} %"
        
        table.setItem(row, 0, QTableWidgetItem(drive))
        table.setItem(row, 1, QTableWidgetItem(total_gb))
        table.setItem(row, 2, QTableWidgetItem(free_gb))
        table.setItem(row, 3, QTableWidgetItem(free_pct))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget