# database/init_db.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_connector import db
from sample_data_generator import SampleDataGenerator

def main():
    print("🚀 Initializing database...")
    print("="*40)
    
    # Connect to database
    if not db.connect():
        print("❌ Failed to connect. Check PostgreSQL is running.")
        return
    
    # Create PostGIS extension
    try:
        db.execute_query("CREATE EXTENSION IF NOT EXISTS postgis;", fetch=False)
        print("✅ PostGIS extension enabled")
    except Exception as e:
        print(f"⚠️ PostGIS extension: {e}")
    
    # Create tables and sample data
    SampleDataGenerator.create_tables()
    
    # Test query
    print("\n🔍 Testing connection...")
    try:
        result = db.fetch_one("SELECT COUNT(*) as count FROM land_values")
        print(f"✅ Database ready: {result[0]} records")
    except Exception as e:
        print(f"⚠️ Count query failed: {e}")

    # Show sample queries
    print("\n📊 Sample queries to test:")
    queries = SampleDataGenerator.get_sample_queries()
    for name, query in queries.items():
        print(f"\n--- {name} ---")
        try:
            df = db.to_dataframe(query)
            print(df.head())
        except Exception as e:
            print(f"⚠️ Query '{name}' failed: {e}")
    
    db.close()
    print("\n" + "="*40)
    print("✅ Database initialization complete!")

if __name__ == "__main__":
    main()