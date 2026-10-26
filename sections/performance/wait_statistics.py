from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from db import DatabaseManager

def create_wait_statistics_section():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    
    title = QLabel("Top Wait Statistics")
    title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff; margin-bottom: 4px;")
    
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["Wait Type", "Wait Time (sec)", "Percentage"])
    table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    
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
        WITH Waits AS (
            SELECT 
                wait_type,
                wait_time_ms / 1000.0 AS WaitTimeSec,
                SUM(wait_time_ms) OVER() AS TotalWaitTimeMs
            FROM sys.dm_os_wait_stats
            WHERE wait_type NOT IN (
                'CLR_SEMAPHORE', 'LAZYWRITER_SLEEP', 'RESOURCE_QUEUE', 'SLEEP_TASK',
                'SLEEP_SYSTEMTASK', 'SQLTRACE_BUFFER_FLUSH', 'WAIT_XTP_HOST_WAIT',
                'WAIT_XTP_CKPT_CLOSE', 'WAIT_XTP_RECOVERY', 'XE_TIMER_EVENT', 'XE_DISPATCHER_WAIT'
            )
        )
        SELECT TOP 10
            wait_type AS WaitType,
            CAST(WaitTimeSec AS DECIMAL(10, 2)) AS WaitTimeSec,
            CAST(CASE WHEN TotalWaitTimeMs > 0 THEN (WaitTimeSec * 1000.0 / TotalWaitTimeMs) * 100 ELSE 0 END AS DECIMAL(5, 2)) AS Percentage
        FROM Waits
        ORDER BY WaitTimeSec DESC;
    """
    results = db.execute_query(query)
    
    table.setRowCount(len(results))
    for row, record in enumerate(results):
        w_type = str(record.get('WaitType') or record.get('waittype') or '')
        w_time = str(record.get('WaitTimeSec') or record.get('waittimesec') or '0')
        w_pct = f"{str(record.get('Percentage') or record.get('percentage') or '0')} %"
        
        table.setItem(row, 0, QTableWidgetItem(w_type))
        table.setItem(row, 1, QTableWidgetItem(w_time))
        table.setItem(row, 2, QTableWidgetItem(w_pct))
        
    layout.addWidget(title)
    layout.addWidget(table)
    return widget