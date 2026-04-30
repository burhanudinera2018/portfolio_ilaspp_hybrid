import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os

st.set_page_config(page_title="Kriging Results", layout="wide")
st.title("🌐 Kriging Interpolation")

try:
    kriging_df = pd.read_csv("../R_version/output/kriging_predictions.csv")
    st.success(f"✅ Loaded {len(kriging_df)} Kriging predictions")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Min Prediction", f"{kriging_df['var1.pred'].min():.2f}")
    with col2:
        st.metric("Max Prediction", f"{kriging_df['var1.pred'].max():.2f}")
    with col3:
        st.metric("Mean Prediction", f"{kriging_df['var1.pred'].mean():.2f}")
    
    # Tampilkan gambar hasil Kriging
    st.subheader("🗺️ Peta Hasil Kriging")
    
    img_paths = [
        ("../R_version/output/kriging_prediction_map.png", "Prediction Map"),
        ("../R_version/output/kriging_variance_map.png", "Uncertainty Map"),
        ("../R_version/output/kriging_contour.png", "Contour Map")
    ]
    
    cols = st.columns(3)
    for i, (path, title) in enumerate(img_paths):
        if os.path.exists(path):
            cols[i].image(path, caption=title, use_container_width=True)
        else:
            cols[i].warning(f"{title} not found")
    
    with st.expander("📋 Data Lengkap"):
        st.dataframe(kriging_df.head(100))
        
except Exception as e:
    st.error(f"Kriging results not found: {e}")
