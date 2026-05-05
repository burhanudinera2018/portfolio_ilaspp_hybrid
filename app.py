"""
ILASPP Hybrid Project - Streamlit Dashboard
Run: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="ILASPP - Hybrid Dashboard",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SIDEBAR MENU
# ============================================
with st.sidebar:
    st.markdown("## 🗺️ ILASPP")
    st.markdown("*Sistem Informasi Nilai Tanah*")
    st.markdown("---")
    
    page = st.radio(
        "📌 **Menu Navigasi**",
        [
            "📊 Dashboard Utama",
            "🗺️ GWR Results",
            "🌐 Kriging Results",
            "🗺️ Peta Dominasi Variabel",
            "📈 Perbandingan & Interpretasi"
        ]
    )
    
    st.markdown("---")
    st.caption("Hybrid R + Python")
    st.caption("GWR + Kriging")
    st.caption("ATR/BPN - ILASPP Project")

# ============================================
# DATA LOADING FUNCTIONS
# ============================================
from pathlib import Path

BASE_DIR = Path(__file__).parent  # ← ini root repository

csv_path = BASE_DIR / "data" / "processed" / "land_values_clean.csv"
gwr_path = BASE_DIR / "R_version" / "output" / "gwr_coefficients.csv"
kriging_path = BASE_DIR / "R_version" / "output" / "kriging_predictions.csv"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data
def load_gwr_results():
    try:
        df = pd.read_csv(gwr_path)
        # Hitung variabel dominan jika belum ada
        if 'dominant_variable' not in df.columns:
            coeff_abs = abs(df[['distance_center', 'road_width']])
            df['dominant_variable'] = coeff_abs.idxmax(axis=1)
        return df
    except Exception as e:
        return None

@st.cache_data
def load_kriging_results():
    try:
        df = pd.read_csv(kriging_path)
        return df
    except Exception as e:
        return None

# Load all data
df = load_data()
gwr_df = load_gwr_results()
kriging_df = load_kriging_results()

# ============================================
# PAGE 1: DASHBOARD UTAMA
# ============================================
if page == "📊 Dashboard Utama":
    st.title("🗺️ ILASPP - Sistem Informasi Nilai Tanah")
    st.markdown("*Hybrid R + Python | GWR + Kriging*")
    st.markdown("---")
    
    if df is not None and len(df) > 0:
        st.success(f"✅ Loaded {len(df)} records")
        
        # Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🏘️ Total Properti", len(df))
        with col2:
            st.metric("📊 Rata-rata Nilai", f"{df['land_value'].mean():.1f} juta/m²")
        with col3:
            st.metric("📈 Nilai Tertinggi", f"{df['land_value'].max():.1f} juta/m²")
        with col4:
            st.metric("📉 Nilai Terendah", f"{df['land_value'].min():.1f} juta/m²")
        
        # Map - menggunakan scatter_mapbox untuk peta yang lebih baik
        st.subheader("🗺️ Peta Distribusi Nilai Tanah")
        fig = px.scatter_mapbox(
            df, lat='latitude', lon='longitude',
            color='land_value', size=[8] * len(df),
            color_continuous_scale='Viridis',
            hover_data=['district', 'zone_type', 'land_value'],
            zoom=10, height=500,
            title="Distribusi Spasial Nilai Tanah"
        )
        fig.update_layout(mapbox_style='carto-positron')
        st.plotly_chart(fig, use_container_width=True)
        
        # Bar chart per district
        st.subheader("📊 Rata-rata Nilai Tanah per Kecamatan")
        district_stats = df.groupby('district')['land_value'].agg(['mean', 'count']).reset_index()
        district_stats.columns = ['district', 'avg_value', 'count']
        district_stats = district_stats.sort_values('avg_value', ascending=False)
        
        fig2 = px.bar(district_stats, x='district', y='avg_value', 
                      color='avg_value', color_continuous_scale='Viridis',
                      title='Rata-rata Nilai Tanah per Kecamatan',
                      labels={'avg_value': 'Nilai (juta/m²)', 'district': 'Kecamatan'})
        st.plotly_chart(fig2, use_container_width=True)
        
        # Show raw data
        with st.expander("📋 Lihat Data Mentah"):
            st.dataframe(df)
    else:
        st.error("⚠️ Data tidak ditemukan. Jalankan: cd R_version && Rscript 01_data_preparation.R")
        st.info(f"Mencari file di: {os.path.abspath(csv_path)}")

# ============================================
# PAGE 2: GWR RESULTS
# ============================================
elif page == "🗺️ GWR Results":
    st.title("📈 Geographically Weighted Regression (GWR)")
    st.markdown("*Analisis Variasi Spasial Pengaruh Variabel terhadap Nilai Tanah*")
    st.markdown("---")
    
    if gwr_df is not None and len(gwr_df) > 0:
        st.success(f"✅ Loaded {len(gwr_df)} GWR results")
        
        # Key Metrics
        st.subheader("📊 Ringkasan Statistik GWR")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📈 Mean Local R²", f"{gwr_df['Local_R2'].mean():.4f}")
        with col2:
            st.metric("📉 Min Local R²", f"{gwr_df['Local_R2'].min():.4f}")
        with col3:
            st.metric("📊 Max Local R²", f"{gwr_df['Local_R2'].max():.4f}")
        with col4:
            st.metric("📐 SD Local R²", f"{gwr_df['Local_R2'].std():.4f}")
        
        # Coefficient Distribution
        st.subheader("📊 Distribusi Koefisien per Variabel")
        
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.histogram(gwr_df, x='distance_center', 
                                title='Koefisien Distance Center (Jarak ke Pusat)',
                                labels={'distance_center': 'Koefisien'},
                                color_discrete_sequence=['blue'],
                                nbins=30)
            fig1.add_vline(x=0, line_dash="dash", line_color="red")
            st.plotly_chart(fig1, use_container_width=True)
            
        with col2:
            fig2 = px.histogram(gwr_df, x='road_width',
                                title='Koefisien Road Width (Lebar Jalan)',
                                labels={'road_width': 'Koefisien'},
                                color_discrete_sequence=['green'],
                                nbins=30)
            fig2.add_vline(x=0, line_dash="dash", line_color="red")
            st.plotly_chart(fig2, use_container_width=True)
        
        # Coefficient Summaries
        st.subheader("📋 Ringkasan Koefisien")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Distance Center (Jarak ke Pusat Kota)**")
            st.markdown(f"""
            - Mean: **{gwr_df['distance_center'].mean():.4f}**
            - Min: {gwr_df['distance_center'].min():.4f}
            - Max: {gwr_df['distance_center'].max():.4f}
            - % Negative: **{(gwr_df['distance_center'] < 0).mean() * 100:.1f}%**
            """)
        
        with col2:
            st.markdown("**Road Width (Lebar Jalan)**")
            st.markdown(f"""
            - Mean: **{gwr_df['road_width'].mean():.4f}**
            - Min: {gwr_df['road_width'].min():.4f}
            - Max: {gwr_df['road_width'].max():.4f}
            - % Positive: **{(gwr_df['road_width'] > 0).mean() * 100:.1f}%**
            """)
        
        # Dominant Variable
        st.subheader("🎯 Variabel Dominan per Lokasi")
        
        fig3 = px.pie(values=gwr_df['dominant_variable'].value_counts().values, 
                      names=gwr_df['dominant_variable'].value_counts().index,
                      title='Proporsi Variabel Dominan',
                      color_discrete_sequence=['#E53935', '#43A047'])
        st.plotly_chart(fig3, use_container_width=True)
        
        # Show images
        st.subheader("🗺️ Visualisasi GWR")
        img_col1, img_col2 = st.columns(2)
        
        with img_col1:
            if os.path.exists("../R_version/output/gwr_local_r2_map.png"):
                st.image("../R_version/output/gwr_local_r2_map.png", caption="Local R² Map")
            else:
                st.info("Local R² map not found")
        
        with img_col2:
            if os.path.exists("../R_version/output/gwr_predicted_vs_actual.png"):
                st.image("../R_version/output/gwr_predicted_vs_actual.png", caption="Predicted vs Actual")
            else:
                st.info("Prediction plot not found")
        
        with st.expander("📋 Lihat Data GWR Lengkap"):
            st.dataframe(gwr_df)
            
    else:
        st.warning("⚠️ GWR results not found. Run: cd R_version && Rscript 02_gwr_analysis_fixed.R")

# ============================================
# PAGE 3: KRIGING RESULTS
# ============================================
elif page == "🌐 Kriging Results":
    st.title("🌐 Kriging Interpolation")
    st.markdown("*Prediksi Nilai Tanah di Seluruh Area Berdasarkan Data Titik*")
    st.markdown("---")
    
    if kriging_df is not None and len(kriging_df) > 0:
        st.success(f"✅ Loaded {len(kriging_df)} Kriging predictions")
        
        # Key Metrics
        st.subheader("📊 Ringkasan Statistik Kriging")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📈 Min Prediction", f"{kriging_df['var1.pred'].min():.2f} juta/m²")
        with col2:
            st.metric("📊 Max Prediction", f"{kriging_df['var1.pred'].max():.2f} juta/m²")
        with col3:
            st.metric("📉 Mean Prediction", f"{kriging_df['var1.pred'].mean():.2f} juta/m²")
        
        # Prediction distribution
        st.subheader("📊 Distribusi Nilai Prediksi")
        fig = px.histogram(kriging_df, x='var1.pred',
                          title='Distribusi Nilai Tanah Hasil Kriging',
                          labels={'var1.pred': 'Predicted Value (juta/m²)'},
                          nbins=50,
                          color_discrete_sequence=['purple'])
        st.plotly_chart(fig, use_container_width=True)
        
        # Uncertainty distribution
        st.subheader("⚠️ Distribusi Uncertainty")
        fig2 = px.histogram(kriging_df, x='var1.var',
                           title='Distribusi Variance (Ketidakpastian Prediksi)',
                           labels={'var1.var': 'Variance'},
                           nbins=50,
                           color_discrete_sequence=['orange'])
        st.plotly_chart(fig2, use_container_width=True)
        
        # Show images
        st.subheader("🗺️ Visualisasi Kriging")
        
        img_col1, img_col2, img_col3 = st.columns(3)
        
        with img_col1:
            if os.path.exists("../R_version/output/kriging_prediction_map.png"):
                st.image("../R_version/output/kriging_prediction_map.png", caption="Prediction Map")
            else:
                st.info("Prediction map not found")
        
        with img_col2:
            if os.path.exists("../R_version/output/kriging_variance_map.png"):
                st.image("../R_version/output/kriging_variance_map.png", caption="Uncertainty Map")
            else:
                st.info("Variance map not found")
        
        with img_col3:
            if os.path.exists("../R_version/output/kriging_contour.png"):
                st.image("../R_version/output/kriging_contour.png", caption="Contour Map")
            else:
                st.info("Contour map not found")
        
        with st.expander("📋 Lihat Data Kriging Lengkap"):
            st.dataframe(kriging_df.head(500))
            
    else:
        st.warning("⚠️ Kriging results not found. Run: cd R_version && Rscript 03_kriging_analysis.R")
        st.info(f"Mencari file di: {os.path.abspath(kriging_path)}")

# ============================================
# PAGE 4: PETA DOMINASI VARIABEL
# ============================================
elif page == "🗺️ Peta Dominasi Variabel":
    st.title("🗺️ Peta Dominasi Variabel")
    st.markdown("*Wilayah mana yang didominasi oleh jarak ke pusat kota vs lebar jalan?*")
    st.markdown("---")
    
    if gwr_df is not None and len(gwr_df) > 0:
        if 'latitude' not in gwr_df.columns or 'longitude' not in gwr_df.columns:
            st.error("Koordinat tidak ditemukan dalam data GWR")
        else:
            # ============ MAP 1: DOMINANT VARIABLE MAP ============
            st.subheader("📍 Peta Dominasi Variabel per Lokasi")
            
            fig1 = px.scatter_geo(
                gwr_df,
                lat='latitude',
                lon='longitude',
                color='dominant_variable',
                size='Local_R2' if 'Local_R2' in gwr_df.columns else 8,
                hover_name='district' if 'district' in gwr_df.columns else gwr_df.index.astype(str),
                hover_data={
                    'distance_center': ':.4f',
                    'road_width': ':.4f',
                    'Local_R2': ':.4f'
                },
                color_discrete_map={
                    'distance_center': '#E53935',
                    'road_width': '#43A047'
                },
                title='<b>Faktor Dominan Nilai Tanah per Lokasi</b><br><span style="font-size:12px">🔴 Merah = Didominasi Jarak ke Pusat | 🟢 Hijau = Didominasi Lebar Jalan</span>',
                projection='mercator'
            )
            fig1.update_geos(
                showland=True, 
                landcolor='lightgray', 
                showocean=True, 
                oceancolor='lightblue',
                showcountries=True,
                countrycolor='gray'
            )
            fig1.update_layout(height=550, margin={"r":0, "t":50, "l":0, "b":0})
            st.plotly_chart(fig1, use_container_width=True)
            
            # ============ MAP 2 & 3: COEFFICIENT MAPS ============
            st.subheader("📊 Besaran Pengaruh Variabel per Lokasi")
            col1, col2 = st.columns(2)
            
            with col1:
                fig2 = px.scatter_geo(
                    gwr_df,
                    lat='latitude',
                    lon='longitude',
                    color='distance_center',
                    size='Local_R2' if 'Local_R2' in gwr_df.columns else 8,
                    hover_name='district' if 'district' in gwr_df.columns else gwr_df.index.astype(str),
                    color_continuous_scale='RdBu_r',
                    title='<b>Koefisien Distance Center</b><br><span style="font-size:12px">🔴 Negatif = semakin jauh semakin murah<br>🔵 Positif = semakin jauh semakin mahal</span>',
                    projection='mercator'
                )
                fig2.update_geos(showland=True, landcolor='lightgray')
                fig2.update_layout(height=450, margin={"r":0, "t":50, "l":0, "b":0})
                st.plotly_chart(fig2, use_container_width=True)
            
            with col2:
                fig3 = px.scatter_geo(
                    gwr_df,
                    lat='latitude',
                    lon='longitude',
                    color='road_width',
                    size='Local_R2' if 'Local_R2' in gwr_df.columns else 8,
                    hover_name='district' if 'district' in gwr_df.columns else gwr_df.index.astype(str),
                    color_continuous_scale='RdYlGn',
                    title='<b>Koefisien Road Width</b><br><span style="font-size:12px">🟢 Positif = semakin lebar semakin mahal<br>🔴 Negatif = semakin lebar semakin murah</span>',
                    projection='mercator'
                )
                fig3.update_geos(showland=True, landcolor='lightgray')
                fig3.update_layout(height=450, margin={"r":0, "t":50, "l":0, "b":0})
                st.plotly_chart(fig3, use_container_width=True)
            
            # ============ SUMMARY TABLE ============
            st.subheader("📋 Ringkasan per Kecamatan")
            
            if 'district' in gwr_df.columns:
                summary_df = gwr_df.groupby('district').agg({
                    'distance_center': 'mean',
                    'road_width': 'mean',
                    'Local_R2': 'mean'
                }).round(4).reset_index()
                
                dominant_summary = gwr_df.groupby('district')['dominant_variable'].agg(
                    lambda x: x.value_counts().index[0] if len(x) > 0 else 'N/A'
                ).reset_index()
                dominant_summary.columns = ['district', 'dominant_majority']
                
                summary_df = summary_df.merge(dominant_summary, on='district')
                summary_df.columns = ['Kecamatan', 'Rata-rata Koef Jarak', 'Rata-rata Koef Lebar Jalan', 'Mean Local R²', 'Variabel Dominan']
                
                st.dataframe(summary_df, use_container_width=True)
                
                csv = summary_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Ringkasan (CSV)",
                    data=csv,
                    file_name="gwr_dominant_variable_summary.csv",
                    mime="text/csv"
                )
            else:
                st.info("Data kecamatan tidak tersedia untuk ditampilkan dalam tabel")
            
            # ============ INSIGHT ============
            st.markdown("---")
            st.subheader("💡 Insight dari Peta Dominasi")
            
            dom_counts = gwr_df['dominant_variable'].value_counts()
            pct_distance = dom_counts.get('distance_center', 0) / len(gwr_df) * 100
            pct_road = dom_counts.get('road_width', 0) / len(gwr_df) * 100
            
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px;">
                <p style="font-size: 16px; font-weight: bold;">📈 Hasil GWR menunjukkan:</p>
                <ul>
                    <li><span style="color: #E53935;">🔴 <b>{pct_distance:.1f}% lokasi</b></span> didominasi oleh <b>JARAK KE PUSAT KOTA</b></li>
                    <li><span style="color: #43A047;">🟢 <b>{pct_road:.1f}% lokasi</b></span> didominasi oleh <b>LEBAR JALAN</b></li>
                </ul>
                <p><b>💡 Interpretasi untuk Kebijakan:</b></p>
                <ul>
                    <li><b>Daerah dominasi jarak</b> → Fokus pada <b>aksesibilitas ke pusat bisnis</b></li>
                    <li><b>Daerah dominasi lebar jalan</b> → Prioritaskan <b>infrastruktur jalan</b></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.warning("⚠️ GWR results not found. Run: cd R_version && Rscript 02_gwr_analysis_fixed.R")

# ============================================
# PAGE 5: PERBANDINGAN & INTERPRETASI
# ============================================
elif page == "📈 Perbandingan & Interpretasi":
    st.title("📈 Perbandingan GWR vs Kriging")
    st.markdown("*Integrasi Kedua Metode untuk Analisis Spasial yang Komprehensif*")
    st.markdown("---")
    
    # Overview table
    st.subheader("🔬 Ringkasan Metode")
    
    overview_df = pd.DataFrame({
        "Metode": ["GWR", "Kriging"],
        "Tujuan": [
            "Mengetahui penyebab variasi nilai tanah",
            "Memprediksi nilai di seluruh area"
        ],
        "Output Utama": [
            "Koefisien per lokasi, Local R²",
            "Peta prediksi kontinu, Uncertainty map"
        ],
        "Kelebihan": [
            "Menjelaskan variasi spasial, Interpretable",
            "Mengisi area kosong, Quantify uncertainty"
        ]
    })
    st.dataframe(overview_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # GWR Interpretation
    st.subheader("📊 Interpretasi GWR")
    
    if gwr_df is not None and len(gwr_df) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 **Distance Center**")
            mean_dc = gwr_df['distance_center'].mean()
            pct_neg = (gwr_df['distance_center'] < 0).mean() * 100
            st.markdown(f"""
            - Rata-rata koefisien: **{mean_dc:.4f}**
            - {pct_neg:.0f}% lokasi koefisien **negatif**
            
            **Interpretasi:**  
            Semakin jauh dari pusat kota, nilai tanah **menurun**.
            Setiap +1 km jarak, nilai turun **{abs(mean_dc):.2f} juta/m²**.
            """)
        
        with col2:
            st.markdown("#### 🛣️ **Road Width**")
            mean_rw = gwr_df['road_width'].mean()
            pct_pos = (gwr_df['road_width'] > 0).mean() * 100
            st.markdown(f"""
            - Rata-rata koefisien: **{mean_rw:.4f}**
            - {pct_pos:.0f}% lokasi koefisien **positif**
            
            **Interpretasi:**  
            Semakin lebar jalan, nilai tanah **meningkat**.
            Setiap +1 m lebar jalan, nilai naik **{mean_rw:.2f} juta/m²**.
            """)
        
        st.markdown("#### 📈 **Kualitas Model**")
        st.markdown(f"""
        - Mean Local R²: **{gwr_df['Local_R2'].mean():.4f}**
        - Range: {gwr_df['Local_R2'].min():.4f} - {gwr_df['Local_R2'].max():.4f}
        """)
    else:
        st.info("GWR results not loaded")
    
    st.markdown("---")
    
    # Kriging Interpretation
    st.subheader("🌐 Interpretasi Kriging")
    
    if kriging_df is not None and len(kriging_df) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 **Statistik Prediksi**")
            st.markdown(f"""
            - Range: **{kriging_df['var1.pred'].min():.2f} - {kriging_df['var1.pred'].max():.2f}** juta/m²
            - Mean: **{kriging_df['var1.pred'].mean():.2f}** juta/m²
            """)
        
        with col2:
            st.markdown("#### ⚠️ **Ketidakpastian**")
            st.markdown(f"""
            - Mean variance: **{kriging_df['var1.var'].mean():.2f}**
            - Std Dev: **{np.sqrt(kriging_df['var1.var'].mean()):.2f}**
            
            Area dengan variance tinggi perlu survei tambahan.
            """)
    else:
        st.info("Kriging results not loaded")
    
    st.markdown("---")
    
    # Recommendations
    st.subheader("💡 Rekomendasi Kebijakan")
    
    st.markdown("""
    ### 📌 Berdasarkan GWR:
    1. Prioritas pengembangan di area dengan akses jalan lebar
    2. Insentif untuk pengembangan di area pinggiran (koefisien jarak negatif kuat)
    
    ### 📌 Berdasarkan Kriging:
    1. Fokus survei di area dengan variance tinggi
    2. Identifikasi hotspot untuk investasi properti
    
    ### 📌 Rekomendasi Lanjutan:
    1. Integrasikan data raster (elevasi, kepadatan)
    2. Perbarui data berkala
    3. Kembangkan dashboard real-time
    """)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.caption("🗺️ ILASPP Hybrid Portfolio | R + Python | GWR + Kriging | ATR/BPN")

# Copyright & Social Links - VERSION RAPIH
st.markdown(
    f"""
    <div style="text-align: center; padding: 15px 0 10px 0;">
        <p style="font-size: 13px; color: #666; margin-bottom: 12px;">
            © 2026 by Burhanudin Badiuzaman — Portfolio Project Data Analyst ATR/BPN
        </p>
        <div style="display: flex; justify-content: center; gap: 25px; flex-wrap: wrap;">
            <a href="https://www.linkedin.com/in/burhanudin-badiuzaman4a9204161/" target="_blank" style="text-decoration: none; font-size: 13px; color: #0077b5;">🔗 LinkedIn</a>
            <a href="https://github.com/burhanudinera2018" target="_blank" style="text-decoration: none; font-size: 13px; color: #333;">🐙 GitHub</a>
            <a href="mailto:burhanudinera2018@gmail.com" style="text-decoration: none; font-size: 13px; color: #ea4335;">📧 Email</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
