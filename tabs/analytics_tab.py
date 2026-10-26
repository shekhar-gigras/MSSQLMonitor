from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from sections.analytics.active_sessions import create_active_sessions_section
from sections.analytics.top_queries import create_top_queries_section
from sections.analytics.missing_indexes import create_missing_indexes_section

def create_analysis_tab():
    container = QWidget()
    main_layout = QVBoxLayout(container)
    main_layout.setSpacing(15)
    
    # Row 1: Active Sessions & Missing Indexes side-by-side
    row1_layout = QHBoxLayout()
    row1_layout.setSpacing(15)
    row1_layout.addWidget(create_active_sessions_section())
    row1_layout.addWidget(create_missing_indexes_section())
    main_layout.addLayout(row1_layout)
    
    # Row 2: Top Resource-Intensive Queries below
    main_layout.addWidget(create_top_queries_section())
    
    # Wrap inside scroll area for neat scaling
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(container)
    scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
    
    wrapper = QWidget()
    wrapper_layout = QVBoxLayout(wrapper)
    wrapper_layout.setContentsMargins(0, 0, 0, 0)
    wrapper_layout.addWidget(scroll_area)
    
    return wrapper