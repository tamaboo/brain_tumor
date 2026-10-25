import streamlit as st
import streamlit.components.v1 as components
from admin.auth import (init_auth_state, login_user, logout_user,
                        pulihkan_sesi, sinkronkan_cookie)
from navbar.edukasi import tampilkan_edukasi
from navbar.panduan import tampilkan_panduan
from navbar.chatbot import tampilkan_chatbot_floating
from admin.manajemen_pasien import tampilkan_manajemen_pasien
from navbar.header import tampilkan_header, tampilkan_splash
from navbar.kamus_bahasa import t
from navbar.login_ui import tampilkan_login
from admin.akun import (tampilkan_akun_saya, tampilkan_kelola_staf,
                        tampilkan_ganti_password, buka_dialog_logout, L as LA)

# 1. KONFIGURASI HALAMAN WAJIB DI BARIS PERTAMA
st.set_page_config(
    page_title="NeuroSight | Brain Tumor Diagnostics (XAI)",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Injeksi CSS untuk memblokir Sidebar, memperindah Tab, dan memperjelas UI yang samar
st.markdown("""
    <style>
        [data-testid="collapsedControl"] {display: none;}
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        .stTabs [data-baseweb="tab-list"] {
            display: flex;
            justify-content: center;
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 18px;
            font-weight: 600;
        }
        
        /* --- PERBAIKAN VISUAL BORDER & INPUT --- */
        [data-testid="stForm"], [data-testid="stDataEditor"] {
            border: 2px solid #A0AAB5 !important; /* Border Form & Tabel agar tegas */
            border-radius: 10px !important;
            background-color: rgba(255, 255, 255, 0.95) !important; /* Background putih solid menutupi pattern */
            box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
        }
        
        .stTextInput input, .stNumberInput input {
            border: 1px solid #7B8A9B !important; /* Border kotak teks */
            background-color: #ffffff !important;
            color: #1E1E1E !important;
        }
        
        div[data-baseweb="select"] > div {
            border: 1px solid #7B8A9B !important; /* Border kotak dropdown */
            background-color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Bungkus semua proses background & header di dalam 1 container tetap 
top_wrapper = st.container()
with top_wrapper:
    tampilkan_splash()
    init_auth_state()
    pulihkan_sesi()
    sinkronkan_cookie()
    
    if st.session_state.get("_sesi_err"):
        st.warning("Login berhasil, tetapi sesi tidak dapat disimpan di Supabase (tabel admin_sessions): "
                   + st.session_state.pop("_sesi_err"))
    if st.session_state.pop("_toast_logout", False):
        st.toast(LA("logout.done"), icon="👋")

    # 4. HEADER: logo + nama web (kiri) dan tombol bahasa ID | EN (kanan)
    tampilkan_header()

# 5. Pembuatan Navbar Atas (Tabs) - label mengikuti bahasa aktif
tab_edukasi, tab_panduan, tab_medis = st.tabs(
    [t("tab.home"), t("tab.guide"), t("tab.medic")]
)

# --- TAB 1: EDUKASI ---
with tab_edukasi:
    tampilkan_edukasi()

# --- TAB 2: PANDUAN ---
with tab_panduan:
    tampilkan_panduan()

# --- TAB 3: AREA TENAGA MEDIS ---
with tab_medis:
    @st.fragment
    def render_area_medis():
        if not st.session_state.get("logged_in", False):
            tampilkan_login(login_user)
        else:
            role = st.session_state.get("role", "dokter")
            es_admin = role == "admin"

            col_info, col_logout = st.columns([4, 1])
            with col_info:
                nama = st.session_state.get("current_user", "") or "Admin"
                if role != "admin" and not nama.lower().startswith("dr"):
                    nama = f"Dr. {nama}"
                st.success(f"{t('app.connected')}: **{nama}** · {LA('role.' + (role if role in ('admin', 'dokter') else 'dokter'))}")
            with col_logout:
                if st.button(t("app.logout"), use_container_width=True, type="primary"):
                    buka_dialog_logout(logout_user)

            st.divider()

            if st.session_state.get("must_change_password"):
                tampilkan_ganti_password(wajib=True)
            else:
                labels = [LA("nav.patients"), LA("nav.account")] + ([LA("nav.staff")] if es_admin else [])
                sub = st.tabs(labels)
                with sub[0]:
                    tampilkan_manajemen_pasien()
                with sub[1]:
                    tampilkan_akun_saya()
                if es_admin:
                    with sub[2]:
                        tampilkan_kelola_staf()

    render_area_medis()

# 6. CHATBOT BUBBLE
tampilkan_chatbot_floating()

# 7. PENJAGA POSISI TAB
if st.session_state.get("logged_in", False):
    components.html(
        """
        <script>
            const tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"]');
            if (tabs.length >= 3 && sessionStorage.getItem("stay_in_medic") === "true") {
                tabs[2].click();
            }
            if (tabs.length >= 3) {
                tabs[0].onclick = () => sessionStorage.setItem("stay_in_medic", "false");
                tabs[1].onclick = () => sessionStorage.setItem("stay_in_medic", "false");
                tabs[2].onclick = () => sessionStorage.setItem("stay_in_medic", "true");
            }
        </script>
        """,
        height=0,
        width=0,
    )