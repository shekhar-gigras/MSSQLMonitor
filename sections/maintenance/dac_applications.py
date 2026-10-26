from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_dac_applications_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Deployed Data-Tier Applications (BACPAC / DACFx)")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Application Name", "Version", "Description", "Created / Deployed Date"])
    table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
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
            instance_name AS AppName,
            type_version AS Version,
            ISNULL(description, 'No Description Provided') AS Description,
            CAST(date_created AS VARCHAR(30)) AS CreatedDate
        FROM msdb.dbo.sysdac_instances;
    """
    results = db.execute_query(query)
    
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        app = str(record.get('AppName') or record.get('appname') or '')
        ver = str(record.get('Version') or record.get('version') or '')
        desc = str(record.get('Description') or record.get('description') or '')
        cdate = str(record.get('CreatedDate') or record.get('createddate') or '')
        
        table.setItem(row, 0, QTableWidgetItem(app))
        table.setItem(row, 1, QTableWidgetItem(ver))
        table.setItem(row, 2, QTableWidgetItem(desc))
        table.setItem(row, 3, QTableWidgetItem(cdate))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget