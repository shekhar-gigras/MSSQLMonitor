from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_maintenance_plans_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("SQL Server Maintenance Plans & Packages")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["Plan Name", "Sub-Plan Name", "Description"])
    table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
    
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
            ISNULL(p.name, 'N/A') AS PlanName,
            ISNULL(s.subplan_name, 'N/A') AS SubPlanName,
            ISNULL(p.description, 'No Description') AS Description
        FROM msdb.dbo.sysmaintplan_plans p
        LEFT JOIN msdb.dbo.sysmaintplan_subplans s ON p.id = s.plan_id;
    """
    results = db.execute_query(query)
    
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        pname = str(record.get('PlanName') or record.get('planname') or '')
        subname = str(record.get('SubPlanName') or record.get('subplanname') or '')
        desc = str(record.get('Description') or record.get('description') or '')
        
        table.setItem(row, 0, QTableWidgetItem(pname))
        table.setItem(row, 1, QTableWidgetItem(subname))
        table.setItem(row, 2, QTableWidgetItem(desc))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget