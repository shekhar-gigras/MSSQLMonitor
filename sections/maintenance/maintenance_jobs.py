from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_maintenance_jobs_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("SQL Server Agent Maintenance Jobs Status")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Job Name", "Run Status", "Run Time", "Message"])
    table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
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
        SELECT TOP 15
            j.name AS JobName,
            CASE h.run_status 
                WHEN 0 THEN 'Failed' 
                WHEN 1 THEN 'Succeeded' 
                WHEN 2 THEN 'Retry' 
                WHEN 3 THEN 'Canceled' 
                ELSE 'Unknown' 
            END AS RunStatus,
            STUFF(STUFF(RIGHT('000000' + CAST(h.run_time AS VARCHAR(6)), 6), 5, 0, ':'), 3, 0, ':') AS RunTime,
            h.message AS Message
        FROM msdb.dbo.sysjobs j
        JOIN msdb.dbo.sysjobhistory h ON j.job_id = h.job_id
        WHERE h.step_id = 0
        ORDER BY h.run_date DESC, h.run_time DESC;
    """
    results = db.execute_query(query)
    
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        jname = str(record.get('JobName') or record.get('jobname') or '')
        status = str(record.get('RunStatus') or record.get('runstatus') or '')
        rtime = str(record.get('RunTime') or record.get('runtime') or '')
        msg = str(record.get('Message') or record.get('message') or '')
        
        table.setItem(row, 0, QTableWidgetItem(jname))
        table.setItem(row, 1, QTableWidgetItem(status))
        table.setItem(row, 2, QTableWidgetItem(rtime))
        table.setItem(row, 3, QTableWidgetItem(msg))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget