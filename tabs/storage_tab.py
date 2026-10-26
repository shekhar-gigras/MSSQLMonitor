from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from sections.storage.file_space_utilization import create_file_space_section
from sections.storage.index_fragmentation import create_index_fragmentation_section
from sections.storage.physical_drive_space import create_physical_drive_space_section
from sections.storage.file_autogrowth import create_file_autogrowth_section

def create_storage_tab():
    container = QWidget()
    main_layout = QVBoxLayout(container)
    main_layout.setSpacing(15)
    
    # Row 1: Physical Drive Space & File Space Utilization side-by-side
    row1_layout = QHBoxLayout()
    row1_layout.setSpacing(15)
    row1_layout.addWidget(create_physical_drive_space_section())
    row1_layout.addWidget(create_file_space_section())
    main_layout.addLayout(row1_layout)
    
    # Row 2: Auto-Growth Configuration & Index Fragmentation side-by-side
    row2_layout = QHBoxLayout()
    row2_layout.setSpacing(15)
    row2_layout.addWidget(create_file_autogrowth_section())
    row2_layout.addWidget(create_index_fragmentation_section())
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