from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from sections.administration.server_logins import create_server_logins_section
from sections.administration.mail_history import create_mail_history_section
from sections.administration.server_configurations import create_server_configurations_section
from sections.administration.linked_servers import create_linked_servers_section
from sections.administration.server_properties import create_server_properties_section
from sections.administration.error_logs import create_error_logs_section

def create_administration_tab():
    container = QWidget()
    main_layout = QVBoxLayout(container)
    main_layout.setSpacing(15)
    
    # Row 1: Server Logins & Database Mail History side-by-side
    row1_layout = QHBoxLayout()
    row1_layout.setSpacing(15)
    row1_layout.addWidget(create_server_logins_section())
    row1_layout.addWidget(create_mail_history_section())
    main_layout.addLayout(row1_layout)
    
    # Row 2: Server Properties (Collation, TempDB, Paths) & Server Configurations side-by-side
    row2_layout = QHBoxLayout()
    row2_layout.setSpacing(15)
    row2_layout.addWidget(create_server_properties_section())
    row2_layout.addWidget(create_server_configurations_section())
    main_layout.addLayout(row2_layout)
    
    # Row 3: Linked Servers Overview
    main_layout.addWidget(create_linked_servers_section())
    
    # Row 4: SQL Server Error Log Viewer below
    main_layout.addWidget(create_error_logs_section())
    
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