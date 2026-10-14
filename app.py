import streamlit as st
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

# 2. Injeksi CSS untuk memblokir Sidebar dan memperindah Tab
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
    </style>
""", unsafe_allow_html=True)

# 2b. SPLASH SCREEN (tampil sekali per sesi, memudar otomatis)
tampilkan_splash()

# 3. Inisialisasi State Login + pulihkan login dari cookie (supaya tidak logout saat refresh)
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
    if not st.session_state.get("logged_in", False):
        tampilkan_login(login_user)
    else:
        role = st.session_state.get("role", "dokter")
        es_admin = role == "admin"

        col_info, col_logout = st.columns([4, 1])
        with col_info:
            nama = st.session_state.get("current_user", "") or "Admin"
            # tambah awalan "Dr." hanya untuk dokter dan hanya jika belum ada di nama
            if role != "admin" and not nama.lower().startswith("dr"):
                nama = f"Dr. {nama}"
            st.success(f"{t('app.connected')}: **{nama}** · {LA('role.' + (role if role in ('admin', 'dokter') else 'dokter'))}")
        with col_logout:
            if st.button(t("app.logout"), use_container_width=True, type="primary"):
                buka_dialog_logout(logout_user)          # popup konfirmasi dulu

        st.divider()

        if st.session_state.get("must_change_password"):
            # Setelah reset oleh admin: wajib ganti password sebelum memakai dashboard
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

# 6. CHATBOT BUBBLE (pojok kanan bawah), dipanggil sekali di luar semua tab
tampilkan_chatbot_floating()