# 🗺️ ILASPP - Integrasi Data Spasial untuk Analisis Harga Properti di Indonesia

<p align="center">
  <img src="https://img.icons8.com/color/96/000000/map-pin.png" alt="ILASPP Logo" width="80">
</p>

<p align="center">
  <strong>Analisis Spasial | GWR + Kriging | Prediksi Harga Sewa & Tanah</strong>
</p>

<p align="center">
  <a href="https://github.com/burhanudin/portfolio_ilaspp_hybrid">
    <img src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github" alt="GitHub">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge&logo=opensourceinitiative" alt="License">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/R-4.5-276DC3?style=flat-square&logo=r" alt="R">
  <img src="https://img.shields.io/badge/PostgreSQL-17-4169E1?style=flat-square&logo=postgresql" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/PostGIS-3.4-4169E1?style=flat-square&logo=postgresql" alt="PostGIS">
  <img src="https://img.shields.io/badge/Scikit--Learn-1.6-F7931E?style=flat-square&logo=scikitlearn" alt="Scikit-Learn">
</p>

---

## 📌 **Project Overview**

Proyek **ILASPP** (Integrasi Data Spasial untuk Analisis Harga Properti di Indonesia) adalah sistem analisis dan prediksi harga properti berbasis **Geographically Weighted Regression (GWR)** dan **Kriging Interpolation**. Proyek ini dikembangkan untuk mendukung pengambilan keputusan di bidang pertanahan dan tata ruang, dengan cakupan **522 kabupaten/kota** di seluruh Indonesia.

### 🎯 Masalah Bisnis
- Penentuan nilai tanah oleh ATR/BPN seringkali kurang akurat karena tidak mempertimbangkan faktor spasial lokal
- Potensi penerimaan pajak daerah tidak optimal
- Masyarakat bisa dirugikan oleh penetapan nilai yang tidak sesuai

### 💡 Solusi yang Dikembangkan
- **Model GWR (R² = 86.61%)** : Menangkap variasi spasial lokal dengan optimal bandwidth 186m
- **Kriging Interpolation** : Memprediksi nilai di lokasi yang tidak terobservasi
- **Integrasi Data BPS** : 25 tabel indikator perumahan dan kesehatan lingkungan
- **Dashboard Interaktif** : Visualisasi dengan Streamlit dan Folium heatmap

### 📊 Dampak Bisnis
- ✅ Akurasi prediksi nilai properti yang tinggi
- ✅ Mendukung keputusan tata ruang dan perpajakan
- ✅ Cakupan 100% kabupaten/kota di Indonesia

---

## 🏗️ **Arsitektur Proyek**


```mermaid
portfolio_ilaspp_hybrid/
│
├── 📁 data/ # Data mentah & processed
│ ├── raw/ # Data asli (PDF BPS, GeoJSON)
│ │ ├── indicators-for-housing-and-health-of-environment-2024.pdf
│ │ └── harga-konsumen-kabupaten-kota-di-indonesia-2024.pdf
│ ├── processed/ # Data setelah cleaning
│ │ ├── master_data_perumahan.xlsx
│ │ ├── dataset_gwr_clean.csv
│ │ ├── dataset_gwr_522_kabupaten.csv
│ │ └── prediksi_522_kabupaten_kota.csv
│ └── geojson/ # Data spasial
│ ├── kabupaten_indonesia.geojson
│ ├── prediksi_522_kabupaten.geojson
│ └── koordinat_provinsi_2024.xlsx
│
├── 📁 notebooks/ # Jupyter Notebooks
│ ├── 01_ekstraksi_data.ipynb # Ekstraksi dari PDF BPS
│ ├── 02_cleaning_merge.ipynb # Pembersihan & penggabungan data
│ ├── 03_gwr_analysis.ipynb # Analisis GWR
│ └── 04_visualization.ipynb # Visualisasi & peta
│
├── 📁 R_version/ # ✅ Analisis spasial dengan R
│ ├── 01_data_preparation.R # Load & prep data
│ ├── 02_gwr_analysis_final.R # GWR analysis (R²=96.9%)
│ ├── 03_kriging_analysis.R # Kriging interpolation
│ ├── 04_visualization.R # Visualisasi output
│ └── 📁 output/ # Hasil GWR & Kriging
│
├── 📁 src/ # Script Python
│ ├── Python_version/
│ │ ├── streamlit_app.py # Dashboard utama
│ │ ├── spatial_analysis.py # Fungsi analisis spasial
│ │ ├── llm_agent.py # AI Assistant (Gemini)
│ │ └── pages/
│ │ ├── 01_dashboard.py
│ │ ├── 02_gwr_viewer.py
│ │ └── 03_kriging_viewer.py
│ ├── database/
│ │ ├── db_connector.py
│ │ ├── init_db.py
│ │ └── sample_data_generator.py
│ └── app.py # Aplikasi utama
│
├── 📁 outputs/ # Hasil akhir
│ ├── figures/ # Grafik & peta
│ │ ├── peta_full_indonesia_522.png
│ │ ├── peta_choropleth_combined_full.png
│ │ ├── bubble_maps_combined.png
│ │ ├── 1_top_bottom_rumah_layak_huni.png
│ │ ├── 2_korelasi_indikator.png
│ │ ├── 3_air_vs_sanitasi.png
│ │ └── 4_pengeluaran_perumahan.png
│ ├── models/ # Model & koefisien
│ │ ├── model_info.json
│ │ ├── gwr_coefficients.csv
│ │ └── kriging_predictions.csv
│ └── reports/ # Laporan analisis
│ ├── ringkasan_executive.xlsx
│ ├── hasil_analisis_perumahan.xlsx
│ └── regresi_spasial_results.csv
│
├── 📁 deploy_ilaspp/ # File deployment
│ ├── app.py
│ ├── requirements.txt
│ ├── packages.txt
│ └── *.csv (data untuk deployment)
│
├── 📁 docs/ # Dokumentasi
│ └── images/ # Gambar dokumentasi
│
├── 📄 requirements.txt # Python dependencies
├── 📄 .env.example # Template environment
└── 📄 README.md # Dokumentasi ini
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

### 1️⃣ Clone Repository

```bash
git clone https://github.com/burhanudinera2018/portfolio_ilaspp_hybrid.git
cd portfolio_ilaspp_hybrid

