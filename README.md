```markdown
# 🗺️ ILASPP - Sistem Informasi Nilai Tanah Spasial Prediktif

**Hybrid R + Python | GWR + Kriging | Streamlit Dashboard**

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![R 4.5](https://img.shields.io/badge/R-4.5-blue.svg)](https://www.r-project.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue.svg)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)](https://streamlit.io/)

---

## 📌 **Project Overview**

Proyek ini adalah **sistem informasi nilai tanah spasial prediktif** yang dikembangkan untuk memenuhi kebutuhan analisis data di **ATR/BPN (Kementerian Agraria dan Tata Ruang/Badan Pertanahan Nasional)**.

**Fitur Utama:**
- ✅ **GWR (Geographically Weighted Regression)** - Analisis variasi spasial pengaruh variabel
- ✅ **Kriging Interpolation** - Prediksi nilai tanah di seluruh area
- ✅ **Streamlit Dashboard** - Visualisasi interaktif
- ✅ **PostgreSQL + PostGIS** - Database spasial enterprise
- ✅ **Hybrid R + Python** - Dual language implementation

---

## 🏗️ **Arsitektur Proyek**

```mermaid
portfolio_ilaspp_hybrid/
├── data/                    # Data mentah & processed
├── database/                # Script PostgreSQL + PostGIS
├── R_version/               # ✅ Analisis spasial dengan R
│   ├── 01_data_preparation.R
│   ├── 02_gwr_analysis_fixed.R
│   ├── 03_kriging_analysis.R
│   └── output/              # Hasil GWR & Kriging
├── Python_version/          # ✨ Dashboard & Visualisasi
│   └── streamlit_app.py
├── validation/              # Validasi R vs Python
└── docs/                    # Dokumentasi

```

---

## 🚀 **Quick Start**

### **1. Setup Database (PostgreSQL + PostGIS)**

```bash
# Buat database
createdb -U postgres atr_bpn_project

# Enable PostGIS
psql -U postgres -d atr_bpn_project -c "CREATE EXTENSION postgis;"

# Generate sample data
cd database
python init_db.py
```

### **2. Jalankan Analisis GWR & Kriging (R)**

```bash
cd R_version
Rscript 01_data_preparation.R
Rscript 02_gwr_analysis_fixed.R
Rscript 03_kriging_analysis.R
```

### **3. Jalankan Dashboard (Python)**

```bash
cd Python_version
streamlit run streamlit_app.py
```

Akses dashboard di: `http://localhost:8501`

---

## 📊 **Hasil Analisis**

### **GWR (Geographically Weighted Regression)**

| Metrik | Nilai |
|--------|-------|
| R² (gw.R2) | 0.4237 |
| Adjusted R² | 0.4100 |
| Mean Local R² | 0.4241 |

**Koefisien:**
- **Distance Center**: -1.2155 (100% negatif) → semakin jauh dari pusat, nilai tanah turun
- **Road Width**: +0.2436 (100% positif) → semakin lebar jalan, nilai tanah naik

### **Kriging Interpolation**

| Metrik | Nilai |
|--------|-------|
| Range Prediksi | 14.34 - 40.65 juta/m² |
| Mean Prediksi | 23.87 juta/m² |
| Mean Variance | 85.87 |

---

## 🛠️ **Teknologi yang Digunakan**

| Komponen | Teknologi |
|----------|-----------|
| **Database** | PostgreSQL 17 + PostGIS |
| **Analisis Spasial (R)** | GWmodel, gstat, sf, sp |
| **Dashboard (Python)** | Streamlit, Plotly, Pandas |
| **Visualisasi** | Plotly, Folium, ggplot2 |
| **LLM** | LangChain + OpenAI (opsional) |

---

## 📈 **Screenshot Dashboard**

| Halaman | Fitur |
|---------|-------|
| Dashboard Utama | Peta distribusi, statistik, bar chart |
| GWR Results | Distribusi koefisien, Local R² map |
| Kriging Results | Peta prediksi, uncertainty map |
| Perbandingan | Interpretasi & rekomendasi kebijakan |

---

## 👤 **Author**

**Data Analyst** - ILASPP Project Portfolio  
*Project ini dikembangkan sebagai portfolio untuk posisi Data Analyst di ATR/BPN*

---

## 📝 **Lisensi**

MIT License - Bebas digunakan untuk keperluan pembelajaran dan portfolio.

---

## 🙏 **Acknowledgments**

- Kementerian ATR/BPN - ILASPP Project
- World Bank - Technical framework
- Open Source Community - R, Python, PostgreSQL, Streamlit
```
```