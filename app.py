"""
ILASPP Hybrid Project - Streamlit Dashboard (Deploy Version)
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np

# Page config
st.set_page_config(
    page_title="ILASPP - Hybrid Dashboard",
    page_icon="🗺️",
    layout="wide"
)

# ============================================
# DATA LOADING
# ============================================
@st.cache_data
def load_original_data():
    """Load original land value data"""
    try:
        df = pd.read_csv("land_values_clean.csv")
        return df
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data
def load_gwr_results():
    try:
        df = pd.read_csv("gwr_coefficients.csv")
        return df
    except:
        return None

@st.cache_data
def load_kriging_results():
    try:
        df = pd.read_csv("kriging_predictions.csv")
        return df
    except:
        return None

# Load all data
df = load_original_data()
gwr_df = load_gwr_results()
kriging_df = load_kriging_results()

# ============================================
# SIDEBAR MENU
# ============================================
with st.sidebar:
    st.markdown("## 🗺️ ILASPP")
    st.markdown("*Sistem Informasi Nilai Tanah*")
    st.markdown("---")
    
    page = st.radio(
        "📌 Menu Navigasi",
        [
            "📊 Dashboard Utama",
            "🗺️ GWR Results",
            "🌐 Kriging Results",
            "📈 Perbandingan"
        ]
    )
    
    st.markdown("---")
    st.caption("Hybrid R + Python | GWR + Kriging")

# ============================================
# PAGE 1: DASHBOARD UTAMA
# ============================================
if page == "📊 Dashboard Utama":
    st.title("🗺️ ILASPP - Sistem Informasi Nilai Tanah")
    st.markdown("*Hybrid R + Python | GWR + Kriging*")
    st.markdown("---")
    
    if df is not None and len(df) > 0:
        st.success(f"✅ Loaded {len(df)} records")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🏘️ Total Properti", len(df))
        with col2:
            st.metric("📊 Rata-rata Nilai", f"{df['land_value'].mean():.1f} juta/m²")
        with col3:
            st.metric("📈 Nilai Tertinggi", f"{df['land_value'].max():.1f} juta/m²")
        with col4:
            st.metric("📉 Nilai Terendah", f"{df['land_value'].min():.1f} juta/m²")
        
        # Map
        st.subheader("🗺️ Peta Distribusi Nilai Tanah")
        fig = px.scatter_mapbox(
            df, lat='latitude', lon='longitude',
            color='land_value', size=[8] * len(df),
            color_continuous_scale='Viridis',
            hover_data=['district', 'zone_type', 'land_value'],
            zoom=10, height=500
        )
        fig.update_layout(mapbox_style='carto-positron')
        st.plotly_chart(fig, use_container_width=True)
        
        # Bar chart
        st.subheader("📊 Rata-rata Nilai Tanah per Kecamatan")
        district_stats = df.groupby('district')['land_value'].agg('mean').reset_index()
        district_stats.columns = ['district', 'avg_value']
        district_stats = district_stats.sort_values('avg_value', ascending=False)
        
        fig2 = px.bar(district_stats, x='district', y='avg_value', 
                      color='avg_value', color_continuous_scale='Viridis')
        st.plotly_chart(fig2, use_container_width=True)
        
        with st.expander("📋 Lihat Data Mentah"):
            st.dataframe(df)
    else:
        st.error("⚠️ Data tidak ditemukan")

# ============================================
# PAGE 2: GWR RESULTS
# ============================================
elif page == "🗺️ GWR Results":
    st.title("📈 Geographically Weighted Regression (GWR)")
    st.markdown("---")
    
    if gwr_df is not None and len(gwr_df) > 0:
        st.success(f"✅ Loaded {len(gwr_df)} GWR results")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Mean Local R²", f"{gwr_df['Local_R2'].mean():.4f}")
        with col2:
            st.metric("Min Local R²", f"{gwr_df['Local_R2'].min():.4f}")
        with col3:
            st.metric("Max Local R²", f"{gwr_df['Local_R2'].max():.4f}")
        with col4:
            st.metric("% Negative Distance", f"{(gwr_df['distance_center'] < 0).mean() * 100:.0f}%")
        
        st.subheader("📊 Distribusi Koefisien")
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.histogram(gwr_df, x='distance_center', title='Distance Center Coefficient')
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.histogram(gwr_df, x='road_width', title='Road Width Coefficient')
            st.plotly_chart(fig2, use_container_width=True)
        
        with st.expander("📋 Data Lengkap"):
            st.dataframe(gwr_df)
    else:
        st.warning("⚠️ GWR results not found")

# ============================================
# PAGE 3: KRIGING RESULTS
# ============================================
elif page == "🌐 Kriging Results":
    st.title("🌐 Kriging Interpolation")
    st.markdown("---")
    
    if kriging_df is not None and len(kriging_df) > 0:
        st.success(f"✅ Loaded {len(kriging_df)} predictions")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Min Prediction", f"{kriging_df['var1.pred'].min():.2f}")
        with col2:
            st.metric("Max Prediction", f"{kriging_df['var1.pred'].max():.2f}")
        with col3:
            st.metric("Mean Prediction", f"{kriging_df['var1.pred'].mean():.2f}")
        
        st.subheader("📊 Distribusi Prediksi")
        fig = px.histogram(kriging_df, x='var1.pred', nbins=50, title='Kriging Predictions')
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 Data Lengkap"):
            st.dataframe(kriging_df.head(500))
    else:
        st.warning("⚠️ Kriging results not found")

# ============================================
# PAGE 4: PERBANDINGAN
# ============================================
elif page == "📈 Perbandingan":
    st.title("📈 Perbandingan GWR vs Kriging")
    st.markdown("---")
    
    st.subheader("🔬 Ringkasan Metode")
    overview = pd.DataFrame({
        "Metode": ["GWR", "Kriging"],
        "Tujuan": ["Mengetahui penyebab variasi", "Memprediksi nilai di seluruh area"],
        "Output": ["Koefisien per lokasi, Local R²", "Peta prediksi kontinu"]
    })
    st.dataframe(overview, hide_index=True)
    
    if gwr_df is not None:
        st.subheader("📊 Interpretasi GWR")
        st.markdown(f"""
        - **Distance Center:** {gwr_df['distance_center'].mean():.4f} ({(gwr_df['distance_center'] < 0).mean() * 100:.0f}% negatif)  
          → Semakin jauh dari pusat, nilai tanah turun
        - **Road Width:** {gwr_df['road_width'].mean():.4f} ({(gwr_df['road_width'] > 0).mean() * 100:.0f}% positif)  
          → Semakin lebar jalan, nilai tanah naik
        """)
    
    if kriging_df is not None:
        st.subheader("🌐 Interpretasi Kriging")
        st.markdown(f"""
        - Range Prediksi: {kriging_df['var1.pred'].min():.2f} - {kriging_df['var1.pred'].max():.2f} juta/m²
        - Mean Prediksi: {kriging_df['var1.pred'].mean():.2f} juta/m²
        """)

# ============================================
# FOOTER - COPYRIGHT & IDENTITAS PEMBUAT
# ============================================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; padding: 20px 0 10px 0; color: #666666;">
        <p>© 2026 Burhanudin Badiuzaman | Data Scientist & AI Engineer</p>
        <p style="font-size: 12px; margin-top: 5px;">
            Dibangun untuk ILASPP - ATR/BPN | 
            <a href="https://github.com/burhanudinera2018" target="_blank" style="color: #2563eb; text-decoration: none;">GitHub</a> | 
            <a href="https://www.linkedin.com/in/burhanudin-badiuzaman-4a9204161/" target="_blank" style="color: #2563eb; text-decoration: none;">LinkedIn</a>
        </p>
        <p style="font-size: 11px; margin-top: 5px;">
            Hybrid R + Python | GWR + Kriging | PostgreSQL + PostGIS
        </p>
    </div>
    """,
    unsafe_allow_html=True
)