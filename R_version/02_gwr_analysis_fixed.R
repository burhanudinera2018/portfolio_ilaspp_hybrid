# ============================================
# ILASPP - GWR Analysis (FIXED - dengan nama variabel yang BENAR)
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

# Extract results from SDF
gwr_df <- as.data.frame(gwr_res$SDF)

# Tambahkan koordinat
gwr_df$longitude <- coordinates(df_utm)[,1]
gwr_df$latitude <- coordinates(df_utm)[,2]

# ============ GLOBAL DIAGNOSTICS (dengan nama yang BENAR) ============
cat("\n========== GLOBAL DIAGNOSTICS ==========\n")
cat("R² (gw.R2):", round(gwr_res$GW.diagnostic$gw.R2, 4), "\n")
cat("Adjusted R² (gwR2.adj):", round(gwr_res$GW.diagnostic$gwR2.adj, 4), "\n")
cat("AIC:", round(gwr_res$GW.diagnostic$AIC, 2), "\n")
cat("AICc:", round(gwr_res$GW.diagnostic$AICc, 2), "\n")  # Perbaikan: AICC bukan AICc
cat("BIC:", round(gwr_res$GW.diagnostic$BIC, 2), "\n")
cat("RSS.gw:", round(gwr_res$GW.diagnostic$RSS.gw, 2), "\n")
cat("enp:", round(gwr_res$GW.diagnostic$enp, 2), "\n")
cat("edf:", round(gwr_res$GW.diagnostic$edf, 2), "\n")

# ============ KOEFISIEN SUMMARY ============
cat("\n========== KOEFISIEN SUMMARY ==========\n")

cat("\nIntercept:\n")
cat("  Mean:", round(mean(gwr_df$Intercept), 4), "\n")
cat("  Min:", round(min(gwr_df$Intercept), 4), "\n")
cat("  Max:", round(max(gwr_df$Intercept), 4), "\n")
cat("  SD:", round(sd(gwr_df$Intercept), 4), "\n")

cat("\ndistance_center:\n")
cat("  Mean:", round(mean(gwr_df$distance_center), 4), "\n")
cat("  Min:", round(min(gwr_df$distance_center), 4), "\n")
cat("  Max:", round(max(gwr_df$distance_center), 4), "\n")
cat("  SD:", round(sd(gwr_df$distance_center), 4), "\n")
pct_neg <- round(sum(gwr_df$distance_center < 0) / nrow(gwr_df) * 100, 1)
cat("  % Negative (semakin jauh semakin murah):", pct_neg, "%\n")

cat("\nroad_width:\n")
cat("  Mean:", round(mean(gwr_df$road_width), 4), "\n")
cat("  Min:", round(min(gwr_df$road_width), 4), "\n")
cat("  Max:", round(max(gwr_df$road_width), 4), "\n")
cat("  SD:", round(sd(gwr_df$road_width), 4), "\n")
pct_pos <- round(sum(gwr_df$road_width > 0) / nrow(gwr_df) * 100, 1)
cat("  % Positive (semakin lebar semakin mahal):", pct_pos, "%\n")

# ============ LOCAL R² ============
cat("\n========== LOCAL R² ==========\n")
if("Local_R2" %in% names(gwr_df)) {
    cat("  Mean:", round(mean(gwr_df$Local_R2, na.rm=TRUE), 4), "\n")
    cat("  Min:", round(min(gwr_df$Local_R2, na.rm=TRUE), 4), "\n")
    cat("  Max:", round(max(gwr_df$Local_R2, na.rm=TRUE), 4), "\n")
    cat("  SD:", round(sd(gwr_df$Local_R2, na.rm=TRUE), 4), "\n")
} else {
    cat("  Local_R2 column not found\n")
}

