from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_linked_servers_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Linked Servers Overview")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Server Name", "Product", "Provider", "Data Source"])
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
        SELECT 
            name AS ServerName,
            ISNULL(product, 'N/A') AS Product,
            ISNULL(provider, 'N/A') AS Provider,
            ISNULL(data_source, 'N/A') AS DataSource
        FROM sys.servers
        WHERE server_id != 0;
    """
    try:
        results = db.execute_query(query)
    except Exception:
        results = []
        
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        sname = str(record.get('ServerName') or record.get('servername') or '')
        prod = str(record.get('Product') or record.get('product') or '')
        prov = str(record.get('Provider') or record.get('provider') or '')
        dsrc = str(record.get('DataSource') or record.get('datasource') or '')
        
        table.setItem(row, 0, QTableWidgetItem(sname))
        table.setItem(row, 1, QTableWidgetItem(prod))
        table.setItem(row, 2, QTableWidgetItem(prov))
        table.setItem(row, 3, QTableWidgetItem(dsrc))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget