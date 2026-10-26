import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QToolBar,
    QDialog,
    QWidget,
    QSizePolicy
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

from connection import ConnectionDialog
from tabs.overview_tab import create_overview_tab
from tabs.performance_tab import create_performance_tab
from tabs.storage_tab import create_storage_tab
from tabs.maintenance_tab import create_maintenance_tab
from tabs.administration_tab import create_administration_tab
from tabs.analytics_tab import create_analysis_tab


class Dashboard(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MSSQL Performance Dashboard")
        self.showMaximized()  # Opens the window in maximized mode
        self.switch_server_requested = False
        self.build_ui()

    def build_ui(self):
        # Top Toolbar for Control Actions
        toolbar = QToolBar("Server Toolbar")
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #1e293b;
                border-bottom: 1px solid #cbd5e1;
                padding: 6px;
            }
            QToolButton {
                color: #ffffff;
                font-weight: bold;
                font-size: 13px;
                padding: 6px 14px;
                border-radius: 4px;
                background-color: #334155;
                margin-right: 8px;
            }
            QToolButton:hover {
                background-color: #475569;
            }
        """)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # Expanding Spacer to push buttons to the right side
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)

        # 1. Change SQL Details Button
        switch_action = QAction("🔌 Change SQL Details", self)
        switch_action.triggered.connect(self.on_switch_server)
        toolbar.addAction(switch_action)

        # 2. Exit Button
        exit_action = QAction("❌ Exit", self)
        exit_action.triggered.connect(self.on_exit)
        toolbar.addAction(exit_action)

        # Tabs Setup
        tabs = QTabWidget()
        tabs.addTab(create_overview_tab(), "📊 Overview")
        tabs.addTab(create_performance_tab(), "⚡ Performance")
        tabs.addTab(create_storage_tab(), "💾 Storage")
        tabs.addTab(create_maintenance_tab(), "🛡 Maintenance")
        tabs.addTab(create_administration_tab(), "⚙ Administration")
        tabs.addTab(create_analysis_tab(), "📈 Analytics")

        # Apply styling for font type, font size, and background color
        stylesheet = """
            /* Background color of the main tab content area */
            QTabWidget::pane {
                border: 1px solid #cbd5e1;
                background-color: #f8fafc; 
            }
            
            /* Styling for individual tab headers */
            QTabBar::tab {
                font-family: 'Segoe UI', Arial, sans-serif; /* Font Type */
                font-size: 14px;                            /* Font Size */
                font-weight: bold;
                padding: 10px 20px;                        /* Tab padding */
                background-color: #e2e8f0;                  /* Unselected tab background */
                color: #334155;                            /* Text color */
                border: 1px solid #cbd5e1;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 3px;
            }
            
            /* Style for the active/selected tab */
            QTabBar::tab:selected {
                background-color: #ffffff;                  /* Selected tab background */
                color: #0f172a;                            /* Selected text color */
                border-bottom: 2px solid #2563eb;            /* Accent underline for active tab */
            }
            
            /* Hover effect when mouse is over a tab */
            QTabBar::tab:hover {
                background-color: #cbd5e1;
                color: #0f172a;
            }
        """
        
        tabs.setStyleSheet(stylesheet)
        self.setCentralWidget(tabs)

    def on_switch_server(self):
        """Triggered when user clicks 'Change SQL Details'."""
        self.switch_server_requested = True
        self.close()

    def on_exit(self):
        """Triggered when user clicks 'Exit'."""
        self.switch_server_requested = False
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Application loop to handle switching connection or terminating completely
    while True:
        conn_dialog = ConnectionDialog()
        if conn_dialog.exec() == QDialog.DialogCode.Accepted:
            window = Dashboard()
            window.show()
            app.exec()
            
            if window.switch_server_requested:
                continue
            else:
                break
        else:
            break
            
    sys.exit(0)