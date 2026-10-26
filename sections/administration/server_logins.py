from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_server_logins_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Server Logins & Security Overview")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Login Name", "Login Type", "Status", "Created Date"])
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
            name AS LoginName,
            type_desc AS LoginType,
            CASE is_disabled WHEN 1 THEN 'Disabled' ELSE 'Enabled' END AS Status,
            CAST(create_date AS VARCHAR(30)) AS CreatedDate
        FROM sys.server_principals
        WHERE type IN ('S', 'U', 'G');
    """
    results = db.execute_query(query)
    
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        lname = str(record.get('LoginName') or record.get('loginname') or '')
        ltype = str(record.get('LoginType') or record.get('logintype') or '')
        status = str(record.get('Status') or record.get('status') or '')
        cdate = str(record.get('CreatedDate') or record.get('createddate') or '')
        
        table.setItem(row, 0, QTableWidgetItem(lname))
        table.setItem(row, 1, QTableWidgetItem(ltype))
        table.setItem(row, 2, QTableWidgetItem(status))
        table.setItem(row, 3, QTableWidgetItem(cdate))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget