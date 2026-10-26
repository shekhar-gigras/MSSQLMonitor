from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from sections.maintenance.backup_history import create_backup_history_section
from sections.maintenance.maintenance_jobs import create_maintenance_jobs_section
from sections.maintenance.maintenance_plans import create_maintenance_plans_section
from sections.maintenance.dac_applications import create_dac_applications_section

def create_maintenance_tab():
    container = QWidget()
    main_layout = QVBoxLayout(container)
    main_layout.setSpacing(15)
    
    # Row 1: Backup History & Maintenance Jobs Status side-by-side
    row1_layout = QHBoxLayout()
    row1_layout.setSpacing(15)
    row1_layout.addWidget(create_backup_history_section())
    row1_layout.addWidget(create_maintenance_jobs_section())
    main_layout.addLayout(row1_layout)
    
    # Row 2: Maintenance Plans & DAC Applications (BACPAC) side-by-side
    row2_layout = QHBoxLayout()
    row2_layout.setSpacing(15)
    row2_layout.addWidget(create_maintenance_plans_section())
    row2_layout.addWidget(create_dac_applications_section())
    main_layout.addLayout(row2_layout)
    
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