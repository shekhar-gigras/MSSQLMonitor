from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_mail_history_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Database Mail & Notification History")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Mail ID", "Status", "Request Date", "Subject"])
    table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
    
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
            mailitem_id AS MailID,
            sent_status AS Status,
            CAST(send_request_date AS VARCHAR(30)) AS RequestDate,
            ISNULL(subject, 'No Subject') AS Subject
        FROM msdb.dbo.sysmail_allitems
        ORDER BY send_request_date DESC;
    """
    try:
        results = db.execute_query(query)
    except Exception:
        results = []
        
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        mid = str(record.get('MailID') or record.get('mailid') or '')
        status = str(record.get('Status') or record.get('status') or '')
        rdate = str(record.get('RequestDate') or record.get('requestdate') or '')
        subj = str(record.get('Subject') or record.get('subject') or '')
        
        table.setItem(row, 0, QTableWidgetItem(mid))
        table.setItem(row, 1, QTableWidgetItem(status))
        table.setItem(row, 2, QTableWidgetItem(rdate))
        table.setItem(row, 3, QTableWidgetItem(subj))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget