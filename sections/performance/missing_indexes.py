from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_missing_indexes_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Top Missing Indexes (Performance Boost)")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["Database", "Table Name", "Estimated Impact"])
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
        SELECT TOP 10
            DB_NAME(mid.database_id) AS DatabaseName,
            mid.statement AS TableName,
            CAST(migs.avg_user_impact * (migs.user_seeks + migs.user_scans) AS DECIMAL(18,2)) AS EstimatedImpact
        FROM sys.dm_db_missing_index_group_stats migs
        JOIN sys.dm_db_missing_index_groups mig ON migs.group_handle = mig.index_group_handle
        JOIN sys.dm_db_missing_index_details mid ON mig.index_handle = mid.index_handle
        ORDER BY EstimatedImpact DESC;
    """
    results = db.execute_query(query)
    
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        dbname = str(record.get('DatabaseName') or record.get('databasename') or '')
        tbl = str(record.get('TableName') or record.get('tablename') or '')
        impact = str(record.get('EstimatedImpact') or record.get('estimatedimpact') or '0')
        
        table.setItem(row, 0, QTableWidgetItem(dbname))
        table.setItem(row, 1, QTableWidgetItem(tbl))
        table.setItem(row, 2, QTableWidgetItem(impact))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget