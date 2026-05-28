import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="SPK Smartphone — Fuzzy Mamdani",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ===== GLOBAL ===== */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0a0e1a; color: #e8eaf2; }

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1326 0%, #111827 100%);
    border-right: 1px solid rgba(99, 102, 241, 0.2);
}
[data-testid="stSidebar"] .stRadio label {
    color: #9ca3af !important; font-size: 0.9rem; padding: 6px 0; transition: color 0.2s;
}
[data-testid="stSidebar"] .stRadio label:hover { color: #a5b4fc !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] .sidebar-title {
    font-family: 'Syne', sans-serif !important; color: #6366f1 !important;
    font-size: 1.1rem; letter-spacing: 0.05em; text-transform: uppercase;
}

/* ===== TYPOGRAPHY ===== */
h1, h2, h3 { font-family: 'Syne', sans-serif !important; letter-spacing: -0.02em; }

/* ===== HERO CARD ===== */
.hero-container {
    background: linear-gradient(135deg, #1a1f35 0%, #0f172a 60%, #1e1040 100%);
    border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 20px;
    padding: 3rem 3.5rem; margin-bottom: 2rem; position: relative; overflow: hidden;
}
.hero-container::before {
    content: ''; position: absolute; top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%); border-radius: 50%;
}
.hero-badge {
    display: inline-block; background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.4); color: #a5b4fc; font-size: 0.75rem;
    font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase;
    padding: 5px 14px; border-radius: 100px; margin-bottom: 1.2rem;
}
.hero-title {
    font-size: 2.8rem; font-weight: 800; line-height: 1.1; margin: 0 0 1rem 0;
    background: linear-gradient(135deg, #e0e7ff 0%, #a5b4fc 50%, #818cf8 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub { color: #6b7280; font-size: 1.05rem; line-height: 1.6; max-width: 520px; font-weight: 300; }

/* ===== STAT CARDS ===== */
.stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1.5rem 0; }
.stat-card {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 1.2rem 1.5rem; text-align: center;
    transition: border-color 0.2s, transform 0.2s;
}
.stat-card:hover { border-color: rgba(99,102,241,0.35); transform: translateY(-2px); }
.stat-number { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 700; color: #818cf8; line-height: 1; }
.stat-label { font-size: 0.78rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; }

/* ===== SECTION HEADERS ===== */
.section-header { display: flex; align-items: center; gap: 12px; margin: 2rem 0 1.2rem 0; }
.section-num {
    background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white;
    font-family: 'Syne', sans-serif; font-size: 0.8rem; font-weight: 700;
    width: 32px; height: 32px; border-radius: 8px; display: inline-flex;
    align-items: center; justify-content: center; flex-shrink: 0;
}
.section-title { font-family: 'Syne', sans-serif; font-size: 1.15rem; font-weight: 700; color: #e0e7ff; margin: 0; }

/* ===== CRITERIA CARDS ===== */
.criteria-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.criteria-card {
    background: rgba(255,255,255,0.03); border: 1.5px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 1.2rem; transition: all 0.2s;
}
.criteria-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }
.criteria-name { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.95rem; color: #e0e7ff; }
.criteria-desc { font-size: 0.78rem; color: #6b7280; margin-top: 2px; }

/* ===== TABLE STYLING ===== */
.stDataFrame { border-radius: 12px !important; overflow: hidden !important; border: 1px solid rgba(99,102,241,0.2) !important; }

/* ===== BUTTONS ===== */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important; color: white !important;
    border: none !important; border-radius: 10px !important; font-weight: 500 !important;
    font-size: 0.95rem !important; padding: 0.6rem 2.2rem !important;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }

/* ===== RESULT CARDS ===== */
.result-item {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 1rem 1.4rem; margin-bottom: 0.7rem; display: flex; align-items: center; gap: 1rem;
}
.result-rank { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 800; color: #4b5563; min-width: 36px; }
.result-rank.top1 { color: #f59e0b; } .result-rank.top2 { color: #9ca3af; } .result-rank.top3 { color: #b45309; }
.result-name { font-weight: 500; color: #e0e7ff; font-size: 0.95rem; flex: 1; }
.result-price { color: #6b7280; font-size: 0.85rem; }
.result-score { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.9rem; color: #818cf8; background: rgba(99,102,241,0.1); padding: 3px 10px; border-radius: 100px; }

hr { border-color: rgba(255,255,255,0.07) !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# --- 1. LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv('ndtv_data_final.csv')
    kolom_penting = ['Price', 'RAM (MB)', 'Battery capacity (mAh)']
    df = df.dropna(subset=kolom_penting)
    return df

df = load_data()

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0 1.5rem 0;'>
        <div style='font-family: Syne, sans-serif; font-size: 1.3rem; font-weight: 800;
                    background: linear-gradient(135deg, #818cf8, #a78bfa);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    background-clip: text; margin-bottom: 4px;'>
            FUZZY SPK
        </div>
        <div style='color: #4b5563; font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase;'>
            Sistem Cerdas Pemilihan HP
        </div>
    </div>
    <hr style='border-color: rgba(255,255,255,0.07); margin: 0 0 1.2rem 0;'>
    """, unsafe_allow_html=True)

    menu = st.radio("", ["🏠  Beranda", "📊  Dataset", "🔢  Perhitungan SPK", "👥  Profil Kelompok"], label_visibility="collapsed")

    st.markdown("""
    <div style='margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.07);'>
        <div style='font-size: 0.72rem; color: #374151; line-height: 1.5;'>
            Metode <b style='color:#6366f1'>Fuzzy Mamdani</b><br>
            Aplikasi Rule Base (MIN) & Defuzzifikasi Centroid (COA)<br><br>
            <span style='color:#4b5563'>UPN "Veteran" Yogyakarta</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# HALAMAN BERANDA
# ==============================
if "Beranda" in menu:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">📱 Decision Support System</div>
        <h1 class="hero-title">Sistem Pendukung<br>Keputusan Smartphone</h1>
        <p class="hero-sub">
            Menggunakan metode <strong style="color:#a5b4fc">Fuzzy Mamdani</strong> untuk menemukan
            smartphone terbaik berdasarkan fungsi implikasi (MIN), agregasi (MAX), dan defuzzifikasi titik berat (Centroid).
        </p>
    </div>
    """, unsafe_allow_html=True)

    total_hp = len(df)
    avg_price = int(df['Price'].mean())

    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-card">
            <div class="stat-number">{total_hp:,}</div>
            <div class="stat-label">Total Smartphone</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{avg_price:,}</div>
            <div class="stat-label">Rata-rata Harga</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">8</div>
            <div class="stat-label">Rule Base Aktif</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    cards = [
        ("💰", "Kriteria Harga", "Himpunan: Murah & Mahal."),
        ("🧠", "Kriteria RAM", "Himpunan: Kecil & Besar."),
        ("🔋", "Kriteria Baterai", "Himpunan: Boros & Awet."),
    ]
    for col, (icon, name, desc) in zip([col1, col2, col3], cards):
        with col:
            st.markdown(f"""
            <div class="criteria-card">
                <div class="criteria-icon">{icon}</div>
                <div class="criteria-name">{name}</div>
                <div class="criteria-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ==============================
# HALAMAN DATASET
# ==============================
elif "Dataset" in menu:
    st.markdown("""
    <div style='margin-bottom: 1.5rem;'>
        <h1 style='font-family: Syne, sans-serif; font-size: 2rem; font-weight: 800; color: #e0e7ff;'>Dataset Smartphone</h1>
        <p style='color: #4b5563; font-size: 0.9rem;'>Sumber: <code>ndtv_data_final.csv</code></p>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(df.head(250), use_container_width=True, height=460)

# ==============================
# HALAMAN PERHITUNGAN SPK (MAMDANI)
# ==============================
elif "Perhitungan" in menu:
    st.markdown("""
    <h1 style='font-family: Syne, sans-serif; font-size: 2rem; font-weight: 800;
               background: linear-gradient(135deg, #e0e7ff, #818cf8);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;
               background-clip: text; margin-bottom: 0.3rem;'>
        Proses Fuzzy Mamdani
    </h1>
    <p style='color:#4b5563; font-size:0.9rem; margin-bottom: 1.8rem;'>
        Fuzzifikasi → Evaluasi Rule (MIN) → Agregasi (MAX) → Defuzzifikasi (Centroid / COA)
    </p>
    """, unsafe_allow_html=True)

    # --- LANGKAH 1: KRITERIA ---
    st.markdown("""
    <div class="section-header">
        <span class="section-num">1</span>
        <span class="section-title">🔧 Pengaturan Batas Himpunan</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**💰 Harga (Murah & Mahal)**")
        batas_harga = st.slider("Batas (a) & (b) Harga", min_value=0, max_value=25000, value=(2000, 8000), step=500)
    with col2:
        st.markdown("**🧠 RAM (Kecil & Besar)**")
        batas_ram = st.slider("Batas (a) & (b) RAM", min_value=0, max_value=16000, value=(2000, 8000), step=500)
    with col3:
        st.markdown("**🔋 Baterai (Boros & Awet)**")
        batas_baterai = st.slider("Batas (a) & (b) Baterai", min_value=1000, max_value=7000, value=(3000, 5000), step=100)

    # FUNGSI FUZZIFIKASI (TURUN = Kiri, NAIK = Kanan)
    def fuzzy_turun(x, a, b):
        if x <= a: return 1.0
        elif x >= b: return 0.0
        else: return (b - x) / (b - a)

    def fuzzy_naik(x, a, b):
        if x <= a: return 0.0
        elif x >= b: return 1.0
        else: return (x - a) / (b - a)
        
    # FUNGSI OUTPUT MAMDANI (Kelayakan 0 - 100)
    # Output Rendah = Fungsi Turun Linier 0 ke 100
    # Output Tinggi = Fungsi Naik Linier 0 ke 100
    def mu_out_rendah(z):
        return (100 - z) / 100
        
    def mu_out_tinggi(z):
        return z / 100

    # --- LANGKAH 2: VISUALISASI KURVA INTERAKTIF ---
    st.markdown("""
    <div class="section-header" style='margin-top:2rem;'>
        <span class="section-num">2</span>
        <span class="section-title">📊 Fungsi Keanggotaan Fuzzy (Input)</span>
    </div>
    """, unsafe_allow_html=True)

    fig, axes = plt.subplots(1, 3, figsize=(14, 3.5))
    fig.patch.set_facecolor('#0f1629')

    configs = [
        ("Kriteria Harga", np.linspace(0, 25000, 300), batas_harga, "Harga (unit)", ["Murah", "Mahal"]),
        ("Kriteria RAM", np.linspace(0, 16000, 300), batas_ram, "RAM (MB)", ["Kecil", "Besar"]),
        ("Kriteria Baterai", np.linspace(1000, 7000, 300), batas_baterai, "Kapasitas (mAh)", ["Boros", "Awet"])
    ]

    for ax, (title, x_vals, batas, xlabel, labels) in zip(axes, configs):
        a, b = batas
        y_turun = [fuzzy_turun(x, a, b) for x in x_vals]
        y_naik = [fuzzy_naik(x, a, b) for x in x_vals]

        ax.set_facecolor('#111827')
        ax.plot(x_vals, y_turun, color='#f87171', linewidth=2.2, label=labels[0])
        ax.plot(x_vals, y_naik, color='#34d399', linewidth=2.2, label=labels[1])
        ax.fill_between(x_vals, y_turun, alpha=0.1, color='#f87171')
        ax.fill_between(x_vals, y_naik, alpha=0.1, color='#34d399')
        
        ax.set_title(title, color='#e0e7ff', fontsize=11, fontweight='bold', pad=10)
        ax.set_xlabel(xlabel, color='#4b5563', fontsize=9)
        ax.set_ylabel("μ(x)", color='#4b5563', fontsize=9)
        ax.tick_params(colors='#374151', labelsize=8)
        ax.spines[:].set_color('#1f2937')
        ax.legend(fontsize=8, loc="center right")

    plt.tight_layout(pad=1.5)
    st.pyplot(fig, use_container_width=True)
    plt.close()

    # --- LANGKAH 3: EKSEKUSI MAMDANI ---
    st.markdown("""
    <div class="section-header" style='margin-top:2rem;'>
        <span class="section-num">3</span>
        <span class="section-title">🏆 Hitung & Defuzzifikasi (Centroid)</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⚡  Hitung Rekomendasi Mamdani"):
        hasil_z = []
        
        # Domain evaluasi Z untuk integrasi numerik (Center of Area)
        # Menggunakan 101 titik dari 0 hingga 100
        z_domain = np.linspace(0, 100, 101)

        for index, row in df.iterrows():
            h, r, b = row['Price'], row['RAM (MB)'], row['Battery capacity (mAh)']

            # 1. Fuzzifikasi
            mu_h_murah = fuzzy_turun(h, batas_harga[0], batas_harga[1])
            mu_h_mahal = fuzzy_naik(h, batas_harga[0], batas_harga[1])
            
            mu_r_kecil = fuzzy_turun(r, batas_ram[0], batas_ram[1])
            mu_r_besar = fuzzy_naik(r, batas_ram[0], batas_ram[1])
            
            mu_b_boros = fuzzy_turun(b, batas_baterai[0], batas_baterai[1])
            mu_b_awet  = fuzzy_naik(b, batas_baterai[0], batas_baterai[1])

            # 2. Evaluasi Rules (Alpha-Predicate pakai fungsi MIN)
            # R1: IF Murah AND Besar AND Awet THEN Kelayakan TINGGI
            a1 = min(mu_h_murah, mu_r_besar, mu_b_awet) # Output: TINGGI
            # R2: IF Murah AND Besar AND Boros THEN Kelayakan TINGGI
            a2 = min(mu_h_murah, mu_r_besar, mu_b_boros) # Output: TINGGI
            # R3: IF Murah AND Kecil AND Awet THEN Kelayakan TINGGI
            a3 = min(mu_h_murah, mu_r_kecil, mu_b_awet) # Output: TINGGI
            # R4: IF Murah AND Kecil AND Boros THEN Kelayakan RENDAH
            a4 = min(mu_h_murah, mu_r_kecil, mu_b_boros) # Output: RENDAH
            # R5: IF Mahal AND Besar AND Awet THEN Kelayakan TINGGI
            a5 = min(mu_h_mahal, mu_r_besar, mu_b_awet) # Output: TINGGI
            # R6: IF Mahal AND Besar AND Boros THEN Kelayakan RENDAH
            a6 = min(mu_h_mahal, mu_r_besar, mu_b_boros) # Output: RENDAH
            # R7: IF Mahal AND Kecil AND Awet THEN Kelayakan RENDAH
            a7 = min(mu_h_mahal, mu_r_kecil, mu_b_awet) # Output: RENDAH
            # R8: IF Mahal AND Kecil AND Boros THEN Kelayakan RENDAH
            a8 = min(mu_h_mahal, mu_r_kecil, mu_b_boros) # Output: RENDAH

            # 3. Agregasi Output (Fungsi MAX)
            alpha_tinggi = max(a1, a2, a3, a5)
            alpha_rendah = max(a4, a6, a7, a8)

            # 4. Defuzzifikasi (Metode Centroid / Center of Area)
            numerator = 0
            denominator = 0
            
            for z in z_domain:
                # Memotong luasan (Implikasi) & menggabungkan (Agregasi)
                # Area Rendah dipotong oleh alpha_rendah, Area Tinggi dipotong oleh alpha_tinggi
                mu_z_rendah = min(alpha_rendah, mu_out_rendah(z))
                mu_z_tinggi = min(alpha_tinggi, mu_out_tinggi(z))
                
                # Fungsi keanggotaan gabungan pada titik Z
                mu_gabungan = max(mu_z_rendah, mu_z_tinggi)
                
                numerator += z * mu_gabungan
                denominator += mu_gabungan
            
            # Hitung titik berat (Z*)
            Z_akhir = numerator / denominator if denominator != 0 else 0
            hasil_z.append(Z_akhir)

        df_hasil = df.copy()
        df_hasil['Skor Kelayakan'] = hasil_z
        
        # Urutkan berdasarkan skor tertinggi
        df_hasil = df_hasil.sort_values('Skor Kelayakan', ascending=False).reset_index(drop=True)
        df_hasil.index = df_hasil.index + 1

        # Menampilkan tabel
        tampil_cols = ['Name', 'Price', 'RAM (MB)', 'Battery capacity (mAh)', 'Skor Kelayakan']
        
        st.markdown("<br><p style='font-family:Syne; font-weight:700; color:#e0e7ff;'>Tabel Hasil Defuzzifikasi (Top 20)</p>", unsafe_allow_html=True)
        st.dataframe(
            df_hasil.head(20)[tampil_cols].style
            .background_gradient(subset=['Skor Kelayakan'], cmap='Purples')
            .format({'Skor Kelayakan': '{:.2f}'}),
            use_container_width=True, height=350
        )

        # Menampilkan Top 5
        st.markdown("<br><div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#e0e7ff;'>🏆 Top 5 Rekomendasi Produk</div><br>", unsafe_allow_html=True)

        top5 = df_hasil.head(5)
        rank_icons = ["🥇", "🥈", "🥉", "4.", "5."]
        rank_classes = ["top1", "top2", "top3", "", ""]
        
        for i, row in top5.iterrows():
            idx = i - 1
            score = row['Skor Kelayakan']
            bar_w = int(score)  # score mamdani direntang 0 - 100
            
            st.markdown(f"""
            <div class="result-item">
                <div class="result-rank {rank_classes[idx]}">{rank_icons[idx]}</div>
                <div style='flex:1;'>
                    <div class="result-name">{row['Name']}</div>
                    <div class="result-price">Harga: {int(row['Price']):,} &nbsp;·&nbsp;
                        RAM: {int(row['RAM (MB)']):,} MB &nbsp;·&nbsp;
                        Baterai: {int(row['Battery capacity (mAh)']):,} mAh
                    </div>
                    <div style='margin-top:5px;height:3px;background:#1f2937;border-radius:2px;'>
                        <div style='width:{bar_w}%;height:100%;
                                    background:linear-gradient(90deg,#6366f1,#8b5cf6);
                                    border-radius:2px;'></div>
                    </div>
                </div>
                <div class="result-score">{score:.2f} / 100</div>
            </div>
            """, unsafe_allow_html=True)

# ==============================
# HALAMAN PROFIL KELOMPOK
# ==============================
elif "Profil" in menu:
    st.markdown("""
    <h1 style='font-family:Syne,sans-serif;font-size:2rem;font-weight:800;
               background:linear-gradient(135deg,#e0e7ff,#818cf8);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               background-clip:text;margin-bottom:0.3rem;'>
        Profil Kelompok
    </h1>
    <p style='color:#4b5563;font-size:0.9rem;margin-bottom:2rem;'>
        Proyek Akhir — Sistem Cerdas Pendukung Keputusan
    </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    members = [("👨‍💻", "Nicholas Rafael Putra M.", "Praktikan SCPK"), ("👨", "Hafizd S. Abdurrahman", "Praktikan SCPK")]
    for col, (icon, name, role) in zip([col1, col2], members):
        with col:
            st.markdown(f"""
            <div class="profile-card" style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:2rem; text-align:center;">
                <div style="width:70px;height:70px; background:linear-gradient(135deg,#6366f1,#8b5cf6); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.8rem; margin:0 auto 1rem auto;">{icon}</div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.05rem;color:#e0e7ff;margin-bottom:4px;">{name}</div>
                <div style="color:#6b7280;font-size:0.83rem;letter-spacing:0.05em;text-transform:uppercase;">{role}</div>
            </div>
            """, unsafe_allow_html=True)