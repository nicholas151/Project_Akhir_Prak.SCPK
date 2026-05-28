import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

st.set_page_config(
    page_title="SPK Smartphone — Fuzzy Mamdani",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    try:
        df = pd.read_csv('ndtv_data_final.csv')
        kolom_penting = ['Price', 'RAM (MB)', 'Battery capacity (mAh)']
        df = df.dropna(subset=kolom_penting)
        return df
    except FileNotFoundError:
        # Dummy data sebagai fallback
        data = {'Name': ['HP Hemat', 'HP Nanggung', 'HP Sultan', 'HP Gaib'], 
                'Price': [5000, 15000, 25000, 8000], 
                'RAM (MB)': [2000, 8000, 12000, 4000], 
                'Battery capacity (mAh)': [3000, 4500, 6000, 5000]}
        return pd.DataFrame(data)

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

    menu = st.radio("", ["Beranda", "Dataset", "Perhitungan SPK"], label_visibility="collapsed")

    st.markdown("""
    <div style='margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.07);'>
        <div style='font-size: 0.72rem; color: #374151; line-height: 1.5;'>
            Metode <b style='color:#6366f1'>Fuzzy Mamdani (Skfuzzy)</b><br>
            Hafizd Sidiq Abdurrahman - 123240167<br><br>
            Nicholas Rafael Putra M. - 123240151<br><br>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# HALAMAN BERANDA
# ==============================
if "Beranda" in menu:
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Sistem Pendukung<br>Keputusan Smartphone</h1>
        <p class="hero-sub">
            Menggunakan metode <strong style="color:#a5b4fc">Fuzzy Mamdani (Library skfuzzy)</strong> untuk menemukan
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
            <div class="stat-number">10</div>
            <div class="stat-label">Rule Base Aktif</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    cards = [
        ("Kriteria Harga", "Himpunan: Murah, Sedang, Mahal."),
        ("Kriteria RAM", "Himpunan: Kecil, Sedang, Besar."),
        ("Kriteria Baterai", "Himpunan: Boros, Sedang, Awet."),
    ]
    for col, (name, desc) in zip([col1, col2, col3], cards):
        with col:
            st.markdown(f"""
            <div class="criteria-card">
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
# HALAMAN PERHITUNGAN SPK (MAMDANI DINAMIS)
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
        Atur batas himpunan pada slider di bawah ini. 
    </p>
    """, unsafe_allow_html=True)

    # --- LANGKAH 1: PENGATURAN BATAS HIMPUNAN (SLIDER) ---
    st.markdown("""
    <div class="section-header">
        <span class="section-num">1</span>
        <span class="section-title">Pengaturan Batas Himpunan</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Harga (Murah, Sedang, Mahal)**")
        batas_harga = st.slider("Batas Transisi Harga", min_value=0, max_value=30000, value=(7000, 18000), step=500)
    with col2:
        st.markdown("**RAM (Kecil, Sedang, Besar)**")
        batas_ram = st.slider("Batas Transisi RAM", min_value=0, max_value=16000, value=(3000, 8000), step=500)
    with col3:
        st.markdown("**Baterai (Boros, Sedang, Awet)**")
        batas_baterai = st.slider("Batas Transisi Baterai", min_value=1000, max_value=8000, value=(3000, 5500), step=100)

    # --- SETUP ENGINE FUZZY MENGGUNAKAN NILAI SLIDER ---
    
    # Universe Setup 
    harga_univ = np.arange(0, 30001, 1)    
    ram_univ = np.arange(0, 16385, 1)      
    baterai_univ = np.arange(1000, 8001, 1)
    skor_univ = np.arange(0, 101, 1)       

    harga = ctrl.Antecedent(harga_univ, 'harga')
    ram = ctrl.Antecedent(ram_univ, 'ram')
    baterai = ctrl.Antecedent(baterai_univ, 'baterai')
    skor = ctrl.Consequent(skor_univ, 'skor')

    # Logika Geometri Sempurna: Memastikan jumlah fungsi keanggotaan = 1 di titik temu
    a_h, b_h = batas_harga
    mid_h = (a_h + b_h) / 2
    harga['murah'] = fuzz.trapmf(harga.universe, [0, 0, a_h, mid_h])
    harga['sedang'] = fuzz.trimf(harga.universe, [a_h, mid_h, b_h])
    harga['mahal'] = fuzz.trapmf(harga.universe, [mid_h, b_h, 30000, 30000])

    a_r, b_r = batas_ram
    mid_r = (a_r + b_r) / 2
    ram['kecil'] = fuzz.trapmf(ram.universe, [0, 0, a_r, mid_r])
    ram['sedang'] = fuzz.trimf(ram.universe, [a_r, mid_r, b_r])
    ram['besar'] = fuzz.trapmf(ram.universe, [mid_r, b_r, 16384, 16384])

    a_b, b_b = batas_baterai
    mid_b = (a_b + b_b) / 2
    baterai['boros'] = fuzz.trapmf(baterai.universe, [1000, 1000, a_b, mid_b])
    baterai['sedang'] = fuzz.trimf(baterai.universe, [a_b, mid_b, b_b])
    baterai['awet'] = fuzz.trapmf(baterai.universe, [mid_b, b_b, 8000, 8000])

    # Himpunan Output Skor (Statis, 0-100)
    skor['rendah'] = fuzz.trapmf(skor.universe, [0, 0, 40, 60])
    skor['sedang'] = fuzz.trimf(skor.universe, [40, 60, 80])
    skor['tinggi'] = fuzz.trapmf(skor.universe, [60, 80, 100, 100])

    # Rule Base Terstruktur
    r1 = ctrl.Rule(harga['murah'] & ram['besar'] & baterai['awet'], skor['tinggi'])
    r2 = ctrl.Rule(harga['murah'] & ram['sedang'], skor['sedang'])
    r3 = ctrl.Rule(harga['murah'] & ram['kecil'], skor['rendah'])
    r4 = ctrl.Rule(harga['sedang'] & ram['besar'], skor['tinggi'])
    r5 = ctrl.Rule(harga['sedang'] & ram['sedang'], skor['sedang'])
    r6 = ctrl.Rule(harga['sedang'] & ram['kecil'], skor['rendah'])
    r7 = ctrl.Rule(harga['mahal'] & ram['besar'], skor['sedang'])
    r8 = ctrl.Rule(harga['mahal'] & ram['sedang'], skor['rendah'])
    r9 = ctrl.Rule(harga['mahal'] & ram['kecil'], skor['rendah'])
    r10 = ctrl.Rule(baterai['boros'], skor['rendah'])

    sistem_kontrol = ctrl.ControlSystem([r1, r2, r3, r4, r5, r6, r7, r8, r9, r10])
    simulasi = ctrl.ControlSystemSimulation(sistem_kontrol)

    # --- LANGKAH 2: VISUALISASI KURVA HIMPUNAN ---
    st.markdown("""
    <div class="section-header" style='margin-top:2rem;'>
        <span class="section-num">2</span>
        <span class="section-title">Fungsi Keanggotaan Fuzzy</span>
    </div>
    """, unsafe_allow_html=True)

    fig, axes = plt.subplots(1, 3, figsize=(14, 3.5))
    fig.patch.set_facecolor('#0f1629')

    # Plot Harga
    axes[0].set_facecolor('#111827')
    axes[0].plot(harga.universe, harga['murah'].mf, color='#34d399', linewidth=2, label='Murah')
    axes[0].plot(harga.universe, harga['sedang'].mf, color='#facc15', linewidth=2, label='Sedang')
    axes[0].plot(harga.universe, harga['mahal'].mf, color='#f87171', linewidth=2, label='Mahal')
    axes[0].set_title("Kriteria Harga", color='#e0e7ff', fontsize=11, fontweight='bold', pad=10)
    
    # Plot RAM
    axes[1].set_facecolor('#111827')
    axes[1].plot(ram.universe, ram['kecil'].mf, color='#f87171', linewidth=2, label='Kecil')
    axes[1].plot(ram.universe, ram['sedang'].mf, color='#facc15', linewidth=2, label='Sedang')
    axes[1].plot(ram.universe, ram['besar'].mf, color='#34d399', linewidth=2, label='Besar')
    axes[1].set_title("Kriteria RAM", color='#e0e7ff', fontsize=11, fontweight='bold', pad=10)

    # Plot Baterai
    axes[2].set_facecolor('#111827')
    axes[2].plot(baterai.universe, baterai['boros'].mf, color='#f87171', linewidth=2, label='Boros')
    axes[2].plot(baterai.universe, baterai['sedang'].mf, color='#facc15', linewidth=2, label='Sedang')
    axes[2].plot(baterai.universe, baterai['awet'].mf, color='#34d399', linewidth=2, label='Awet')
    axes[2].set_title("Kriteria Baterai", color='#e0e7ff', fontsize=11, fontweight='bold', pad=10)

    for ax in axes:
        ax.tick_params(colors='#374151', labelsize=8)
        ax.spines[:].set_color('#1f2937')
        ax.legend(fontsize=8, loc="best", facecolor='#111827', edgecolor='#1f2937', labelcolor='#e0e7ff')

    plt.tight_layout(pad=1.5)
    st.pyplot(fig, use_container_width=True)
    plt.close()

    # --- LANGKAH 3: EKSEKUSI MAMDANI ---
    st.markdown("""
    <div class="section-header" style='margin-top:2rem;'>
        <span class="section-num">3</span>
        <span class="section-title">Hitung & Defuzzifikasi (Skfuzzy Centroid)</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Hitung Rekomendasi Mamdani"):
        hasil_z = []
        
        for index, row in df.iterrows():
            h, r, b = row['Price'], row['RAM (MB)'], row['Battery capacity (mAh)']
            
            # np.clip mencegah error saat ada data jauh di luar batas slider
            simulasi.input['harga'] = np.clip(h, 0, 30000)
            simulasi.input['ram'] = np.clip(r, 0, 16384)
            simulasi.input['baterai'] = np.clip(b, 1000, 8000)

            try:
                simulasi.compute()
                hasil = simulasi.output['skor']
            except ValueError:
                hasil = 0 
                
            hasil_z.append(hasil)

        df_hasil = df.copy()
        df_hasil['Skor Kelayakan'] = hasil_z
        
        # Urutkan berdasarkan skor tertinggi
        df_hasil = df_hasil.sort_values('Skor Kelayakan', ascending=False).reset_index(drop=True)
        df_hasil.index = df_hasil.index + 1

        # Menampilkan tabel Top 20
        tampil_cols = ['Name', 'Price', 'RAM (MB)', 'Battery capacity (mAh)', 'Skor Kelayakan']
        
        st.markdown("<br><p style='font-family:Syne; font-weight:700; color:#e0e7ff;'>Tabel Hasil Defuzzifikasi (Top 20)</p>", unsafe_allow_html=True)
        st.dataframe(
            df_hasil.head(20)[tampil_cols].style
            .background_gradient(subset=['Skor Kelayakan'], cmap='Purples')
            .format({'Skor Kelayakan': '{:.2f}'}),
            use_container_width=True, height=350
        )

        # Menampilkan Top 5 Visual
        st.markdown("<br><div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#e0e7ff;'>Top 5 Rekomendasi Produk</div><br>", unsafe_allow_html=True)

        top5 = df_hasil.head(5)
        rank_icons = ["1", "2", "3", "4", "5"]
        rank_classes = ["top1", "top2", "top3", "", ""]
        
        for i, row in top5.iterrows():
            idx = i - 1
            score = row['Skor Kelayakan']
            bar_w = int(score)
            
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