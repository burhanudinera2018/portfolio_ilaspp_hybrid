# validation/compare_results.py
print("🔬 Validation: Checking R output exists...")

import os
import pandas as pd

# Cek apakah file hasil R ada
files = ["../R_version/output/gwr_coefficients.csv",
         "../R_version/output/kriging_predictions.csv"]

for f in files:
    if os.path.exists(f):
        print(f"✅ {f} exists")
    else:
        print(f"⚠️ {f} not found - run R scripts first")

print("\n✅ Validation ready!")
