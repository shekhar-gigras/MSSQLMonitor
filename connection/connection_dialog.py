import pyodbc
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QComboBox, QPushButton, QMessageBox, QFormLayout, QCheckBox
)
from PyQt6.QtCore import Qt
from .connection_manager import ConnectionManager

class ConnectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Connect to SQL Server")
        self.setFixedSize(420, 320)
        self.conn_manager = ConnectionManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Server Name Input
        self.server_input = QLineEdit(self.conn_manager.server)
        self.server_input.setPlaceholderText("e.g., localhost\\SQLEXPRESS or 192.168.1.50")
        form_layout.addRow(QLabel("Server Name:"), self.server_input)

        # Authentication Type Combo
        self.auth_combo = QComboBox()
        self.auth_combo.addItems(["Windows Authentication", "SQL Server Authentication"])
        if self.conn_manager.auth_type == "SQL Server":
            self.auth_combo.setCurrentIndex(1)
        self.auth_combo.currentIndexChanged.connect(self.toggle_auth_fields)
        form_layout.addRow(QLabel("Authentication:"), self.auth_combo)

        # Username & Password Inputs
        self.user_input = QLineEdit(self.conn_manager.username)
        self.user_input.setPlaceholderText("SQL Login username")
        
        self.pass_input = QLineEdit(self.conn_manager.password)
        self.pass_input.setPlaceholderText("SQL Login password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.user_label = QLabel("Login / Username:")
        self.pass_label = QLabel("Password:")

        form_layout.addRow(self.user_label, self.user_input)
        form_layout.addRow(self.pass_label, self.pass_input)

        # Extra Options: Encrypt & Trust Certificate Checkboxes
        self.encrypt_chk = QCheckBox("Force Encryption")
        self.encrypt_chk.setChecked(self.conn_manager.encrypt.lower() == "yes")
        
        self.trust_cert_chk = QCheckBox("Trust Server Certificate")
        self.trust_cert_chk.setChecked(self.conn_manager.trust_server_certificate.lower() == "yes")

        form_layout.addRow(QLabel("Security Options:"), self.encrypt_chk)
        form_layout.addRow(QLabel(""), self.trust_cert_chk)

        layout.addLayout(form_layout)

        # Action Buttons
        btn_layout = QHBoxLayout()
        self.test_btn = QPushButton("Test Connection")
        self.test_btn.clicked.connect(self.test_connection)
        
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.accept_connection)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(self.test_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.connect_btn)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)
        self.toggle_auth_fields()

    def toggle_auth_fields(self):
        is_sql = self.auth_combo.currentText() == "SQL Server Authentication"
        self.user_label.setVisible(is_sql)
        self.user_input.setVisible(is_sql)
        self.pass_label.setVisible(is_sql)
        self.pass_input.setVisible(is_sql)

    def get_current_credentials(self):
        self.conn_manager.server = self.server_input.text().strip()
        self.conn_manager.auth_type = "Windows" if self.auth_combo.currentIndex() == 0 else "SQL Server"
        self.conn_manager.username = self.user_input.text().strip()
        self.conn_manager.password = self.pass_input.text()
        
        # Save checkbox selections
        self.conn_manager.encrypt = "yes" if self.encrypt_chk.isChecked() else "no"
        self.conn_manager.trust_server_certificate = "yes" if self.trust_cert_chk.isChecked() else "no"

    def test_connection(self):
        self.get_current_credentials()
        conn_str = self.conn_manager.get_connection_string()
        try:
            conn = pyodbc.connect(conn_str, timeout=5)
            conn.close()
            QMessageBox.information(self, "Success", "Connection established successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Connection Failed", str(e))

    def accept_connection(self):
        self.get_current_credentials()
        conn_str = self.conn_manager.get_connection_string()
        try:
            conn = pyodbc.connect(conn_str, timeout=5)
            conn.close()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Connection Failed", f"Cannot connect to server:\n{e}")