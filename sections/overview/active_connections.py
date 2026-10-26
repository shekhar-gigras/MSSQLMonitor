from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_active_connections_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Active Connection User Details")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #334155;")
    
    table = QTableWidget()
    table.setColumnCount(5)
    table.setHorizontalHeaderLabels(["Session ID", "Login Name", "Host Name", "Database", "Status"])
    
    # Enable Interactive resizing for columns so horizontal scroll works properly
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
    table.horizontalHeader().setStretchLastSection(True)
    
    # Ensure Scrollbars appear automatically when data/columns exceed dimensions
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
        SELECT TOP 20
            s.session_id AS SessionID,
            s.login_name AS LoginName,
            ISNULL(s.host_name, 'N/A') AS HostName,
            ISNULL(d.name, 'N/A') AS DatabaseName,
            s.status AS Status
        FROM sys.dm_exec_sessions s
        LEFT JOIN sys.databases d ON s.database_id = d.database_id
        WHERE s.is_user_process = 1
        ORDER BY s.last_request_start_time DESC;
    """
    results = db.execute_query(query)
    
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        session_id = str(record.get('SessionID') or record.get('sessionid') or '')
        login_name = str(record.get('LoginName') or record.get('loginname') or '')
        host_name = str(record.get('HostName') or record.get('hostname') or '')
        db_name = str(record.get('DatabaseName') or record.get('databasename') or '')
        status = str(record.get('Status') or record.get('status') or '')
        
        table.setItem(row, 0, QTableWidgetItem(session_id))
        table.setItem(row, 1, QTableWidgetItem(login_name))
        table.setItem(row, 2, QTableWidgetItem(host_name))
        table.setItem(row, 3, QTableWidgetItem(db_name))
        table.setItem(row, 4, QTableWidgetItem(status))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget