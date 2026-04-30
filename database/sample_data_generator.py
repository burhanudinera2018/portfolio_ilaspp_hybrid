# database/sample_data_generator.py
import numpy as np
import pandas as pd
from db_connector import db


class SampleDataGenerator:
    @staticmethod
    def create_tables():
        """Membuat tabel dan sample data"""
        
        # Drop table if exists (optional, comment out if you want to keep data)
        # db.execute_query("DROP TABLE IF EXISTS land_values;", fetch=False)
        
        # Create table with geometry
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS land_values (
                id SERIAL PRIMARY KEY,
                district VARCHAR(100),
                land_area_m2 FLOAT,
                road_width_m FLOAT,
                distance_to_center_km FLOAT,
                zone_type VARCHAR(50),
                land_value_per_m2_juta FLOAT,
                latitude FLOAT,
                longitude FLOAT,
                geom GEOMETRY(Point, 4326)
            )
        """
        db.execute_query(create_table_sql, fetch=False)
        print("✅ Table 'land_values' created")
        
        # Check if table is empty
        count = db.fetch_one("SELECT COUNT(*) FROM land_values")[0]
        
        if count == 0:
            # Generate sample data
            SampleDataGenerator._insert_sample_data()
        else:
            print(f"ℹ️ Table already has {count} records, skipping sample data insertion")
        
        # Create indexes
        indexes_sql = """
            CREATE INDEX IF NOT EXISTS idx_land_values_geom 
                ON land_values USING GIST (geom);
            CREATE INDEX IF NOT EXISTS idx_land_values_district 
                ON land_values (district);
            CREATE INDEX IF NOT EXISTS idx_land_values_value 
                ON land_values (land_value_per_m2_juta);
        """
        db.execute_query(indexes_sql, fetch=False)
        print("✅ Indexes created")
    
    @staticmethod
    def _insert_sample_data():
        """Insert sample data into table"""
        np.random.seed(42)
        
        districts = ['Menteng', 'Kuningan', 'Sudirman', 'Kemayoran', 'Palmerah', 
                     'Cilandak', 'Pasar Minggu', 'Ciputat', 'Bintaro', 'Pondok Indah']
        zone_types = ['Komersial', 'Residensial', 'Industri', 'Campuran']
        
        n_points = 200
        inserted = 0
        
        print(f"📊 Generating {n_points} sample records...")
        
        for i in range(n_points):
            district = np.random.choice(districts)
            zone_type = np.random.choice(zone_types)
            
            # Generate realistic values
            distance_to_center = np.random.exponential(5)
            road_width = np.random.uniform(2, 30)
            land_area = np.random.uniform(60, 500)
            
            # Land value formula: higher when closer to center + wider road
            base_value = 20 - distance_to_center * 1.2
            base_value += road_width * 0.3
            if zone_type == 'Komersial':
                base_value += 15
            elif zone_type == 'Campuran':
                base_value += 5
            
            land_value = max(2, base_value + np.random.normal(0, 3))
            
            # Coordinates around Jakarta
            lon = np.random.uniform(106.7, 106.9)
            lat = np.random.uniform(-6.3, -6.1)
            
            insert_sql = """
                INSERT INTO land_values 
                (district, land_area_m2, road_width_m, distance_to_center_km,
                 zone_type, land_value_per_m2_juta, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 
                        ST_SetSRID(ST_MakePoint(%s, %s), 4326))
            """
            
            db.execute_query(insert_sql, (
                district, land_area, road_width, distance_to_center,
                zone_type, round(land_value, 2), lat, lon, lon, lat
            ), fetch=False)
            inserted += 1
            
            if (i + 1) % 50 == 0:
                print(f"   Inserted {i + 1}/{n_points} records...")
        
        print(f"✅ {inserted} sample records inserted")
    
    @staticmethod
    def get_sample_queries():
        """Contoh query untuk testing"""
        queries = {
            "top_10_value": """
                SELECT district, land_value_per_m2_juta, longitude, latitude
                FROM land_values 
                ORDER BY land_value_per_m2_juta DESC 
                LIMIT 10;
            """,
            "district_stats": """
                SELECT 
                    district,
                    COUNT(*) as property_count,
                    ROUND(AVG(land_value_per_m2_juta)::numeric, 2) as avg_value,
                    ROUND(MIN(land_value_per_m2_juta)::numeric, 2) as min_value,
                    ROUND(MAX(land_value_per_m2_juta)::numeric, 2) as max_value
                FROM land_values
                GROUP BY district
                ORDER BY avg_value DESC;
            """,
            "zone_stats": """
                SELECT 
                    zone_type,
                    COUNT(*) as count,
                    ROUND(AVG(land_value_per_m2_juta)::numeric, 2) as avg_value
                FROM land_values
                GROUP BY zone_type;
            """
        }
        return queries