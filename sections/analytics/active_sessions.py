from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_active_sessions_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Active Sessions & Blocking Overview")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(5)
    table.setHorizontalHeaderLabels(["SPID", "Login Name", "Database", "Status", "Blocking SPID"])
    table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
    table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
    
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
        SELECT TOP 25
            s.session_id AS SPID,
            ISNULL(s.login_name, 'Unknown') AS LoginName,
            ISNULL(DB_NAME(r.database_id), 'Master/System') AS DBName,
            ISNULL(r.status, s.status) AS Status,
            CAST(ISNULL(r.blocking_session_id, 0) AS VARCHAR(10)) AS BlockingSPID
        FROM sys.dm_exec_sessions s
        LEFT JOIN sys.dm_exec_requests r ON s.session_id = r.session_id
        WHERE s.is_user_process = 1
        ORDER BY s.cpu_time DESC;
    """
    try:
        results = db.execute_query(query)
    except Exception:
        results = []
        
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        spid = str(record.get('SPID') or record.get('spid') or '')
        lname = str(record.get('LoginName') or record.get('loginname') or '')
        dbname = str(record.get('DBName') or record.get('dbname') or '')
        status = str(record.get('Status') or record.get('status') or '')
        bspid = str(record.get('BlockingSPID') or record.get('blockingspid') or '')
        
        table.setItem(row, 0, QTableWidgetItem(spid))
        table.setItem(row, 1, QTableWidgetItem(lname))
        table.setItem(row, 2, QTableWidgetItem(dbname))
        table.setItem(row, 3, QTableWidgetItem(status))
        table.setItem(row, 4, QTableWidgetItem(bspid))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget