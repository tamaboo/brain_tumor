import streamlit as st
from navbar.kamus_bahasa import t, get_lang
from navbar.header import _cari_logo, _logo_uri, NAMA_DEPAN, NAMA_BELAKANG

TXT = {
    "id": {
        "login.eyebrow": "Portal Tenaga Medis",
        "login.heading": "Masuk ke akun Anda",
        "login.ph.user": "Masukkan username",
        "login.ph.pass": "Masukkan password",
        "login.empty": "Harap isi username dan password.",
        "login.checking": "Memeriksa kredensial...",
        "login.welcome": "Prosedur Tenaga Medis",
        "login.lead": "Ikuti alur berikut untuk memeriksa citra MRI pasien dan mencatat hasilnya.",
        "login.b1": "Masuk dengan akun yang didaftarkan oleh administrator.",
        "login.b2": "Unggah citra MRI pasien (JPG atau PNG).",
        "login.b3": "Tinjau hasil AI dan heatmap Grad-CAM sebagai second opinion.",
        "login.b4": "Lengkapi data pasien, lalu simpan ke database rekam medis.",
        "login.note": "Hasil AI hanyalah alat bantu. Keputusan klinis tetap berada pada dokter.",
    },
    "en": {
        "login.eyebrow": "Medical Staff Portal",
        "login.heading": "Sign in to your account",
        "login.ph.user": "Enter your username",
        "login.ph.pass": "Enter your password",
        "login.empty": "Please enter your username and password.",
        "login.checking": "Verifying credentials...",
        "login.welcome": "Medical Staff Procedure",
        "login.lead": "Follow this workflow to review a patient's MRI image and record the result.",
        "login.b1": "Sign in with the account registered by the administrator.",
        "login.b2": "Upload the patient's MRI image (JPG or PNG).",
        "login.b3": "Review the AI result and Grad-CAM heatmap as a second opinion.",
        "login.b4": "Complete the patient data, then save it to the medical records database.",
        "login.note": "AI results are a support tool only. Clinical decisions remain with the physician.",
    },
}


def L(key):
    """Teks login: pakai kamus lokal di atas; jika tidak ada, ambil dari kamus_bahasa (mis. login.user, login.btn)."""
    return TXT.get(get_lang(), {}).get(key) or TXT["id"].get(key) or t(key)


FX = "'Plus Jakarta Sans',system-ui,sans-serif"

CSS = """
<style>
/* ---------- kartu login ---------- */
.st-key-login_card{max-width:1000px;margin:1.2rem auto 2rem;background:#fff;border:1px solid #DCE5FA;border-radius:28px;
  overflow:hidden;box-shadow:0 30px 70px -32px rgba(47,107,255,.55)}
.st-key-login_card [data-testid="stHorizontalBlock"]{gap:0!important}
/* ---------- panel biru (kiri) ---------- */
.st-key-login_left{position:relative;overflow:hidden;min-height:580px;padding:2.4rem 2.2rem;color:#fff;
  background:linear-gradient(150deg,#2F6BFF 0%,#1F4FD6 100%)}
.st-key-login_left::before{content:"";position:absolute;right:-90px;top:-90px;width:300px;height:300px;border-radius:50%;
  border:40px solid rgba(255,255,255,.08)}
.st-key-login_left::after{content:"";position:absolute;left:-44px;bottom:-44px;width:180px;height:180px;border-radius:46px;
  background:rgba(255,255,255,.09);transform:rotate(18deg)}
.lg-brand{position:relative;display:flex;align-items:center;gap:.8rem}
.lg-brand .tile{width:60px;height:60px;border-radius:18px;background:#fff;display:flex;align-items:center;justify-content:center;
  box-shadow:0 12px 26px -12px rgba(0,0,0,.45)}
.lg-brand img{width:42px;height:42px;object-fit:contain}
.lg-brand .nm{font:800 1.5rem/1 __FX__;color:#fff;letter-spacing:-.02em}
.lg-h{position:relative;font:800 2rem/1.15 __FX__;margin:2.8rem 0 .9rem;color:#fff;letter-spacing:-.02em}
.lg-p{position:relative;color:rgba(255,255,255,.88);line-height:1.7;max-width:22rem;margin:0;font-size:.98rem}
.lg-list{position:relative;list-style:none;margin:1.9rem 0 0;padding:0}
.lg-list li{display:flex;gap:.8rem;align-items:flex-start;margin-bottom:1rem;font-weight:500;font-size:.93rem;line-height:1.5;color:#fff}
.lg-list i{flex:none;width:26px;height:26px;border-radius:50%;background:rgba(255,255,255,.2);display:flex;
  align-items:center;justify-content:center;font-style:normal;font-weight:700;font-size:.8rem;margin-top:.05rem}
.lg-note{position:relative;margin-top:1.8rem;padding:.9rem 1.1rem;border-radius:14px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);font-size:.84rem;line-height:1.55;color:#fff}
/* ---------- form (kanan) ---------- */
.st-key-login_right{min-height:580px;padding:2.6rem 2.5rem;display:flex;flex-direction:column;justify-content:center}
.lg-ic{width:54px;height:54px;border-radius:17px;background:#EAF0FF;display:flex;align-items:center;justify-content:center;margin-bottom:1.1rem}
.lg-ic svg{width:26px;height:26px;stroke:#2F6BFF;fill:none;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}
.lg-pill{display:inline-flex;align-items:center;gap:.5rem;padding:.3rem .85rem;border-radius:999px;background:#EAF0FF;color:#1F4FD6;
  font-size:.74rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.8rem}
.lg-pill::before{content:"";width:7px;height:7px;border-radius:50%;background:#2F6BFF}
.lg-title{font:800 1.8rem/1.15 __FX__;color:#0B1B3A;letter-spacing:-.02em;margin:0 0 .45rem}
.lg-sub{color:#5E6C84;line-height:1.65;margin:0 0 1.4rem;font-size:.95rem}
.st-key-login_right [data-testid="stForm"]{border:none;padding:0}
.st-key-login_right [data-testid="stTextInput"] label p{font-weight:600;color:#0B1B3A;font-size:.88rem}
.st-key-login_right div[data-baseweb="input"]{border-radius:12px;border:1px solid #DCE5FA;background:#F6F9FF;transition:.15s}
.st-key-login_right div[data-baseweb="input"]:focus-within{border-color:#2F6BFF!important;background:#fff;box-shadow:0 0 0 3px rgba(47,107,255,.15)}
.st-key-login_right div[data-baseweb="input"] input{padding:.8rem .9rem}
.st-key-login_right button[kind="primaryFormSubmit"],.st-key-login_right button[kind="primary"]{
  height:3.1rem;border-radius:12px;font-weight:700;background:#2F6BFF;border:none;box-shadow:0 12px 24px -14px rgba(47,107,255,.9)}
.st-key-login_right button[kind="primaryFormSubmit"]:hover{background:#1F4FD6;border:none}
@media(max-width:760px){.st-key-login_left{display:none}.st-key-login_right{padding:2rem 1.4rem;min-height:0}}
</style>
""".replace("__FX__", FX)

