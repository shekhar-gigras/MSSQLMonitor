from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt6.QtCore import Qt
from sections.performance.cpu_queries import create_cpu_queries_section
from sections.performance.wait_statistics import create_wait_statistics_section
from sections.performance.blocking_sessions import create_blocking_sessions_section
from sections.performance.long_running_queries import create_long_running_queries_section
from sections.performance.missing_indexes import create_missing_indexes_section
from sections.performance.tempdb_usage import create_tempdb_usage_section

def create_performance_tab():
    # Main container widget
    container = QWidget()
    main_layout = QVBoxLayout(container)
    main_layout.setSpacing(15)
    
    # Row 1: CPU Queries & Wait Statistics
    row1_layout = QHBoxLayout()
    row1_layout.setSpacing(15)
    row1_layout.addWidget(create_cpu_queries_section())
    row1_layout.addWidget(create_wait_statistics_section())
    main_layout.addLayout(row1_layout)
    
    # Row 2: Blocking Sessions & Long Running Queries
    row2_layout = QHBoxLayout()
    row2_layout.setSpacing(15)
    row2_layout.addWidget(create_blocking_sessions_section())
    row2_layout.addWidget(create_long_running_queries_section())
    main_layout.addLayout(row2_layout)
    
    # Row 3: Missing Indexes & TempDB Usage
    row3_layout = QHBoxLayout()
    row3_layout.setSpacing(15)
    row3_layout.addWidget(create_missing_indexes_section())
    row3_layout.addWidget(create_tempdb_usage_section())
    main_layout.addLayout(row3_layout)
    
    # Wrap inside a QScrollArea for smooth professional scrolling
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(container)
    scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
    
    # Final wrapper widget for the tab
    wrapper = QWidget()
    wrapper_layout = QVBoxLayout(wrapper)
    wrapper_layout.setContentsMargins(0, 0, 0, 0)
    wrapper_layout.addWidget(scroll_area)
    
    return wrapper