```

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

## 📊 Hasil Analisis
📈 GWR (Geographically Weighted Regression)
A. Model Regresi Spasial (Harga Sewa)
Metrik	Nilai	Interpretasi
R²	86.61%	Model menjelaskan variasi harga sewa
RMSE	2,708	Akurasi prediksi
Peningkatan	+3.94%	vs Regresi Linear global
📌 Top 5 Faktor Pengaruh Harga Sewa:
Faktor	Koefisien	Pengaruh
🥇 Status Kontrak/Sewa	+8,160	Paling Kuat
🥈 Ketahanan Bangunan	+6,969	Sangat Kuat
🥉 Akses Air Minum	+4,350	Kuat
4️⃣ Akses Sanitasi	+3,541	Kuat
5️⃣ Rumah Layak Huni	-8,667	Negatif
B. Model GWR (Nilai Tanah)
Metrik	Nilai	Interpretasi
R² (gw.R2)	0.4237	Model menjelaskan 42.4% variasi nilai tanah
Mean Local R²	0.4241	Kualitas model konsisten di semua lokasi
Bandwidth Optimal	186 meter	Menangkap variasi spasial lokal
📌 Koefisien:

Variabel	Rata-rata	Interpretasi
📍 Distance Center	-1.2155	100% negatif → semakin jauh dari pusat, nilai tanah TURUN
🛣️ Road Width	+0.2436	100% positif → semakin lebar jalan, nilai tanah NAIK
🌐 Kriging Interpolation
Metrik	Nilai
📈 Range Prediksi	14.34 - 40.65 juta/m²
📊 Mean Prediksi	23.87 juta/m²
🗺️ Cakupan Data
Metrik	Nilai
Kabupaten/Kota	522
Provinsi	34
Cakupan	100% Indonesia
🛠️ Teknologi yang Digunakan
Komponen	Teknologi	Logo
Database	PostgreSQL 17 + PostGIS	🐘
Analisis Spasial (R)	GWmodel, gstat, sf, sp	📊
Dashboard (Python)	Streamlit, Plotly, Pandas	🐍
Machine Learning	Scikit-learn, XGBoost	🤖
Visualisasi	Plotly, Folium, Matplotlib, Seaborn	🎨
LLM	Google Gemini 2.5 Flash (opsional)	🤖
Geospatial	GeoPandas, Shapely	🗺️
📸 Screenshot Dashboard
Halaman	Fitur
🏠 Dashboard Utama	Peta interaktif 522 kab/kota, statistik, bar chart
📈 GWR Results	Distribusi koefisien, Local R² map, bubble maps
🌐 Kriging Results	Peta prediksi, uncertainty map, contour plot
📊 Perbandingan	Interpretasi & rekomendasi kebijakan
📂 Dataset Tambahan
Proyek ini juga mengekstrak dan menganalisis data dari publikasi BPS:

Indikator Perumahan dan Kesehatan Lingkungan 2024 (25 tabel)

Data Sewa/Kontrak Rumah per Provinsi (2022-2024)

Data 522 Kabupaten/Kota dari GeoJSON BNPB

👤 Author
Burhanudin Badiuzaman
Data Scientist | Spatial Analytics Enthusiast

<p align="left"> <a href="https://github.com/burhanudinera2018"> <img src="https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github" alt="GitHub"> </a> <a href="https://www.linkedin.com/in/burhanudin-badiuzaman4a9204161/"> <img src="https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat-square&logo=linkedin" alt="LinkedIn"> </a> </p>
📝 Lisensi
Distributed under the MIT License. See LICENSE for more information.

🙏 Acknowledgments
ATR/BPN - ILASPP Project (Integrated Land Administration and Spatial Planning)

World Bank - Technical framework and support

BPS - Survei Sosial Ekonomi Nasional (Susenas) 2024

Open Source Community - R, Python, PostgreSQL, Streamlit

<p align="center"> <i>Built with ❤️ for Data Analytics | Spatial Analytics Portfolio</i> </p> 

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
```