IC_LOCK = '<rect x="4" y="11" width="16" height="10" rx="2.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>'


def _h(s: str) -> str:
    return " ".join(line.strip() for line in s.strip().splitlines())


def tampilkan_login(login_fn):
    """Halaman login. `login_fn(username, password)` -> True jika berhasil (mis. admin.auth.login_user)."""
    st.markdown(_h(CSS), unsafe_allow_html=True)

    logo = _cari_logo()
    img = f'<img src="{_logo_uri(str(logo))}" alt="logo">' if logo and logo.exists() else "🧠"

    with st.container(key="login_card"):
        kiri, kanan = st.columns([1, 1.05], gap="small")

        # ---------------- panel biru ----------------
        with kiri:
            with st.container(key="login_left"):
                st.markdown(_h(f"""
                <div class="lg-brand"><div class="tile">{img}</div><div class="nm">{NAMA_DEPAN}{NAMA_BELAKANG}</div></div>
                <div class="lg-h">{L("login.welcome")}</div>
                <p class="lg-p">{L("login.lead")}</p>
                <ul class="lg-list">
                  <li><i>1</i><span>{L("login.b1")}</span></li>
                  <li><i>2</i><span>{L("login.b2")}</span></li>
                  <li><i>3</i><span>{L("login.b3")}</span></li>
                  <li><i>4</i><span>{L("login.b4")}</span></li>
                </ul>
                <div class="lg-note">{L("login.note")}</div>"""), unsafe_allow_html=True)

        # ---------------- form ----------------
        with kanan:
            with st.container(key="login_right"):
                st.markdown(_h(f"""
                <div class="lg-ic"><svg viewBox="0 0 24 24">{IC_LOCK}</svg></div>
                <div class="lg-pill">{L("login.eyebrow")}</div>
                <div class="lg-title">{L("login.heading")}</div>
                <p class="lg-sub">{L("login.sub")}</p>"""), unsafe_allow_html=True)

                with st.form("login_form", clear_on_submit=False):
                    user = st.text_input(L("login.user"), key="login_user_in", placeholder=L("login.ph.user"))
                    pwd = st.text_input(L("login.pass"), type="password", key="login_pass_in", placeholder=L("login.ph.pass"))
                    kirim = st.form_submit_button(L("login.btn"), type="primary", use_container_width=True)

                if kirim:
                    if not user.strip() or not pwd:
                        st.warning(L("login.empty"))
                    else:
                        with st.spinner(L("login.checking")):
                            ok = login_fn(user, pwd)
                        if ok:
                            st.rerun()
                        else:
                            st.error(L("login.fail"))