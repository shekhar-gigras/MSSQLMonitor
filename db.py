import pyodbc
from connection import ConnectionManager

class DatabaseManager:
    def __init__(self):
        self.conn_manager = ConnectionManager()

    def get_connection(self):
        conn_str = self.conn_manager.get_connection_string()
        return pyodbc.connect(conn_str)
        
    def execute_query(self, query):
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            
            # Agar query se koi result set nahi milta (jaise non-SELECT statements)
            if not cursor.description:
                conn.commit()
                return []
                
            # Columns name extract karke dictionary mein map karna taaki record.get('ColName') chal sake
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
                
            return results
            
        except Exception as e:
            print(f"Query execution error: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()