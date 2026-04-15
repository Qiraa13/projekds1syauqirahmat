import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

# Konfigurasi Halaman
st.set_page_config(page_title="Portal Analitik Karyawan", layout="wide", page_icon="🏢")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* Styling Card/Box untuk hasil prediksi */
    .card-res {
        background-color: #2b2b2b;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin-top: 10px;
        color: #ffffff; /* Memastikan teks berwarna putih agar terbaca di background gelap */
    }
    .card-res p, .card-res h4 {
        color: #ffffff !important;
    }
    .card-safe {
        background-color: #2b2b2b;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00cc96;
        margin-top: 10px;
        color: #ffffff;
    }
    .card-safe p, .card-safe h4 {
        color: #ffffff !important;
    }
    
    /* Mengatur ulang padding agar atas tidak kepotong tapi tetap lebar */
    .block-container {
        padding-top: 3rem !important; /* Diberi ruang agar ikon pilar tidak kepotong */
        padding-bottom: 1rem !important;
        max-width: 95% !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER & NAVIGATION ---
# Menggunakan 2 kolom dengan rasio seimbang agar menu navigasi punya ruang lebar dan tidak menjadi 2 baris
head_col1, head_col2 = st.columns([1.3, 1])

with head_col1:
    st.markdown("<h2 style='margin-bottom:0px; margin-top:0px;'>🏛️ PORTAL ANALITIK KARYAWAN</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6c757d; margin-top:0px;'>Sistem Manajemen & Prediksi Atrisi Cerdas terintegrasi dengan Looker Studio.</p>", unsafe_allow_html=True)

with head_col2:
    selected = option_menu(
        menu_title=None, 
        options=["Home", "Form Prediksi"], 
        icons=["house-door-fill", "magic"], 
        menu_icon="cast", 
        default_index=0, 
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent", "margin-top":"0px"},
            "icon": {"font-size": "16px"}, 
            # Dibuat satu baris agar tulisan tidak turun/berubah ukuran box
            "nav-link": {"font-size": "15px", "text-align": "center", "margin":"0px", "white-space":"nowrap"},
            "nav-link-selected": {"background-color": "#4070f4"}, # Warna biru khas link
        }
    )

st.markdown("---")

# --- HALAMAN 1: HOME ---
if selected == "Home":
    
    # Menampilkan Looker Studio Iframe
    # Height diperbesar sangat signifikan (1200) agar dashboard Looker tidak terpotong Scrollbar dari iframe
    components.html(
        """
        <div style="box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1); border-radius: 10px; overflow:hidden; width: 100%; height: 100%;">
            <iframe width="100%" height="1200px" src="https://lookerstudio.google.com/embed/reporting/5bf1486c-3c9d-49a3-ab6d-b0f6243f304e/page/K1nrF" frameborder="0" style="border:0" allowfullscreen sandbox="allow-storage-access-by-user-activation allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox"></iframe>
        </div>
        """,
        height=1200, # Ketinggian komponen streamlit dinaikkan tajam
    )

