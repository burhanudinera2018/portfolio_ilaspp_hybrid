# 🗺️ ILASPP - Sistem Informasi Nilai Tanah Spasial Prediktif

<p align="center">
  <img src="https://img.icons8.com/color/96/000000/map-pin.png" alt="ILASPP Logo" width="80">
</p>

<p align="center">
  <strong>Hybrid R + Python | GWR + Kriging | Streamlit Dashboard</strong>
</p>

<p align="center">
  <!-- Badges -->
  <a href="https://github.com/burhanudin/portfolio_ilaspp_hybrid">
    <img src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github" alt="GitHub">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/License-MIT-绿色?style=for-the-badge&logo=opensourceinitiative" alt="License">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/R-4.5-276DC3?style=flat-square&logo=r" alt="R">
  <img src="https://img.shields.io/badge/PostgreSQL-17-4169E1?style=flat-square&logo=postgresql" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/PostGIS-3.4-4169E1?style=flat-square&logo=postgresql" alt="PostGIS">
</p>

---

## 📌 **Project Overview**

Proyek ini adalah **sistem informasi nilai tanah spasial prediktif** yang dikembangkan untuk memenuhi kebutuhan analisis data di **ATR/BPN (Kementerian Agraria dan Tata Ruang/Badan Pertanahan Nasional)**.

### ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🌐 **GWR** | Geographically Weighted Regression - Analisis variasi spasial |
| 📊 **Kriging** | Interpolasi spasial untuk prediksi nilai tanah |
| 🖥️ **Dashboard** | Visualisasi interaktif dengan Streamlit |
| 🗄️ **Database** | PostgreSQL + PostGIS untuk data spasial |
| 🔄 **Hybrid** | Dual language implementation (R + Python) |

---

## 🏗️ **Arsitektur Proyek**

```mermaid
portfolio_ilaspp_hybrid/
│
├── 📁 data/                    # Data mentah & processed
│   ├── raw/                    # Data asli
│   ├── processed/              # Data setelah cleaning
│   └── geodata/                # File GeoPackage
│
├── 📁 database/                # Script PostgreSQL + PostGIS
│   ├── init_db.py              # Inisialisasi database
│   ├── db_connector.py         # Konektor database
│   └── sample_data_generator.py # Generate sample data
│
├── 📁 R_version/               # ✅ Analisis spasial dengan R
│   ├── 01_data_preparation.R   # Load & prep data
│   ├── 02_gwr_analysis_fixed.R # GWR analysis
│   ├── 03_kriging_analysis.R   # Kriging analysis
│   └── 📁 output/              # Hasil GWR & Kriging
│
├── 📁 Python_version/          # ✨ Dashboard & Visualisasi
│   └── streamlit_app.py        # Main dashboard
│
├── 📁 validation/              # Validasi R vs Python
├── 📁 docs/                    # Dokumentasi
│
├── 📄 requirements.txt         # Python dependencies
├── 📄 .env.example              # Template environment
└── 📄 README.md                # Dokumentasi ini
```

---

## 🚀 **Quick Start**

### Prasyarat

| Software | Version | Installasi |
|----------|---------|------------|
| PostgreSQL | 17+ | [Download](https://www.postgresql.org/) |
| PostGIS | 3.4+ | [Download](https://postgis.net/) |
| Python | 3.11 | `conda create -n ilaspp python=3.11` |
| R | 4.5+ | [Download](https://cran.r-project.org/) |

### 1️⃣ Setup Database

```bash
# Buat database
createdb -U postgres atr_bpn_project

# Enable PostGIS
psql -U postgres -d atr_bpn_project -c "CREATE EXTENSION postgis;"

# Generate sample data
cd database
pip install -r ../requirements.txt
python init_db.py
```

### 2️⃣ Jalankan Analisis (R)

```bash
cd R_version
Rscript 01_data_preparation.R
Rscript 02_gwr_analysis_fixed.R
Rscript 03_kriging_analysis.R
```

### 3️⃣ Jalankan Dashboard

```bash
cd Python_version
streamlit run streamlit_app.py
```

🌐 **Akses dashboard di:** `http://localhost:8501`

---

## 📊 **Hasil Analisis**

### 📈 GWR (Geographically Weighted Regression)

<table>
<tr>
<th>Metrik</th>
<th>Nilai</th>
<th>Interpretasi</th>
</tr>
<tr>
<td>R² (gw.R2)</td>
<td align="center"><b>0.4237</b></td>
<td>Model menjelaskan 42.4% variasi nilai tanah</td>
</tr>
<tr>
<td>Adjusted R²</td>
<td align="center"><b>0.4100</b></td>
<td>Setelah penalti variabel</td>
</tr>
<tr>
<td>Mean Local R²</td>
<td align="center"><b>0.4241</b></td>
<td>Kualitas model konsisten di semua lokasi</td>
</tr>
</table>

**📌 Koefisien:**

| Variabel | Rata-rata | Interpretasi |
|----------|-----------|--------------|
| 📍 Distance Center | **-1.2155** | 100% negatif → semakin jauh dari pusat, nilai tanah TURUN |
| 🛣️ Road Width | **+0.2436** | 100% positif → semakin lebar jalan, nilai tanah NAIK |

### 🌐 Kriging Interpolation

| Metrik | Nilai |
|--------|-------|
| 📈 Range Prediksi | 14.34 - 40.65 juta/m² |
| 📊 Mean Prediksi | 23.87 juta/m² |
| ⚠️ Mean Variance | 85.87 |

---

## 🛠️ **Teknologi yang Digunakan**

| Komponen | Teknologi | Logo |
|----------|-----------|------|
| **Database** | PostgreSQL 17 + PostGIS | 🐘 |
| **Analisis Spasial (R)** | GWmodel, gstat, sf, sp | 📊 |
| **Dashboard (Python)** | Streamlit, Plotly, Pandas | 🐍 |
| **Visualisasi** | Plotly, Folium, ggplot2 | 🎨 |
| **LLM** | LangChain + OpenAI (opsional) | 🤖 |

---

## 📸 **Screenshot Dashboard**

| Halaman | Fitur |
|---------|-------|
| 🏠 Dashboard Utama | Peta interaktif, statistik, bar chart |
| 📈 GWR Results | Distribusi koefisien, Local R² map |
| 🌐 Kriging Results | Peta prediksi, uncertainty map |
| 📊 Perbandingan | Interpretasi & rekomendasi kebijakan |

---

## 👤 **Author**

**Burhanudin Badiuzaman**  
*Data Analyst | Spatial Analytics Enthusiast*

<p align="left">
  <a href="https://github.com/burhanudinera2018">
    <img src="https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github" alt="GitHub">
  </a>
  <a href="https://www.linkedin.com/in/burhanudin-badiuzaman4a9204161/">
    <img src="https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin" alt="LinkedIn">
  </a>
</p>

---

## 📜 License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

You may copy, distribute, and modify the software under the terms of the GPL-3.0.
Any derivative work must also be distributed under the same license.

See the [LICENSE](LICENSE) file for the full license text.

**For commercial use or proprietary integration**, please contact me for a separate commercial license.

---

## 🙏 **Acknowledgments**

- **ATR/BPN** - ILASPP Project (Integrated Land Administration and Spatial Planning)
- **World Bank** - Technical framework and support
- **Open Source Community** - R, Python, PostgreSQL, Streamlit

---

<p align="center">
  <i>Built with ❤️ for ATR/BPN | Data Analyst Portfolio</i>
</p>