# ============ PREDIKSI vs AKTUAL ============
cat("\n========== PREDIKSI vs AKTUAL ==========\n")
if("yhat" %in% names(gwr_df) && "y" %in% names(gwr_df)) {
    cat("Actual values:", round(min(gwr_df$y), 2), "-", round(max(gwr_df$y), 2), "\n")
    cat("Predicted values:", round(min(gwr_df$yhat), 2), "-", round(max(gwr_df$yhat), 2), "\n")
    cat("Residuals:", round(min(gwr_df$residual), 2), "-", round(max(gwr_df$residual), 2), "\n")
    
    ss_res <- sum((gwr_df$y - gwr_df$yhat)^2)
    ss_tot <- sum((gwr_df$y - mean(gwr_df$y))^2)
    r2_simple <- 1 - ss_res/ss_tot
    cat("\nR² (dari prediksi):", round(r2_simple, 4), "\n")
}

# ============ VARIABEL DOMINAN ============
coeff_abs <- abs(gwr_df[, c("distance_center", "road_width")])
dominant_var <- c("distance_center", "road_width")[apply(coeff_abs, 1, which.max)]
gwr_df$dominant_variable <- dominant_var

cat("\n========== VARIABEL DOMINAN PER LOKASI ==========\n")
print(table(gwr_df$dominant_variable))

# ============ SAVE RESULTS ============
write.csv(gwr_df, "output/gwr_coefficients.csv", row.names = FALSE)
cat("\n✅ GWR coefficients saved to: output/gwr_coefficients.csv\n")

# ============ CREATE VISUALIZATIONS ============

# 1. Local R² map
if("Local_R2" %in% names(gwr_df)) {
    png("output/gwr_local_r2_map.png", width = 800, height = 600)
    colors <- colorRampPalette(c("blue", "lightblue", "yellow", "red"))(100)
    plot(df_utm, col = colors[cut(gwr_df$Local_R2, 100, labels=FALSE)], 
         pch = 19, cex = 1.2, main = "Local R² - Model Quality per Location")
    legend("bottomright", 
           legend = round(seq(min(gwr_df$Local_R2), max(gwr_df$Local_R2), length.out = 5), 3),
           fill = colors[seq(1, 100, length.out=5)], 
           title = "Local R²", cex = 0.8)
    dev.off()
    cat("✅ Local R² map saved\n")
}

# 2. Distance Center coefficient map
png("output/gwr_distance_center_coef.png", width = 800, height = 600)
coef_colors <- colorRampPalette(c("red", "white", "blue"))(100)
plot(df_utm, col = coef_colors[cut(gwr_df$distance_center, 100, labels=FALSE)], 
     pch = 19, cex = 1.2, 
     main = "GWR Coefficient: Distance to Center")
legend("bottomright", 
       legend = round(seq(min(gwr_df$distance_center), max(gwr_df$distance_center), length.out = 5), 3),
       fill = coef_colors[seq(1, 100, length.out=5)], 
       title = "Coefficient", cex = 0.8)
dev.off()
cat("✅ Distance center coefficient map saved\n")

# 3. Road Width coefficient map
png("output/gwr_road_width_coef.png", width = 800, height = 600)
plot(df_utm, col = coef_colors[cut(gwr_df$road_width, 100, labels=FALSE)], 
     pch = 19, cex = 1.2, 
     main = "GWR Coefficient: Road Width")
legend("bottomright", 
       legend = round(seq(min(gwr_df$road_width), max(gwr_df$road_width), length.out = 5), 3),
       fill = coef_colors[seq(1, 100, length.out=5)], 
       title = "Coefficient", cex = 0.8)
dev.off()
cat("✅ Road width coefficient map saved\n")

# 4. Predicted vs Actual plot
png("output/gwr_predicted_vs_actual.png", width = 600, height = 600)
plot(gwr_df$y, gwr_df$yhat, 
     xlab = "Actual Value", ylab = "Predicted Value",
     main = "GWR: Predicted vs Actual",
     pch = 19, col = rgb(0, 0, 1, 0.5))
abline(0, 1, col = "red", lwd = 2, lty = 2)
legend("topleft", legend = "Perfect Prediction", col = "red", lty = 2, lwd = 2)
dev.off()
cat("✅ Predicted vs Actual plot saved\n")

cat("\n========================================\n")
cat("✅ GWR Analysis Complete!\n")