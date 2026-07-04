# ==============================================
# PETA GWR DENGAN GEOJSON ADM2 (KOLOM NAMA YANG BENAR)
# ==============================================

# 1. Load packages
library(sf)
library(ggplot2)
library(viridis)
library(dplyr)
library(scales)

# 2. Set working directory ke folder bnd
setwd("/Users/macos/Study_burhanudin_2025/geodata-master/bnd")
cat("✅ Working directory:", getwd(), "\n")

# 3. Load GeoJSON kabupaten/kota (adm2) dengan layer yang benar
gdf <- st_read("idn_bnd_adm2_2017_bps_a.json", layer = "idn_bnd_adm2_2017_bps_a")
cat("\n✅ GeoJSON loaded:", nrow(gdf), "polygons (kabupaten/kota)\n")

# 4. Kembali ke folder proyek
setwd("/Users/macos/Study_burhanudin_2025/Data Analytics/Portfolio Project/portfolio_ilaspp_hybrid")
cat("\n✅ Working directory:", getwd(), "\n")

# 5. Load hasil GWR
df <- read.csv('hasil_gwr_real.csv')
cat("\n✅ Data GWR loaded:", nrow(df), "kabupaten/kota\n")

# 6. Cek nama kolom di gdf
cat("\n📋 Nama kolom di gdf:\n")
print(names(gdf))

# 7. Kolom nama kabupaten/kota yang benar adalah A2N_BPS
# (A2N_BPS = Nama Kabupaten/Kota dari BPS)
kolom_nama_gdf <- "A2N_BPS"
cat("🔍 Menggunakan kolom:", kolom_nama_gdf, "\n")

# Bersihkan nama
df$nama_clean <- toupper(gsub("Kabupaten |Kota |Kab\\. |Kota ", "", df$Kabupaten))

# Untuk gdf, gunakan A2N_BPS
gdf$nama_clean <- toupper(gsub("Kabupaten |Kota |Kab\\. |Kota ", "", gdf[[kolom_nama_gdf]]))

# 8. Cek beberapa contoh nama untuk verifikasi
cat("\n🔍 Contoh nama dari GeoJSON:\n")
print(head(gdf$nama_clean))

cat("\n🔍 Contoh nama dari data GWR:\n")
print(head(df$nama_clean))

# 9. Gabungkan
gdf_merged <- merge(gdf, df, by = "nama_clean", all.x = TRUE)

cat("\n✅ Data gabungan:", nrow(gdf_merged), "polygons\n")
cat("✅ Wilayah dengan data GWR:", sum(!is.na(gdf_merged$coef_lebar)), "dari", nrow(gdf_merged), "\n")

# 10. Peta Koefisien Lebar Jalan
p1 <- ggplot() +
  geom_sf(data = gdf_merged, aes(fill = coef_lebar), color = "white", size = 0.1) +
  scale_fill_viridis_c(option = "plasma", 
                       name = "Koefisien\nLebar Jalan",
                       na.value = "grey90",
                       labels = comma) +
  labs(title = "Pengaruh Lebar Jalan terhadap Harga Kontrak Rumah",
       subtitle = "Hasil GWR - 85 Kabupaten/Kota di Indonesia",
       caption = "Data: BPS & BNPB | Metode: GWR") +
  theme_minimal() +
  theme(legend.position = "bottom",
        plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
        plot.subtitle = element_text(hjust = 0.5, size = 10),
        axis.text = element_blank(),
        axis.title = element_blank(),
        panel.grid = element_blank())

ggsave("peta_choropleth_lebar_jalan.png", p1, width = 12, height = 10, dpi = 150)
cat("\n✅ Peta 1: peta_choropleth_lebar_jalan.png\n")

# 11. Peta Local R²
p2 <- ggplot() +
  geom_sf(data = gdf_merged, aes(fill = local_r2), color = "white", size = 0.1) +
  scale_fill_viridis_c(option = "magma", 
                       name = "Local R²",
                       na.value = "grey90",
                       limits = c(0, 1),
                       labels = percent) +
  labs(title = "Kinerja Model GWR per Kabupaten/Kota",
       subtitle = "Semakin terang, semakin akurat model",
       caption = "Data: BPS & BNPB | Metode: GWR") +
  theme_minimal() +
  theme(legend.position = "bottom",
        plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
        plot.subtitle = element_text(hjust = 0.5, size = 10),
        axis.text = element_blank(),
        axis.title = element_blank(),
        panel.grid = element_blank())

ggsave("peta_choropleth_local_r2.png", p2, width = 12, height = 10, dpi = 150)
cat("✅ Peta 2: peta_choropleth_local_r2.png\n")

# 12. Gabungkan
if ("patchwork" %in% installed.packages()) {
  library(patchwork)
  p_combined <- p1 + p2 + 
    plot_annotation(title = "Hasil Analisis GWR - Proyek ILASPP",
                    subtitle = "85 Kabupaten/Kota di Indonesia")
  ggsave("peta_choropleth_combined.png", p_combined, width = 14, height = 10, dpi = 150)
  cat("✅ Peta gabungan: peta_choropleth_combined.png\n")
}

cat("\n📁 Semua peta tersimpan di:", getwd(), "\n")