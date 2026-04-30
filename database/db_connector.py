# database/db_connector.py
import psycopg2
import psycopg2.extras
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PostGISConnector:
    def __init__(self):
        self.conn_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'atr_bpn_project'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'postgres')
        }
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Membuat koneksi ke PostgreSQL dengan PostGIS"""
        try:
            self.connection = psycopg2.connect(**self.conn_params)
            self.connection.autocommit = False
            self.cursor = self.connection.cursor()
            print("✅ Database connected")
            return True
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False
    
    def close(self):
        """Menutup koneksi"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed")
    
    def execute_query(self, query, params=None, fetch=False):
        """
        Eksekusi query SQL
        
        Args:
            query: SQL query string
            params: Parameter untuk query (optional)
            fetch: Jika True, return hasil query
        """
        try:
            self.cursor.execute(query, params)
            
            if fetch:
                result = self.cursor.fetchall()
                return result
            else:
                self.connection.commit()
                return True
                
        except Exception as e:
            self.connection.rollback()
            print(f"❌ Query error: {e}")
            raise e
    
    def fetch_all(self, query, params=None):
        """Eksekusi query dan return semua hasil"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def fetch_one(self, query, params=None):
        """Eksekusi query dan return satu hasil"""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def to_dataframe(self, query):
        """Eksekusi query dan return sebagai Pandas DataFrame"""
        return pd.read_sql(query, self.connection)
    
    def get_table_info(self, table_name):
        """Mendapatkan informasi skema tabel"""
        query = f"""
            SELECT 
                column_name,
                data_type,
                is_nullable
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
        """
        return self.to_dataframe(query)
    
    def table_exists(self, table_name):
        """Cek apakah tabel ada di database"""
        query = """
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            )
        """
        result = self.fetch_one(query, (table_name,))
        return result[0] if result else False

# Singleton instance
db = PostGISConnector()