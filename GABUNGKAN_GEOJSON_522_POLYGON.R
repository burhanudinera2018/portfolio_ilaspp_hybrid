# ==============================================
# GABUNGKAN GEOJSON 522 POLYGON DENGAN DATA GWR
# ==============================================

# 1. Set working directory ke folder bnd (PATH YANG BENAR)
setwd("/Users/macos/Study_burhanudin_2025/geodata-master/bnd")
cat("✅ Working directory:", getwd(), "\n")

# 2. Cek file yang tersedia
cat("\n📋 File yang tersedia di folder bnd:\n")
list.files(pattern = ".json")

# 3. Load GeoJSON - GUNAKAN NAMA FILE YANG BENAR
gdf <- st_read("idn_bnd_adm2_2017_bps_a.json", layer = "idn_bnd_adm2_2017_bps_a")
cat("\n✅ GeoJSON loaded:", nrow(gdf), "polygons (kabupaten/kota)\n")

# 4. Cek nama kolom di gdf
cat("\n📋 Nama kolom di gdf:\n")
print(names(gdf))

# 5. Kembali ke folder proyek
setwd("/Users/macos/Study_burhanudin_2025/Data Analytics/Portfolio Project/portfolio_ilaspp_hybrid")
cat("\n✅ Working directory:", getwd(), "\n")

# 6. Load hasil GWR
df <- read.csv('hasil_gwr_real.csv')
cat("\n✅ Data GWR loaded:", nrow(df), "kabupaten/kota\n")

# 7. Bersihkan nama untuk matching
df$nama_clean <- toupper(gsub("Kabupaten |Kota |Kab\\. |Kota ", "", df$Kabupaten))

# Cari kolom nama di gdf
kolom_nama_gdf <- "A2N_BPS"  # Nama Kabupaten/Kota dari BPS
gdf$nama_clean <- toupper(gsub("Kabupaten |Kota |Kab\\. |Kota ", "", gdf[[kolom_nama_gdf]]))

# 8. Gabungkan
gdf_merged <- merge(gdf, df, by = "nama_clean", all.x = TRUE)

cat("\n✅ Data gabungan:", nrow(gdf_merged), "polygons\n")
cat("✅ Wilayah dengan data GWR:", sum(!is.na(gdf_merged$coef_lebar)), "dari", nrow(gdf_merged), "\n")

# 9. Peta Koefisien Lebar Jalan
library(ggplot2)
library(viridis)
library(scales)

p1 <- ggplot() +
  geom_sf(data = gdf_merged, aes(fill = coef_lebar), color = "white", size = 0.1) +
  scale_fill_viridis_c(option = "plasma", 
                       name = "Koefisien\nLebar Jalan",
                       na.value = "grey90",
                       labels = comma) +
  labs(title = "Pengaruh Lebar Jalan terhadap Harga Kontrak Rumah",
       subtitle = "Hasil GWR - 85 Kabupaten/Kota dari 522 di Indonesia",
       caption = "Data: BPS & BNPB | Metode: GWR | Area abu-abu = belum ada data") +
  theme_minimal() +
  theme(legend.position = "bottom",
        plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
        plot.subtitle = element_text(hjust = 0.5, size = 10),
        axis.text = element_blank(),
        axis.title = element_blank(),
        panel.grid = element_blank())

ggsave("peta_choropleth_lebar_jalan_full.png", p1, width = 12, height = 10, dpi = 150)
cat("\n✅ Peta 1: peta_choropleth_lebar_jalan_full.png\n")

# 10. Peta Local R²
p2 <- ggplot() +
  geom_sf(data = gdf_merged, aes(fill = local_r2), color = "white", size = 0.1) +
  scale_fill_viridis_c(option = "magma", 
                       name = "Local R²",
                       na.value = "grey90",
                       limits = c(0, 1),
                       labels = percent) +
  labs(title = "Kinerja Model GWR per Kabupaten/Kota",
       subtitle = "Semakin terang, semakin akurat model",
       caption = "Data: BPS & BNPB | Metode: GWR | Area abu-abu = belum ada data") +
  theme_minimal() +
  theme(legend.position = "bottom",
        plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
        plot.subtitle = element_text(hjust = 0.5, size = 10),
        axis.text = element_blank(),
        axis.title = element_blank(),
        panel.grid = element_blank())

ggsave("peta_choropleth_local_r2_full.png", p2, width = 12, height = 10, dpi = 150)
cat("✅ Peta 2: peta_choropleth_local_r2_full.png\n")

# 11. Gabungkan
if ("patchwork" %in% installed.packages()) {
  library(patchwork)
  p_combined <- p1 + p2 + 
    plot_annotation(title = "Hasil Analisis GWR - Proyek ILASPP",
                    subtitle = "85 Kabupaten/Kota dari 522 di Indonesia")
  ggsave("peta_choropleth_combined_full.png", p_combined, width = 14, height = 10, dpi = 150)
  cat("✅ Peta gabungan: peta_choropleth_combined_full.png\n")
}

cat("\n📁 Semua peta tersimpan di:", getwd(), "\n")