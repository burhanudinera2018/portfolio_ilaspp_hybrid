# ==============================================
# GWR ANALYSIS - ILASPP PROJECT (DATA REAL)
# ==============================================

library(spgwr)
library(sf)
library(ggplot2)
library(dplyr)

# Load data
df <- read.csv('data_gwr_final.csv')
cat("\n✅ Data loaded:", nrow(df), "kabupaten/kota\n")

# Konversi ke format spasial
df_sf <- st_as_sf(df, coords = c('Longitude', 'Latitude'), crs = 4326)
df_sp <- as(df_sf, 'Spatial')

# OLS (Global Regression) - baseline
ols_model <- lm(Y ~ X_jarak + X_lebar_jalan, data = df)
cat("\n========== OLS (GLOBAL REGRESSION) ==========\n")
print(summary(ols_model))

# Bandwidth Selection
cat("\n========== BANDWIDTH SELECTION ==========\n")
formula_gwr <- Y ~ X_jarak + X_lebar_jalan

bw <- gwr.sel(formula_gwr, 
              data = df_sp, 
              adapt = FALSE,
              verbose = FALSE)

cat("✅ Bandwidth optimal:", round(bw, 2), "meter\n")

# Run GWR
cat("\n========== RUNNING GWR ==========\n")
gwr_model <- gwr(formula_gwr,
                 data = df_sp,
                 bandwidth = bw,
                 hatmatrix = TRUE)

cat("\n========== GWR RESULTS ==========\n")
print(gwr_model)

# Perbandingan AIC
aic_ols <- AIC(ols_model)
aic_gwr <- gwr_model$results$AICc

cat("\n========== MODEL COMPARISON ==========\n")
cat("AIC OLS :", round(aic_ols, 2), "\n")
cat("AICc GWR:", round(aic_gwr, 2), "\n")
cat("Selisih (GWR - OLS):", round(aic_gwr - aic_ols, 2), "\n")

if (aic_gwr < aic_ols) {
  cat("✅ GWR lebih baik dari OLS (AIC lebih rendah)\n")
} else {
  cat("⚠️ OLS cukup, GWR tidak memberikan peningkatan signifikan\n")
}

# Ekstrak koefisien lokal
gwr_results <- as.data.frame(gwr_model$SDF)

# Tambahkan koefisien ke data
df$coef_jarak <- gwr_results$X_jarak
df$coef_lebar <- gwr_results$X_lebar_jalan
df$local_r2 <- gwr_results$localR2

# Tabel hasil per wilayah
cat("\n========== 10 WILAYAH DENGAN PENGARUH TERTINGGI ==========\n")
df_sorted <- df[order(-df$coef_lebar), ]
print(df_sorted[1:10, c('Kabupaten', 'coef_lebar', 'coef_jarak', 'local_r2')])

# Simpan hasil
write.csv(df, 'hasil_gwr_real.csv', row.names = FALSE)
cat("\n✅ Hasil GWR disimpan ke: hasil_gwr_real.csv\n")
