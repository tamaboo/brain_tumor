import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import quote
from groq import Groq
from navbar.kamus_bahasa import t

# Groq sering mengganti/menghentikan model. Daftar ini dicoba berurutan:
# jika model pertama tidak tersedia (404), otomatis pindah ke berikutnya.
# Cek daftar terbaru: https://console.groq.com/docs/models
MODELS = [
    "openai/gpt-oss-120b",
    "qwen/qwen3.6-27b",
    "openai/gpt-oss-20b",
]

SYSTEM_PROMPT = """Kamu adalah asisten edukasi pada website deteksi tumor otak berbasis AI (XAI).
Aturan:
- Jawab dalam Bahasa Indonesia yang jelas dan ramah, singkat (maks. sekitar 150 kata) kecuali diminta detail.
- JANGAN memakai tabel. Gunakan paragraf pendek atau daftar poin singkat (jendela chat sempit).
- Topik utama: tumor otak (Glioma, Meningioma, Pituitary), MRI, cara kerja EfficientNetB2, Grad-CAM/heatmap, dan cara memakai website ini.
- Kamu BUKAN dokter. Jangan mendiagnosis atau meresepkan obat. Untuk keluhan pribadi, sarankan konsultasi ke dokter/ahli saraf.
- Jika pertanyaan di luar topik kesehatan otak atau website ini, tolak dengan sopan dan arahkan kembali.
- Jika tidak yakin, katakan tidak yakin; jangan mengarang fakta medis."""

# Ikon robot dokter (putih) + lencana palang medis merah
ROBOT_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'>"
    "<line x1='16' y1='4' x2='16' y2='8' stroke='white' stroke-width='2' stroke-linecap='round'/>"
    "<circle cx='16' cy='3.5' r='2' fill='white'/>"
    "<rect x='2' y='13' width='3' height='6' rx='1.5' fill='white'/>"
    "<rect x='27' y='13' width='3' height='6' rx='1.5' fill='white'/>"
    "<rect x='5' y='8' width='22' height='17' rx='6' fill='white'/>"
    "<circle cx='12' cy='15' r='2.4' fill='#2F6BFF'/><circle cx='20' cy='15' r='2.4' fill='#2F6BFF'/>"
    "<path d='M12 20.5q4 3 8 0' stroke='#2F6BFF' stroke-width='1.8' fill='none' stroke-linecap='round'/>"
    "<circle cx='25' cy='25' r='6' fill='#ff4d4d' stroke='white' stroke-width='1.5'/>"
    "<path d='M25 22v6M22 25h6' stroke='white' stroke-width='2' stroke-linecap='round'/>"
    "</svg>"
)
ICON_URI = "data:image/svg+xml;utf8," + quote(ROBOT_SVG)

CSS = """
<style>
/* ---- tombol chat (pojok kanan bawah): ikon robot dokter + teks ---- */
.st-key-chat_fab{position:fixed!important;bottom:24px;right:24px;z-index:999990;width:auto!important}
.st-key-chat_fab button{
  display:flex;align-items:center;gap:10px;height:58px;min-height:58px;padding:0 22px 0 14px;
  border-radius:999px;border:none;background:#2F6BFF;
  box-shadow:0 4px 14px rgba(15,108,189,.35);transition:transform .2s,background .2s}
.st-key-chat_fab button::before{content:"";flex:none;width:36px;height:36px;
  background:url("__ICON__") center/contain no-repeat}
.st-key-chat_fab button p{margin:0;color:#fff;font-weight:700;font-size:.95rem;white-space:nowrap}
.st-key-chat_fab button:hover{transform:translateY(-2px);background:#1F4FD6;border:none}
.st-key-chat_fab button [data-testid="stIconMaterial"]{display:none}
@keyframes fabpulse{0%{box-shadow:0 0 0 0 rgba(60,200,230,.55)}70%{box-shadow:0 0 0 16px rgba(60,200,230,0)}100%{box-shadow:0 0 0 0 rgba(60,200,230,0)}}
@media (max-width:640px){.st-key-chat_fab button{padding:0 11px}.st-key-chat_fab button p{display:none}}
/* ---- jendela chat ---- */
div[data-testid="stPopoverBody"]:has(.st-key-chat_panel){
  width:min(400px,92vw)!important;max-height:84vh;border-radius:14px;padding:0!important;
  border:1px solid #DCE5FA;box-shadow:0 12px 32px rgba(20,40,60,.18)}
.st-key-chat_panel{padding:0 .9rem .8rem}
.chat-head{display:flex;align-items:center;gap:.7rem;margin:0 -.9rem .6rem;padding:.8rem 1rem;
  background:#2F6BFF;border-radius:14px 14px 0 0;color:#fff}
.chat-head b{font-size:1rem;display:block;line-height:1.2}
.chat-head small{opacity:.9;font-size:.78rem}
.chat-head .dot{width:9px;height:9px;border-radius:50%;background:#2ee66b;display:inline-block;margin-right:5px}
.chat-head .av{flex:none;width:2.6rem;height:2.6rem;border-radius:50%;background:rgba(255,255,255,.3) url("__ICON__") center/70% no-repeat}
.chat-x{margin-left:auto;flex:none;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;
  justify-content:center;background:rgba(255,255,255,.35);cursor:pointer;font-weight:800;font-size:1rem;
  color:#fff;user-select:none;transition:.2s}
.chat-x:hover{background:rgba(255,255,255,.55)}
.st-key-chat_panel [data-testid="stForm"]{border:none;padding:0}
.st-key-chat_panel .stButton button{font-size:.8rem;padding:.25rem .5rem;min-height:2rem}
/* ---- indikator "sedang berpikir" ---- */
.think{display:flex;align-items:center;gap:.45rem;color:#5B6B7B;font-size:.9rem;padding:.2rem 0}
.think i{width:7px;height:7px;border-radius:50%;background:#2F6BFF;display:inline-block;animation:tb 1.2s infinite ease-in-out}
.think i:nth-child(3){animation-delay:.15s}.think i:nth-child(4){animation-delay:.3s}
@keyframes tb{0%,80%,100%{transform:scale(.5);opacity:.35}40%{transform:scale(1);opacity:1}}
</style>
""".replace("__ICON__", ICON_URI)

def _header():
    return (
        '<div class="chat-head"><div class="av"></div>'
        f'<div><b>{t("chat.title")}</b><small><span class="dot"></span>{t("chat.status")}</small></div>'
        f'<div class="chat-x" title="{t("chat.close")}">✕</div></div>'
    )


def _think():
    return f'<div class="think"><span>{t("chat.think")}</span><i></i><i></i><i></i></div>'


def _pertanyaan():
    return [t(f"chat.q{i}") for i in range(1, 5)]


@st.cache_resource
def _client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])


def _stream(messages):
    last_err = None
    for model in MODELS:
        try:
            stream = _client().chat.completions.create(
                model=model, messages=messages, temperature=0.4, max_tokens=1200, stream=True,
            )
        except Exception as e:
            msg = str(e).lower()
            if "404" in msg or "model_not_found" in msg or "decommission" in msg:
                last_err = e
                continue  # coba model berikutnya
            raise
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
        return
    raise last_err or RuntimeError("Tidak ada model Groq yang tersedia.")


def _jawab(pesan):
    """Tampilkan animasi 'berpikir' sampai token pertama tiba, lalu stream jawabannya."""
    ph = st.empty()
    ph.markdown(_think(), unsafe_allow_html=True)
    teks = ""
    try:
        for tok in _stream(pesan):
            teks += tok
            ph.markdown(teks + "▌")
        if not teks.strip():
            teks = t("chat.empty")
        ph.markdown(teks)
        return teks
    except KeyError:
        out = t("chat.err.key")
    except Exception as e:
        msg = str(e).lower()
        if "429" in msg or "rate" in msg:
            out = t("chat.err.rate")
        elif "401" in msg or "invalid api key" in msg:
            out = t("chat.err.auth")
        else:
            out = t("chat.err.generic", e=e)
    ph.error(out)
    return out


