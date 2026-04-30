# ============================================
# ILASPP - GWR Analysis (FINAL - Berdasarkan Struktur Asli)
# ============================================

library(GWmodel)
library(sp)

cat("📊 GWR Analysis (GWmodel)\n")
cat("========================================\n")

# Load data
df <- read.csv("../data/processed/land_values_clean.csv")
cat("✅ Loaded", nrow(df), "records\n")

# Convert to SpatialPointsDataFrame
coordinates(df) <- ~longitude + latitude
proj4string(df) <- CRS("+init=epsg:4326")

# Project to UTM for accurate distance calculation
df_utm <- spTransform(df, CRS("+init=epsg:32748"))
cat("✅ Projected to UTM\n")

# Define formula
formula_gwr <- land_value ~ distance_center + road_width

# Bandwidth selection (adaptive)
cat("\n🔍 Selecting optimal bandwidth...\n")
bw <- bw.gwr(formula_gwr,
             data = df_utm,
             adaptive = TRUE,
             kernel = "gaussian")

cat("✅ Optimal bandwidth:", round(bw, 2), "\n")

# Run GWR
cat("\n📈 Running GWR...\n")
gwr_res <- gwr.basic(formula_gwr,
                     data = df_utm,
                     bw = bw,
                     adaptive = TRUE,
                     kernel = "gaussian")

# Extract results
gwr_df <- as.data.frame(gwr_res$SDF)

# Tambahkan koordinat
gwr_df$longitude <- coordinates(df_utm)[,1]
gwr_df$latitude <- coordinates(df_utm)[,2]

# ============ TAMPILKAN HASIL ============

cat("\n========== GLOBAL DIAGNOSTICS ==========\n")
cat("R²:", round(gwr_res$GW.diagnostic$R2, 4), "\n")
cat("Adjusted R²:", round(gwr_res$GW.diagnostic$R2adj, 4), "\n")
cat("AICc:", round(gwr_res$GW.diagnostic$AICc, 2), "\n")
cat("RSS:", round(gwr_res$GW.diagnostic$RSS, 2), "\n")

cat("\n========== KOEFISIEN SUMMARY ==========\n")

cat("\nIntercept:\n")
cat("  Mean:", round(mean(gwr_df$Intercept), 4), "\n")
cat("  Min:", round(min(gwr_df$Intercept), 4), "\n")
cat("  Max:", round(max(gwr_df$Intercept), 4), "\n")

cat("\ndistance_center (pengaruh jarak ke pusat):\n")
cat("  Mean:", round(mean(gwr_df$distance_center), 4), "\n")
cat("  Min:", round(min(gwr_df$distance_center), 4), "\n")
cat("  Max:", round(max(gwr_df$distance_center), 4), "\n")
cat("  % Negative (semakin jauh semakin murah):", 
    round(sum(gwr_df$distance_center < 0) / nrow(gwr_df) * 100, 1), "%\n")

cat("\nroad_width (pengaruh lebar jalan):\n")
cat("  Mean:", round(mean(gwr_df$road_width), 4), "\n")
cat("  Min:", round(min(gwr_df$road_width), 4), "\n")
cat("  Max:", round(max(gwr_df$road_width), 4), "\n")
cat("  % Positive (semakin lebar semakin mahal):", 
    round(sum(gwr_df$road_width > 0) / nrow(gwr_df) * 100, 1), "%\n")

cat("\n========== LOCAL R² ==========\n")
cat("  Mean:", round(mean(gwr_df$Local_R2), 4), "\n")
cat("  Min:", round(min(gwr_df$Local_R2), 4), "\n")
cat("  Max:", round(max(gwr_df$Local_R2), 4), "\n")
cat("  SD:", round(sd(gwr_df$Local_R2), 4), "\n")

cat("\n========== PREDIKSI & RESIDUAL ==========\n")
cat("Predicted values (yhat):", 
    round(min(gwr_df$yhat), 2), "-", 
    round(max(gwr_df$yhat), 2), "\n")
cat("Residuals:", 
    round(min(gwr_df$residual), 2), "-", 
    round(max(gwr_df$residual), 2), "\n")

# Identify dominant variable per location (variabel dengan pengaruh terbesar)
coeff_abs <- abs(gwr_df[, c("distance_center", "road_width")])
dominant_var <- c("distance_center", "road_width")[apply(coeff_abs, 1, which.max)]
gwr_df$dominant_variable <- dominant_var

cat("\n========== VARIABEL DOMINAN PER LOKASI ==========\n")
print(table(gwr_df$dominant_variable))

# Save results
write.csv(gwr_df, "output/gwr_coefficients.csv", row.names = FALSE)
cat("\n✅ GWR coefficients saved to: output/gwr_coefficients.csv\n")

# Create Local R² map
png("output/gwr_local_r2_map.png", width = 800, height = 600)
colors <- colorRampPalette(c("blue", "lightblue", "yellow", "red"))(100)
# Plot points colored by Local R²
plot(df_utm, col = colors[cut(gwr_df$Local_R2, 100, labels=FALSE)], 
     pch = 19, cex = 1.2, main = "Local R² - Model Quality per Location")
legend("bottomright", 
       legend = round(seq(min(gwr_df$Local_R2), max(gwr_df$Local_R2), length.out = 5), 2),
       fill = colors[seq(1, 100, length.out=5)], 
       title = "Local R²", cex = 0.8)
dev.off()
cat("✅ Local R² map saved to: output/gwr_local_r2_map.png\n")

# Create coefficient map for distance_center (most important variable)
png("output/gwr_distance_center_coef.png", width = 800, height = 600)
coef_colors <- colorRampPalette(c("red", "white", "blue"))(100)
plot(df_utm, col = coef_colors[cut(gwr_df$distance_center, 100, labels=FALSE)], 
     pch = 19, cex = 1.2, 
     main = "GWR Coefficient: Distance to Center (Semakin merah = pengaruh negatif kuat)")
legend("bottomright", 
       legend = round(seq(min(gwr_df$distance_center), max(gwr_df$distance_center), length.out = 5), 2),
       fill = coef_colors[seq(1, 100, length.out=5)], 
       title = "Coefficient", cex = 0.8)
dev.off()
cat("✅ Distance center coefficient map saved\n")

cat("\n========================================\n")
cat("✅ GWR Analysis Complete!\n")