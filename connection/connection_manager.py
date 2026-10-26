class ConnectionManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConnectionManager, cls).__new__(cls)
            cls._instance.server = "localhost"
            cls._instance.database = "master"
            cls._instance.auth_type = "Windows"
            cls._instance.username = ""
            cls._instance.password = ""
            cls._instance.encrypt = "yes"                 # Default encryption setting
            cls._instance.trust_server_certificate = "yes"# Default trust certificate setting
        return cls._instance
    
    def get_connection_string(self):
        self.server = "server.yelawola.com,51433"
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"Encrypt={self.encrypt};"
            f"TrustServerCertificate={self.trust_server_certificate};"
        )
        
        self.username = "sa"
        self.password = "EhkeZcl(n7@C"
        self.auth_type = "SQL Server"  # Change to "Windows" for Windows Authentication
        if self.auth_type == "Windows":
            conn_str += "Trusted_Connection=no;"
        else:
            conn_str += f"UID={self.username};PWD={self.password};"
        # Console par connection string display karne ke liye:
        #print("--- Generated Connection String ---")
        #print(conn_str)
        #print("-----------------------------------")    
        return conn_str