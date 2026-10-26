from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_backup_history_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Database Backup History & DR Status")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Database Name", "Backup Type", "Last Backup Date", "Size (MB)"])
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
            d.name AS DatabaseName,
            CASE b.type 
                WHEN 'D' THEN 'Full Backup' 
                WHEN 'I' THEN 'Differential' 
                WHEN 'L' THEN 'Transaction Log' 
                ELSE 'No Backup' 
            END AS BackupType,
            ISNULL(CAST(b.backup_finish_date AS VARCHAR(30)), 'Never') AS LastBackupDate,
            CAST(ISNULL(b.backup_size, 0) * 1.0 / 1024 / 1024 AS DECIMAL(10,2)) AS BackupSizeMB
        FROM sys.databases d
        OUTER APPLY (
            SELECT TOP 1 type, backup_finish_date, backup_size
            FROM msdb.dbo.backupset
            WHERE database_name = d.name
            ORDER BY backup_finish_date DESC
        ) b
        WHERE d.database_id > 4;
    """
    results = db.execute_query(query)
    
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        dbname = str(record.get('DatabaseName') or record.get('databasename') or '')
        btype = str(record.get('BackupType') or record.get('backuptype') or '')
        bdate = str(record.get('LastBackupDate') or record.get('lastbackupdate') or '')
        bsize = str(record.get('BackupSizeMB') or record.get('backupsizemb') or '0')
        
        table.setItem(row, 0, QTableWidgetItem(dbname))
        table.setItem(row, 1, QTableWidgetItem(btype))
        table.setItem(row, 2, QTableWidgetItem(bdate))
        table.setItem(row, 3, QTableWidgetItem(bsize))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget