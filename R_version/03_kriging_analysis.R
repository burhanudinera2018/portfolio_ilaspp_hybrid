# ============================================
# ILASPP - Kriging Analysis (FIXED)
# ============================================

library(gstat)
library(sp)
library(sf)
library(raster)  # ← PENTING: ini yang sebelumnya kurang

cat("🌐 Kriging Analysis\n")
cat("========================================\n")

# Load data
df <- read.csv("../data/processed/land_values_clean.csv")
cat("✅ Loaded", nrow(df), "records\n")

# Convert to spatial
coordinates(df) <- ~longitude + latitude
proj4string(df) <- CRS("+init=epsg:4326")
df_utm <- spTransform(df, CRS("+init=epsg:32748"))

# Create interpolation grid
bbox <- bbox(df_utm)
grd <- expand.grid(
    x = seq(bbox[1,1], bbox[1,2], length.out = 50),
    y = seq(bbox[2,1], bbox[2,2], length.out = 50)
)
coordinates(grd) <- ~x + y
gridded(grd) <- TRUE
proj4string(grd) <- proj4string(df_utm)
cat("✅ Grid created with", nrow(grd), "points\n")

# Variogram analysis
cat("\n📊 Variogram analysis...\n")
vgm_exp <- variogram(land_value ~ 1, data = df_utm)

# Fit variogram with tryCatch to handle warning
tryCatch({
    vgm_fit <- fit.variogram(vgm_exp, vgm(model = "Sph"))
    cat("✅ Variogram fitted (Spherical model)\n")
}, error = function(e) {
    cat("⚠️ Spherical model failed, trying Exponential...\n")
    vgm_fit <- fit.variogram(vgm_exp, vgm(model = "Exp"))
    cat("✅ Variogram fitted (Exponential model)\n")
})

# Ordinary Kriging
cat("\n🔄 Running Ordinary Kriging...\n")
kriging_result <- krige(land_value ~ 1, df_utm, grd, model = vgm_fit)

# Convert to data frame
kriging_df <- as.data.frame(kriging_result)
kriging_df$x_geo <- coordinates(kriging_result)[,1]
kriging_df$y_geo <- coordinates(kriging_result)[,2]

# Summary
cat("\n========== KRIGING RESULTS ==========\n")
cat("Prediction range:", 
    round(min(kriging_df$var1.pred, na.rm=TRUE), 2), "-",
    round(max(kriging_df$var1.pred, na.rm=TRUE), 2), "juta/m²\n")
cat("Mean prediction:", round(mean(kriging_df$var1.pred, na.rm=TRUE), 2), "\n")
cat("Mean variance:", round(mean(kriging_df$var1.var, na.rm=TRUE), 2), "\n")

# Save results
write.csv(kriging_df, "output/kriging_predictions.csv", row.names = FALSE)
cat("\n✅ Kriging results saved to: output/kriging_predictions.csv\n")

# Create prediction map (menggunakan levelplot dari rasterVis jika ada, atau plot biasa)
png("output/kriging_prediction_map.png", width = 800, height = 600)

# Create raster from XYZ
tryCatch({
    # Convert to raster
    pred_raster <- rasterFromXYZ(cbind(kriging_df$x_geo, kriging_df$y_geo, kriging_df$var1.pred))
    plot(pred_raster, main = "Kriging: Predicted Land Value (juta/m²)",
         col = terrain.colors(100))
    plot(df_utm, add = TRUE, pch = 19, cex = 0.8, col = "black")
}, error = function(e) {
    # Fallback: plot points instead of raster
    cat("⚠️ Raster plot failed, using point plot\n")
    plot(kriging_df$x_geo, kriging_df$y_geo, 
         col = heat.colors(100)[cut(kriging_df$var1.pred, 100)],
         pch = 15, cex = 0.5,
         xlab = "X (UTM)", ylab = "Y (UTM)",
         main = "Kriging: Predicted Land Value (juta/m²)")
    points(df_utm, pch = 19, cex = 0.8, col = "black")
})
dev.off()
cat("✅ Prediction map saved: output/kriging_prediction_map.png\n")

# Create variance/uncertainty map
png("output/kriging_variance_map.png", width = 800, height = 600)
tryCatch({
    var_raster <- rasterFromXYZ(cbind(kriging_df$x_geo, kriging_df$y_geo, sqrt(kriging_df$var1.var)))
    plot(var_raster, main = "Kriging: Prediction Uncertainty (Std Dev)",
         col = rev(heat.colors(100)))
    plot(df_utm, add = TRUE, pch = 19, cex = 0.8, col = "black")
}, error = function(e) {
    plot(kriging_df$x_geo, kriging_df$y_geo, 
         col = rev(heat.colors(100))[cut(sqrt(kriging_df$var1.var), 100)],
         pch = 15, cex = 0.5,
         xlab = "X (UTM)", ylab = "Y (UTM)",
         main = "Kriging: Prediction Uncertainty (Std Dev)")
    points(df_utm, pch = 19, cex = 0.8, col = "black")
})
dev.off()
cat("✅ Variance map saved: output/kriging_variance_map.png\n")

# Create contour plot
png("output/kriging_contour.png", width = 800, height = 600)
tryCatch({
    pred_raster <- rasterFromXYZ(cbind(kriging_df$x_geo, kriging_df$y_geo, kriging_df$var1.pred))
    contour(pred_raster, main = "Kriging: Contour Map of Land Value",
            col = "blue", labcex = 0.8)
    points(df_utm, pch = 19, cex = 0.8, col = "red")
}, error = function(e) {
    # Simple contour using akima if needed
    cat("⚠️ Contour plot requires akima package\n")
    plot(kriging_df$x_geo, kriging_df$y_geo, 
         col = terrain.colors(100)[cut(kriging_df$var1.pred, 100)],
         pch = 15, cex = 0.5,
         main = "Kriging: Predicted Values (color = prediction)")
})
dev.off()
cat("✅ Contour map saved: output/kriging_contour.png\n")

cat("\n========================================\n")
cat("✅ Kriging Analysis Complete!\n")