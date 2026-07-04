# ==============================================
# BUBBLE MAP - VISUALISASI GWR TANPA GEOJSON
# ==============================================

# 1. Load packages
library(ggplot2)
library(viridis)
library(scales)

# 2. Load data hasil GWR
df <- read.csv('hasil_gwr_real.csv')
cat("✅ Data loaded:", nrow(df), "kabupaten/kota\n")

# 3. Tampilkan struktur data
head(df)

# 4. Bubble Map Koefisien Lebar Jalan
p1 <- ggplot(df, aes(x = Longitude, y = Latitude)) +
  geom_point(aes(size = coef_lebar, 
                 color = coef_lebar,
                 text = paste(Kabupaten, "\nKoefisien:", round(coef_lebar, 0))),
             alpha = 0.8) +
  scale_size_continuous(range = c(3, 18), 
                        name = "Koefisien\nLebar Jalan",
                        labels = comma) +
  scale_color_viridis_c(option = "plasma", 
                        name = "Koefisien\nLebar Jalan",
                        labels = comma) +
  labs(title = "Pengaruh Lebar Jalan terhadap Harga Kontrak Rumah",
       subtitle = "Hasil GWR - 85 Kabupaten/Kota di Indonesia",
       x = "Longitude", 
       y = "Latitude",
       caption = "Data: BPS & BNPB | Metode: GWR | Ukuran titik = besaran koefisien") +
  theme_minimal() +
  theme(legend.position = "bottom",
        plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
        plot.subtitle = element_text(hjust = 0.5, size = 10),
        legend.key.width = unit(1.5, "cm"))

# 5. Simpan
ggsave("bubble_map_lebar_jalan.png", p1, width = 12, height = 8, dpi = 150)
cat("✅ Bubble Map 1: bubble_map_lebar_jalan.png\n")

# 6. Bubble Map Local R²
p2 <- ggplot(df, aes(x = Longitude, y = Latitude)) +
  geom_point(aes(size = local_r2, 
                 color = local_r2,
                 text = paste(Kabupaten, "\nLocal R²:", round(local_r2, 3))),
             alpha = 0.8) +
  scale_size_continuous(range = c(3, 18), 
                        name = "Local R²",
                        labels = percent) +
  scale_color_viridis_c(option = "magma", 
                        name = "Local R²",
                        limits = c(0, 1),
                        labels = percent) +
  labs(title = "Kinerja Model GWR per Kabupaten/Kota",
       subtitle = "Semakin besar titik, semakin akurat model di wilayah tersebut",
       x = "Longitude", 
       y = "Latitude",
       caption = "Local R² mendekati 1 = model sangat akurat") +
  theme_minimal() +
  theme(legend.position = "bottom",
        plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
        plot.subtitle = element_text(hjust = 0.5, size = 10),
        legend.key.width = unit(1.5, "cm"))

ggsave("bubble_map_local_r2.png", p2, width = 12, height = 8, dpi = 150)
cat("✅ Bubble Map 2: bubble_map_local_r2.png\n")

# 7. Bubble Map Koefisien Jarak
p3 <- ggplot(df, aes(x = Longitude, y = Latitude)) +
  geom_point(aes(size = abs(coef_jarak), 
                 color = coef_jarak,
                 text = paste(Kabupaten, "\nKoefisien Jarak:", round(coef_jarak, 0))),
             alpha = 0.8) +
  scale_size_continuous(range = c(3, 18), 
                        name = "|Koef. Jarak|") +
  scale_color_gradient2(low = "blue", mid = "white", high = "red", 
                        midpoint = -2000,
                        name = "Koefisien\nJarak") +
  labs(title = "Pengaruh Jarak ke Pusat Kota terhadap Harga Kontrak Rumah",
       subtitle = "Warna biru = negatif (semakin jauh semakin murah)",
       x = "Longitude", 
       y = "Latitude",
       caption = "Data: BPS & BNPB | Metode: GWR") +
  theme_minimal() +
  theme(legend.position = "bottom",
        plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
        plot.subtitle = element_text(hjust = 0.5, size = 10),
        legend.key.width = unit(1.5, "cm"))

ggsave("bubble_map_koefisien_jarak.png", p3, width = 12, height = 8, dpi = 150)
cat("✅ Bubble Map 3: bubble_map_koefisien_jarak.png\n")

# 8. Gabungkan semua dengan patchwork (opsional)
if ("patchwork" %in% installed.packages()) {
  library(patchwork)
  p_combined <- (p1 + p2) / (p3 + plot_spacer()) +
    plot_annotation(title = "Hasil Analisis GWR - Proyek ILASPP",
                    subtitle = "85 Kabupaten/Kota di Indonesia")
  ggsave("bubble_maps_combined.png", p_combined, width = 14, height = 12, dpi = 150)
  cat("✅ Gabungan: bubble_maps_combined.png\n")
}

cat("\n📁 Semua peta tersimpan di:", getwd(), "\n")
cat("\n📋 File yang dihasilkan:\n")
cat("  - bubble_map_lebar_jalan.png\n")
cat("  - bubble_map_local_r2.png\n")
cat("  - bubble_map_koefisien_jarak.png\n")
if ("patchwork" %in% installed.packages()) {
  cat("  - bubble_maps_combined.png\n")
}