# --- HALAMAN 2: FORM PREDIKSI ---
elif selected == "Form Prediksi":
    st.markdown("### 🔮 Mode Kalkulasi Risiko Resign")
    
    with st.expander("ℹ️ **CARA PENGGUNAAN FORMULIR**", expanded=True):
        st.write("1. Pastikan Anda memasukkan metrik karyawan yang sesuai dengan pembaharuan data terakhir.")
        st.write("2. Kolom *Work Life Balance* menggunakan skala **1 (Sangat Buruk)** hingga **4 (Sangat Baik)**.")
        st.write("3. Setelah semua terisi, tekan tombol biru **Jalankan Prediksi** di bagian bawah form.")

    # Frame Utama
    with st.container():
        with st.form("attrition_form", clear_on_submit=False):
            st.markdown("#### 📝 Formulir Evaluasi Individu")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                department = st.selectbox("🎯 Department", ["Research & Development", "Sales", "Human Resources"])
                age = st.number_input("🎂 Age (Umur)", min_value=18, max_value=100, value=30)
                daily_rate = st.number_input("💵 Daily Rate", min_value=0, max_value=5000, value=800)
            
            with c2:
                overtime = st.selectbox("⏳ Overtime (Sering Lembur?)", ["Yes", "No"])
                work_life_balance = st.selectbox("⚖️ Work Life Balance", [1, 2, 3, 4])
                total_working_years = st.number_input("💼 Total Working Years", min_value=0, max_value=50, value=5)
                
            with c3:
                years_at_company = st.number_input("🏢 Years at Company", min_value=0, max_value=50, value=3)
                years_in_current_role = st.number_input("👷 Years in Current Role", min_value=0, max_value=50, value=2)
                years_since_last_promotion = st.number_input("🚀 Years Since Promotion", min_value=0, max_value=50, value=1)
                
            st.markdown("<br>", unsafe_allow_html=True)
            submit_button = st.form_submit_button(label="🔄 PROSES PREDIKSI DATA", use_container_width=True)

    # AREA HASIL PREDIKSI
    if submit_button:
        st.markdown("---")
        st.markdown("### 📑 Kesimpulan & Hasil Analitis")
        
        with st.spinner("Menghubungkan ke Model Machine Learning (MLflow Version)..."):
            
            # --- REAL MACHINE LEARNING LOGIC ---
            import joblib
            try:
                # Membaca model yang sudah dilatih dan disimpan oleh MLflow/train_model.py
                model = joblib.load("attrition_model.pkl")
                
                input_df = pd.DataFrame([{
                    "Department": department,
                    "Age": age,
                    "DailyRate": daily_rate,
                    "OverTime": overtime,
                    "WorkLifeBalance": work_life_balance,
                    "TotalWorkingYears": total_working_years,
                    "YearsAtCompany": years_at_company,
                    "YearsInCurrentRole": years_in_current_role,
                    "YearsSinceLastPromotion": years_since_last_promotion
                }])
                
                try:
                    prob = model.predict_proba(input_df)[0][1] # index 1 adalah 'Yes'
                    probability = prob * 100
                except Exception as inner_e:
                    st.error(f"Error Model Probabilitas: {inner_e}")
                    probability = 0
            except Exception as e:
                st.error(f"Error Membaca Model attrition_model.pkl: {e}")
                probability = 0
            
            # Mempertahankan deteksi faktor secara manual untuk dijelaskan di UI
            risk_factors = []
            
            if overtime == "Yes":
                risk_factors.append("Terlalu sering mengambil lembur (Beban kerja berat).")
            if work_life_balance < 3:
                risk_factors.append(f"Tingkat Keseimbangan Kerja & Hidup rendah (Level {work_life_balance}).")
            if age < 30:
                risk_factors.append("Kategori usia muda (Millennial/Gen Z) memiliki mobilitas karir yang tinggi.")
            if years_since_last_promotion > 4:
                risk_factors.append(f"Stagnansi karir, belum ada promosi selama {years_since_last_promotion} tahun.")
            if daily_rate < 500:
                risk_factors.append("Insentif kompensasi *Daily Rate* di bawah rata-rata yang diharapkan.")
                
            # Memvisualisasikan Output
            col_res_1, col_res_2 = st.columns([1, 2.5])
            
            with col_res_1:
                st.metric(label="🎯 Peluang Karyawan Resign", value=f"{probability:.1f}%")
                color = "red" if probability >= 50 else "green"
                st.markdown(f'''
                    <div style="background-color: #2E3440; border-radius: 5px; width: 100%; height: 25px; border: 1px solid #4C566A;">
                      <div style="background-color: {color}; width: {probability}%; height: 100%; border-radius: 4px;"></div>
                    </div>
                ''', unsafe_allow_html=True)
                st.caption("Indikator Risiko Kritis")
                
            with col_res_2:
                if probability >= 50:
                    st.markdown("""
                    <div class="card-res">
                        <h4 style="margin-top:0px;">⚠️ STATUS: RISIKO TINGGI (DANGER ZONED)</h4>
                        <p>Karyawan ini terdeteksi memiliki profil yang berisiko kuat untuk <strong>meninggalkan perusahaan</strong> dalam 6 bulan ke depan.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if risk_factors:
                        st.markdown("🔍 **Faktor Pemberat Utama:**")
                        for rf in risk_factors:
                            st.markdown(f"- 🔴 {rf}")
                            
                    st.warning("💡 **Tindakan Intervensi yang Disarankan:** Segera jadwalkan meeting eksklusif (One-on-One) dengan karyawan terkait. Berikan penawaran negosiasi atau periksa keseimbangan kerjanya.")
                else:
                    st.markdown("""
                    <div class="card-safe">
                        <h4 style="margin-top:0px;">✅ STATUS: STABIL (SAFE ZONED)</h4>
                        <p>Karyawan ini berpeluang sangat tinggi untuk <strong>bertahan (Retain)</strong>. Motivasi, profil gaji, dan rotasi posisi dirasa cukup sehat.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.info("💡 **Tindakan Intervensi yang Disarankan:** Tidak ada urgensi khusus. Terus rawat interaksi yang baik dan siapkan bonus untuk mengapresiasi loyalitasnya.")
