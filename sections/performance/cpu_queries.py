from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_cpu_queries_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Top CPU Consuming Queries (Complete Text)")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["Complete Query Text", "Execution Count", "Total CPU (ms)"])
    table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    
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
    # Explicit CAST AS VARCHAR(MAX) ensures pyodbc fetches the full query without truncation
    query = """
        SELECT TOP 10
            CAST(
                CASE 
                    WHEN qs.statement_end_offset = -1 THEN 
                        SUBSTRING(st.text, (qs.statement_start_offset/2) + 1, 2147483647)
                    ELSE 
                        SUBSTRING(st.text, (qs.statement_start_offset/2) + 1, ((qs.statement_end_offset - qs.statement_start_offset)/2) + 1)
                END AS VARCHAR(MAX)
            ) AS QueryText,
            qs.execution_count AS ExecutionCount,
            qs.total_worker_time / 1000 AS TotalCPUMs
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
        raw_text = str(record.get('QueryText') or record.get('querytext') or 'N/A')
        # Extra line breaks ko single space mein convert karna taaki table cell mein clean dikhe
        q_text = ' '.join(raw_text.split())
        
        exec_count = str(record.get('ExecutionCount') or record.get('executioncount') or '0')
        cpu_ms = str(record.get('TotalCPUMs') or record.get('totalcpums') or '0')
        
        table.setItem(row, 0, QTableWidgetItem(q_text))
        table.setItem(row, 1, QTableWidgetItem(exec_count))
        table.setItem(row, 2, QTableWidgetItem(cpu_ms))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget