from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from sections.overview.health_score import create_health_score_section
from sections.overview.kpi_section import create_kpi_section
from sections.overview.largest_databases import create_largest_databases_section
from sections.overview.database_chart import create_database_chart_section
from sections.overview.active_connections import create_active_connections_section

def create_overview_tab():
    widget = QWidget()
    main_layout = QVBoxLayout(widget)
    main_layout.setSpacing(15)
    
    # 1. Health Score Banner at Top
    main_layout.addWidget(create_health_score_section())
    
    # 2. KPI Cards Grid Row
    main_layout.addWidget(create_kpi_section())
    
    # 3. Bottom Grid: Largest Databases Table & Size Distribution Chart Side-by-Side
    bottom_layout = QHBoxLayout()
    bottom_layout.setSpacing(15)
    bottom_layout.addWidget(create_largest_databases_section())
    bottom_layout.addWidget(create_database_chart_section())
    main_layout.addLayout(bottom_layout)
    
    # 4. Active Connection User Details Section (Placed below Largest Databases & Chart)
    main_layout.addWidget(create_active_connections_section())
    
    return widget