# ILASPP Data Preparation
library(DBI)
library(RPostgreSQL)

cat("ILASPP Data Preparation (R Version)\n")

conn <- dbConnect(
    PostgreSQL(),
    dbname = "atr_bpn_project",
    host = "localhost",
    user = "postgres",
    password = "s3cr3t_admin"
)

cat("Connected to database\n")

query <- "
    SELECT 
        id, district, zone_type,
        land_value_per_m2_juta as land_value,
        distance_to_center_km as distance_center,
        road_width_m as road_width,
        land_area_m2 as land_area,
        longitude, latitude
    FROM land_values
"

df <- dbGetQuery(conn, query)
cat("Loaded", nrow(df), "records\n")

write.csv(df, "../data/processed/land_values_clean.csv", row.names = FALSE)
cat("Saved to CSV\n")

library(sf)
df_sf <- st_as_sf(df, coords = c("longitude", "latitude"), crs = 4326)
st_write(df_sf, "../data/geodata/land_values.gpkg", delete_layer = TRUE)
cat("Saved to GeoPackage\n")

dbDisconnect(conn)
cat("Done\n")
