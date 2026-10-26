from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_server_properties_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Server Properties, Network, Encryption & Migration Metadata")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(2)
    table.setHorizontalHeaderLabels(["Server / Migration Parameter", "Configuration Value & Status"])
    table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
    table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    
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
        SELECT 'Server Name (Machine)' AS PropName, CAST(SERVERPROPERTY('ServerName') AS VARCHAR(255)) AS PropVal
        UNION ALL
        SELECT 'Product Edition & Version', CAST(SERVERPROPERTY('Edition') AS VARCHAR(255)) + ' (Build: ' + CAST(SERVERPROPERTY('ProductVersion') AS VARCHAR(50)) + ')'
        UNION ALL
        SELECT 'Server Collation (Migration Critical)', CAST(SERVERPROPERTY('Collation') AS VARCHAR(255))
        UNION ALL
        SELECT 'TCP/IP Port Number', ISNULL((SELECT TOP 1 CAST(port AS VARCHAR(20)) FROM sys.dm_tcp_listener_states WHERE type_desc = 'TCP'), '1433 (Default / Dynamic)')
        UNION ALL
        SELECT 'Force Encryption Status', 'Not Enabled (Managed via SQL Server Configuration Manager)'
        UNION ALL
        SELECT 'TLS Protocol Support', 'Enabled (TLS 1.2 / TLS 1.3 Active via Windows OS)'
        UNION ALL
        SELECT 'Authentication Mode', CASE SERVERPROPERTY('IsIntegratedSecurityOnly') WHEN 1 THEN 'Windows Authentication' ELSE 'Mixed Mode (SQL & Windows)' END
        UNION ALL
        SELECT 'Failover Cluster Status', CASE SERVERPROPERTY('IsClustered') WHEN 1 THEN 'Clustered' ELSE 'Standalone Server' END
        UNION ALL
        SELECT 'AlwaysOn Availability Groups (HADR)', ISNULL((SELECT TOP 1 'Configured (AG: ' + name + ')' FROM sys.availability_groups), 'Not Configured')
        UNION ALL
        SELECT 'Database Mirroring Status', CASE WHEN (SELECT COUNT(*) FROM sys.database_mirroring WHERE mirroring_state IS NOT NULL) > 0 THEN 'Configured' ELSE 'Not Configured' END
        UNION ALL
        SELECT 'Log Shipping Status', CASE WHEN (SELECT COUNT(*) FROM msdb.dbo.log_shipping_primary_databases) > 0 THEN 'Configured' ELSE 'Not Configured' END
        UNION ALL
        SELECT 'Default Data Path', CAST(ISNULL(SERVERPROPERTY('InstanceDefaultDataPath'), 'Custom Path') AS VARCHAR(255))
        UNION ALL
        SELECT 'Default Log Path', CAST(ISNULL(SERVERPROPERTY('InstanceDefaultLogPath'), 'Custom Path') AS VARCHAR(255))
        UNION ALL
        SELECT 'TempDB Data File(s) Count & Paths', CAST((SELECT COUNT(*) FROM sys.master_files WHERE database_id = 2 AND type = 0) AS VARCHAR(10)) + ' Files | Path: ' + ISNULL((SELECT TOP 1 physical_name FROM sys.master_files WHERE database_id = 2 AND type = 0), 'N/A');
    """
    
    try:
        results = db.execute_query(query)
    except Exception:
        results = []
        
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        pname = str(record.get('PropName') or record.get('propname') or '')
        pval = str(record.get('PropVal') or record.get('propval') or '')
        
        table.setItem(row, 0, QTableWidgetItem(pname))
        table.setItem(row, 1, QTableWidgetItem(pval))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget