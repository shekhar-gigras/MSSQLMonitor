from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QProgressBar
from db import DatabaseManager

def create_health_score_section():
    widget = QWidget()
    layout = QHBoxLayout(widget)
    layout.setContentsMargins(5, 5, 5, 5)
    
    label = QLabel("Server Overall Health Score:")
    label.setStyleSheet("font-weight: bold; font-size: 14px; color: #334155;")
    
    # Default Health Score
    health_score = 95
    
    try:
        db = DatabaseManager()
        # Check active blocking sessions to determine health impact
        query = """
            SELECT COUNT(*) AS BlockingCount 
            FROM sys.dm_os_waiting_tasks 
            WHERE blocking_session_id IS NOT NULL;
        """
        results = db.execute_query(query)
        if results:
            blocking_count = results[0].get('BlockingCount', 0)
            # Har blocking session par score deduct karein (minimum 0 tak)
            health_score = max(0, 100 - (blocking_count * 15))
    except Exception as e:
        print(f"Health Score Query Error: {e}")
    
    progress = QProgressBar()
    progress.setValue(health_score)
    progress.setTextVisible(True)
    
    # Dynamic Color based on Health Score
    chunk_color = "#22c55e" # Green (Healthy)
    if health_score < 50:
        chunk_color = "#ef4444" # Red (Critical)
    elif health_score < 80:
        chunk_color = "#f59e0b" # Yellow/Orange (Warning)
        
    progress.setStyleSheet(f"""
        QProgressBar {{
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            text-align: center;
            background: #e2e8f0;
            height: 22px;
            font-weight: bold;
            color: #0f172a;
        }}
        QProgressBar::chunk {{
            background-color: {chunk_color};
            border-radius: 5px;
        }}
    """)
    
    layout.addWidget(label)
    layout.addWidget(progress)
    return widget