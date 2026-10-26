from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_top_queries_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Top Resource-Intensive Queries (CPU & Execution)")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(4)
    table.setHorizontalHeaderLabels(["Executions", "Total CPU (ms)", "Logical Reads", "Complete Query Text"])
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
    # Explicit CAST AS VARCHAR(MAX) ensures pyodbc fetches the full query text without truncation
    query = """
        SELECT TOP 20
            qs.execution_count AS ExecCount,
            qs.total_worker_time / 1000 AS TotalCPUMs,
            qs.total_logical_reads AS LogicalReads,
            CAST(
                CASE 
                    WHEN qs.statement_end_offset = -1 THEN 
                        SUBSTRING(st.text, (qs.statement_start_offset/2) + 1, 2147483647)
                    ELSE 
                        SUBSTRING(st.text, (qs.statement_start_offset/2) + 1, ((qs.statement_end_offset - qs.statement_start_offset)/2) + 1)
                END AS VARCHAR(MAX)
            ) AS QueryText
        FROM sys.dm_exec_query_stats qs
        CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) st
        ORDER BY qs.total_worker_time DESC;
    """
    try:
        results = db.execute_query(query)
    except Exception:
        results = []
        
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        ecount = str(record.get('ExecCount') or record.get('execcount') or '0')
        cpu = str(record.get('TotalCPUMs') or record.get('totalcpums') or '0')
        reads = str(record.get('LogicalReads') or record.get('logicalreads') or '0')
        
        raw_text = str(record.get('QueryText') or record.get('querytext') or 'N/A')
        # Clean multi-line breaks into a single continuous readable line
        qtext = ' '.join(raw_text.split())
        
        table.setItem(row, 0, QTableWidgetItem(ecount))
        table.setItem(row, 1, QTableWidgetItem(cpu))
        table.setItem(row, 2, QTableWidgetItem(reads))
        table.setItem(row, 3, QTableWidgetItem(qtext))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget