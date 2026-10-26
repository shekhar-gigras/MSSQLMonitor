from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_long_running_queries_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Long Running & Active Requests")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["SPID", "Database", "Command", "Elapsed Time (sec)"])
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
            r.session_id AS SPID,
            DB_NAME(r.database_id) AS DatabaseName,
            r.command AS Command,
            r.total_elapsed_time / 1000 AS ElapsedSec
        FROM sys.dm_exec_requests r
        WHERE r.session_id > 50 AND r.session_id <> @@SPID
        ORDER BY ElapsedSec DESC;
    """
    results = db.execute_query(query)
    
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        spid = str(record.get('SPID') or record.get('spid') or '')
        dbname = str(record.get('DatabaseName') or record.get('databasename') or '')
        cmd = str(record.get('Command') or record.get('command') or '')
        elapsed = str(record.get('ElapsedSec') or record.get('elapsedsec') or '')
        
        table.setItem(row, 0, QTableWidgetItem(spid))
        table.setItem(row, 1, QTableWidgetItem(dbname))
        table.setItem(row, 2, QTableWidgetItem(cmd))
        table.setItem(row, 3, QTableWidgetItem(elapsed))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget