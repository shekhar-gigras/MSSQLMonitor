from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_blocking_sessions_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Active Blocking Sessions")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Blocked SPID", "Blocking SPID", "Wait Type", "Wait Duration (ms)"])
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
            session_id AS BlockedSPID,
            blocking_session_id AS BlockingSPID,
            wait_type AS WaitType,
            wait_duration_ms AS WaitDurationMs
        FROM sys.dm_os_waiting_tasks
        WHERE blocking_session_id IS NOT NULL;
    """
    results = db.execute_query(query)
    
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        b_spid = str(record.get('BlockedSPID') or record.get('blockedspid') or '')
        bl_spid = str(record.get('BlockingSPID') or record.get('blockingspid') or '')
        w_type = str(record.get('WaitType') or record.get('waittype') or '')
        w_dur = str(record.get('WaitDurationMs') or record.get('waitdurationms') or '')
        
        table.setItem(row, 0, QTableWidgetItem(b_spid))
        table.setItem(row, 1, QTableWidgetItem(bl_spid))
        table.setItem(row, 2, QTableWidgetItem(w_type))
        table.setItem(row, 3, QTableWidgetItem(w_dur))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget