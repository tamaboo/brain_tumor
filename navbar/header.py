import base64
from pathlib import Path
import streamlit as st
from navbar.kamus_bahasa import t, tombol_bahasa

# ---------------------------------------------------------------
# PENGATURAN BRAND (ubah di sini saja)
# ---------------------------------------------------------------
NAMA_DEPAN = "Neuro"                                  # bagian gelap
NAMA_BELAKANG = "Sight"                               # bagian biru
TAGLINE = "Diagnostik Tumor Otak Berbasis XAI"        # teks kecil huruf kapital di bawah nama
LOGO_PATH = ""        # kosong = dicari otomatis (file bernama *logo*). Contoh manual: "assets/logo.png"
LOGO_UKURAN = 96      # px (logo di header) - boleh dinaikkan lagi, mis. 110
TAMPILKAN_SPLASH = True   # layar pembuka saat web pertama kali dibuka
DURASI_SPLASH = 2.6       # detik sebelum splash memudar
LOGO_BIRU = False     # True = ubah logo hijau menjadi biru agar senada dengan tema

_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
         ".webp": "image/webp", ".svg": "image/svg+xml", ".gif": "image/gif"}


def _css():
    filt = "filter:hue-rotate(78deg) saturate(1.25);" if LOGO_BIRU else ""
    return f"""
<style>
/* rapatkan halaman ke pojok kiri-atas */
.block-container,[data-testid="stMainBlockContainer"]{{padding-top:1rem!important;padding-left:2.2rem!important;padding-right:2.2rem!important}}
.brand{{display:flex;align-items:center;gap:1rem;margin:0 0 .9rem;padding:0;background:none;border:none;box-shadow:none}}
.brand img{{width:{LOGO_UKURAN}px;height:{LOGO_UKURAN}px;object-fit:contain;background:transparent;{filt}}}
.brand .nm{{font:800 2rem/1 'Plus Jakarta Sans',system-ui,sans-serif;color:#0B1B3A;letter-spacing:-.025em}}
.brand .nm span{{color:#2F6BFF}}
.brand .tg{{margin-top:.45rem;font:600 .7rem/1 'Plus Jakarta Sans',system-ui,sans-serif;letter-spacing:.16em;
  text-transform:uppercase;color:#5E6C84}}
.st-key-lang_wrap{{display:flex;justify-content:flex-end}}
@media(max-width:640px){{.brand .nm{{font-size:1.5rem}}.brand .tg{{font-size:.58rem;letter-spacing:.1em}}}}
</style>
"""


def _cari_logo():
    root = Path(__file__).resolve().parent.parent          # folder project (naik dari navbar/)
    if LOGO_PATH:
        p = Path(LOGO_PATH)
        return p if p.is_absolute() else root / p
    for folder in [root, root / "assets", root / "images", root / "img", root / "static", root / "navbar"]:
        if folder.is_dir():
            for f in sorted(folder.iterdir()):
                if f.is_file() and f.suffix.lower() in _MIME and "logo" in f.stem.lower():
                    return f
    return None


@st.cache_data(show_spinner=False)
def _logo_uri(path_str: str):
    """Baca logo -> data URI. Area kosong/transparan di sekeliling gambar dipotong otomatis
    supaya logo terlihat besar saat ukurannya dinaikkan."""
    p = Path(path_str)
    mime = _MIME.get(p.suffix.lower(), "image/png")
    raw = p.read_bytes()
    if p.suffix.lower() != ".svg":
        try:
            import io
            from PIL import Image, ImageChops
            im = Image.open(io.BytesIO(raw)).convert("RGBA")
            bbox = im.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox()
            if bbox is None or bbox == (0, 0, *im.size):          # tak ada transparansi -> buang tepi putih
                diff = ImageChops.difference(im.convert("RGB"), Image.new("RGB", im.size, (255, 255, 255)))
                bbox = diff.convert("L").point(lambda v: 255 if v > 12 else 0).getbbox()
            if bbox:
                im = im.crop(bbox)
            buf = io.BytesIO()
            im.save(buf, "PNG")
            raw, mime = buf.getvalue(), "image/png"
        except Exception:
            pass                                                   # PIL tidak ada -> pakai gambar asli
    return f"data:{mime};base64,{base64.b64encode(raw).decode()}"


def tampilkan_header():
    """Logo + nama brand di kiri atas dan tombol bahasa ID | EN di kanan atas. Panggil sekali sebelum st.tabs()."""
    logo = _cari_logo()
    img = f'<img src="{_logo_uri(str(logo))}" alt="logo">' if logo and logo.exists() else ""
    tag = t("brand.tagline")
    kiri, kanan = st.columns([4, 1], vertical_alignment="center")
    with kiri:
        st.markdown(
            _css() + f'<div class="brand">{img}<div><div class="nm">{NAMA_DEPAN}<span>{NAMA_BELAKANG}</span></div>'
                     f'<div class="tg">{tag}</div></div></div>',
            unsafe_allow_html=True,
        )
    with kanan:
        tombol_bahasa()


# ---------------------------------------------------------------
# SPLASH SCREEN
# ---------------------------------------------------------------
_SPLASH_CSS = """
<style>
.sp{position:fixed;inset:0;z-index:2147483000;display:flex;flex-direction:column;align-items:center;justify-content:center;
  background:radial-gradient(circle at 18% 14%,#D9E5FF 0,transparent 46%),radial-gradient(circle at 86% 92%,#C6D8FF 0,transparent 46%),#F6F9FF;
  animation:sp-out .7s ease __D__s forwards}
.sp::before{content:"";position:absolute;right:-130px;top:-130px;width:390px;height:390px;border-radius:50%;border:46px solid rgba(47,107,255,.07)}
.sp::after{content:"";position:absolute;left:-70px;bottom:-70px;width:230px;height:230px;border-radius:62px;background:rgba(47,107,255,.07);transform:rotate(18deg)}
.sp img{position:relative;width:130px;height:130px;object-fit:contain;animation:sp-pop .9s cubic-bezier(.2,.8,.2,1) both}
.sp .nm{position:relative;margin-top:1.3rem;font:800 2.5rem/1 'Plus Jakarta Sans',system-ui,sans-serif;color:#0B1B3A;
  letter-spacing:-.025em;animation:sp-up .8s .2s both}
.sp .nm span{color:#2F6BFF}
.sp .tg{position:relative;margin-top:.7rem;font:600 .72rem/1 'Plus Jakarta Sans',system-ui,sans-serif;letter-spacing:.2em;
  text-transform:uppercase;color:#5E6C84;animation:sp-up .8s .35s both}
.sp .bar{position:relative;width:min(260px,60vw);height:4px;border-radius:99px;background:#DCE5FA;margin-top:2.3rem;overflow:hidden;
  animation:sp-up .6s .5s both}
.sp .bar i{display:block;height:100%;width:0;border-radius:99px;background:#2F6BFF;animation:sp-fill __B__s .5s cubic-bezier(.4,0,.2,1) forwards}
.sp .ld{position:relative;margin-top:.8rem;font:500 .78rem system-ui,sans-serif;color:#5E6C84;animation:sp-up .6s .6s both}
@keyframes sp-pop{from{opacity:0;transform:scale(.7)}to{opacity:1;transform:scale(1)}}
@keyframes sp-up{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
@keyframes sp-fill{to{width:100%}}
@keyframes sp-out{to{opacity:0;visibility:hidden}}
@media (prefers-reduced-motion:reduce){.sp,.sp *{animation-duration:.01s!important}}
</style>
"""


def tampilkan_splash():
    """Layar pembuka (logo + nama + progress bar). Tampil sekali per sesi lalu memudar otomatis.
    Panggil di app.py setelah st.set_page_config()."""
    if not TAMPILKAN_SPLASH or st.session_state.get("_splash_done"):
        return
    st.session_state["_splash_done"] = True
    logo = _cari_logo()
    img = f'<img src="{_logo_uri(str(logo))}" alt="logo">' if logo and logo.exists() else ""
    css = _SPLASH_CSS.replace("__D__", str(DURASI_SPLASH)).replace("__B__", str(max(DURASI_SPLASH - 0.6, 0.8)))
    tag, ld = t("brand.tagline"), t("splash.loading")
    st.markdown(
        css + f'<div class="sp">{img}<div class="nm">{NAMA_DEPAN}<span>{NAMA_BELAKANG}</span></div>'
              f'<div class="tg">{tag}</div><div class="bar"><i></i></div><div class="ld">{ld}</div></div>',
        unsafe_allow_html=True,
    )