def _pilih(q):
    st.session_state.pending_q = q


def _tombol_tutup():
    """Membuat ikon ✕ di header menutup jendela chat (popover Streamlit tidak punya API tutup)."""
    components.html("""
    <script>
    const p = window.parent, d = p.document;
    if (p.__chatXh) d.removeEventListener('click', p.__chatXh, true);
    p.__chatXh = function (e) {
      if (!e.target.closest || !e.target.closest('.chat-x')) return;
      d.dispatchEvent(new p.KeyboardEvent('keydown', {key:'Escape', code:'Escape', keyCode:27, which:27, bubbles:true}));
      setTimeout(() => {                       // jika Esc tidak menutup, klik tombol pembuka (toggle)
        if (d.querySelector('.st-key-chat_panel')) {
          const b = d.querySelector('.st-key-chat_fab button'); if (b) b.click();
        }
      }, 250);
    };
    d.addEventListener('click', p.__chatXh, true);
    </script>""", height=0)


def tampilkan_chatbot_floating():
    """Panggil SEKALI di app.py (di luar tabs). Muncul sebagai tombol di pojok kanan bawah."""
    st.markdown(CSS, unsafe_allow_html=True)

    if "chat_msgs" not in st.session_state:
        st.session_state.chat_msgs = [{"role": "assistant", "content": t("chat.greet")}]
    msgs = st.session_state.chat_msgs
    if len(msgs) == 1:                       # salam mengikuti bahasa aktif
        msgs[0]["content"] = t("chat.greet")
    pending = st.session_state.pop("pending_q", None)

    with st.container(key="chat_fab"):
        with st.popover(t("chat.fab")):
            with st.container(key="chat_panel"):
                st.markdown(_header(), unsafe_allow_html=True)

                box = st.container(height=330, border=False)   # area pesan (scroll)

                if len(msgs) == 1 and not pending:              # saran pertanyaan di awal
                    cols = st.columns(2)
                    for i, q in enumerate(_pertanyaan()):
                        cols[i % 2].button(q, key=f"qk{i}", use_container_width=True,
                                           on_click=_pilih, args=(q,))

                with st.form("chat_form", clear_on_submit=True):
                    c1, c2 = st.columns([5, 1], vertical_alignment="bottom")
                    teks = c1.text_input(t("chat.msg"), placeholder=t("chat.placeholder"),
                                         label_visibility="collapsed")
                    kirim = c2.form_submit_button("➤", use_container_width=True)
                if kirim and teks.strip():
                    pending = teks.strip()

                if len(msgs) > 1 and st.button(t("chat.clear"), key="chat_clear"):
                    st.session_state.chat_msgs = [{"role": "assistant", "content": t("chat.greet")}]
                    st.rerun()

                with box:
                    for m in msgs:
                        with st.chat_message(m["role"], avatar="🤖" if m["role"] == "assistant" else "🧑"):
                            st.markdown(m["content"])
                    if pending:
                        msgs.append({"role": "user", "content": pending})
                        with st.chat_message("user", avatar="🧑"):
                            st.markdown(pending)
                        konteks = [{"role": "system", "content": SYSTEM_PROMPT + t("chat.lang_directive")}] + msgs[-10:]
                        with st.chat_message("assistant", avatar="🤖"):
                            jawaban = _jawab(konteks)
                        msgs.append({"role": "assistant", "content": jawaban})

    _tombol_tutup()


# Alias lama agar import lama tidak error
tampilkan_chatbot = tampilkan_chatbot_floating