import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="GWR Results", layout="wide")
st.title("📈 Geographically Weighted Regression (GWR)")

try:
    gwr_df = pd.read_csv("../R_version/output/gwr_coefficients.csv")
    st.success(f"✅ Loaded {len(gwr_df)} GWR results")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mean Local R²", f"{gwr_df['Local_R2'].mean():.3f}")
    with col2:
        st.metric("Mean Distance Coef", f"{gwr_df['distance_center'].mean():.3f}")
    with col3:
        st.metric("Mean Road Width Coef", f"{gwr_df['road_width'].mean():.3f}")
    
    st.subheader("📊 Koefisien Distance Center per Lokasi")
    fig1 = px.histogram(gwr_df, x='distance_center', 
                        title='Distribusi Koefisien Jarak ke Pusat')
    st.plotly_chart(fig1)
    
    with st.expander("📋 Data Lengkap"):
        st.dataframe(gwr_df)
        
except Exception as e:
    st.error(f"GWR results not found: {e}")
