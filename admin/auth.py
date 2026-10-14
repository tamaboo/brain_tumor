import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone

import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client, Client
from navbar.kamus_bahasa import t

# ------------------------------------------------------------------------------
# PENGATURAN SESI
# ------------------------------------------------------------------------------
SESSION_JAM = 8              # lama login diingat (jam), mis. satu shift kerja
COOKIE = "ns_session"        # nama cookie di browser
SESSION_TABLE = "admin_sessions"

# Menginisialisasi koneksi ke Supabase menggunakan kredensial dari secrets.toml
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# ==============================================================================
# HASH PASSWORD (PBKDF2-SHA256, library standar Python)
# ==============================================================================
_ITER = 200_000

def hash_password(pw: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), salt, _ITER)
    return f"pbkdf2${_ITER}${salt.hex()}${dk.hex()}"

def verify_password(pw: str, stored: str) -> bool:
    try:
        _, it, salt, h = stored.split("$")
        dk = hashlib.pbkdf2_hmac("sha256", pw.encode("utf-8"), bytes.fromhex(salt), int(it))
        return hmac.compare_digest(dk.hex(), h)
    except Exception:
        return False

def buat_password_sementara(n: int = 10) -> str:
    huruf = "ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789"   # tanpa karakter yang mirip (O/0, l/1)
    return "".join(secrets.choice(huruf) for _ in range(n))

def ubah_password_db(username: str, password_baru: str, wajib_ganti: bool = False):
    """Simpan password baru sebagai hash dan hapus password teks biasa (jika masih ada)."""
    supabase.table("admin_users").update({
        "password_hash": hash_password(password_baru),
        "password": "",
        "must_change_password": wajib_ganti,
    }).eq("username", username).execute()

def cek_password_user(user: dict, password: str) -> bool:
    """Cocokkan password dengan hash; akun lama tanpa hash dicocokkan dengan kolom password lama."""
    if user.get("password_hash"):
        return verify_password(password, user["password_hash"])
    plain = user.get("password") or ""
    return bool(plain) and hmac.compare_digest(plain.encode("utf-8"), password.encode("utf-8"))

# ==============================================================================
# SESI LOGIN YANG BERTAHAN SAAT REFRESH (cookie di browser + tabel admin_sessions)
# ==============================================================================
def _hash_token(tok: str) -> str:
    return hashlib.sha256(tok.encode("utf-8")).hexdigest()

def _terapkan_sesi(u: dict):
    username = u["username"]
    st.session_state["logged_in"] = True
    st.session_state["current_user"] = u.get("nama_lengkap") or username
    st.session_state["current_username"] = username
    st.session_state["role"] = (u.get("role") or "dokter").lower()
    st.session_state["must_change_password"] = bool(u.get("must_change_password"))

def buat_sesi(username: str):
    """Dipanggil setelah login berhasil: simpan token (hash-nya) di database, token asli dikirim ke cookie browser."""
    try:
        tok = secrets.token_urlsafe(32)
        sekarang = datetime.now(timezone.utc)
        supabase.table(SESSION_TABLE).delete().lt("expires_at", sekarang.isoformat()).execute()   # bersihkan yang kedaluwarsa
        supabase.table(SESSION_TABLE).insert({
            "token_hash": _hash_token(tok),
            "username": username,
            "expires_at": (sekarang + timedelta(hours=SESSION_JAM)).isoformat(),
        }).execute()
        st.session_state["_tok"] = tok
        st.session_state["_new_cookie"] = tok
    except Exception as e:
        st.session_state["_sesi_err"] = str(e)     # login tetap berhasil, hanya tidak bertahan saat refresh

def pulihkan_sesi():
    """Dipanggil di awal app.py: jika browser punya cookie sesi yang valid, login dipulihkan otomatis."""
    if st.session_state.get("logged_in"):
        return
    try:
        tok = st.context.cookies.get(COOKIE)
    except Exception:
        return                                     # Streamlit terlalu lama (butuh >= 1.37)
    if not tok:
        return
    try:
        r = supabase.table(SESSION_TABLE).select("*").eq("token_hash", _hash_token(tok)).limit(1).execute()
        if not r.data:
            return
        s = r.data[0]
        exp = datetime.fromisoformat(str(s["expires_at"]).replace("Z", "+00:00"))
        if exp < datetime.now(timezone.utc):
            supabase.table(SESSION_TABLE).delete().eq("token_hash", s["token_hash"]).execute()
            return
        ur = supabase.table("admin_users").select("*").eq("username", s["username"]).limit(1).execute()
        if not ur.data or ur.data[0].get("is_active") is False:
            return
        _terapkan_sesi(ur.data[0])
        st.session_state["_tok"] = tok
    except Exception:
        return

def sinkronkan_cookie():
    """Dipanggil di app.py setiap run: menulis atau menghapus cookie di browser bila diperlukan."""
    tok = st.session_state.pop("_new_cookie", None)
    if tok:
        detik = SESSION_JAM * 3600
        components.html(f"""<script>
        const p = window.parent, sec = p.location.protocol === 'https:' ? '; Secure' : '';
        p.document.cookie = "{COOKIE}={tok}; path=/; max-age={detik}; SameSite=Lax" + sec;
        </script>""", height=0)
    if st.session_state.pop("_clear_cookie", False):
        components.html(f"""<script>
        window.parent.document.cookie = "{COOKIE}=; path=/; max-age=0; SameSite=Lax";
        </script>""", height=0)

def hapus_sesi_user(username: str):
    """Putuskan semua sesi login milik satu akun (dipakai saat admin reset password / menonaktifkan akun)."""
    try:
        supabase.table(SESSION_TABLE).delete().eq("username", username).execute()
    except Exception:
        pass

# ==============================================================================
# LOGIN / LOGOUT
# ==============================================================================
def init_auth_state():
    defaults = {
        "logged_in": False,
        "current_user": "",        # nama lengkap
        "current_username": "",    # username (kunci akun)
        "role": "dokter",
        "must_change_password": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def login_user(username, password):
    try:
        resp = supabase.table("admin_users").select("*").eq("username", username).limit(1).execute()
        if not resp.data:
            return False
        u = resp.data[0]

        if u.get("is_active") is False:          # akun dinonaktifkan -> diperlakukan sebagai gagal login
            return False
        if not cek_password_user(u, password):
            return False

        # Akun lama (masih password teks biasa): otomatis ditingkatkan menjadi hash saat login berhasil
        if not u.get("password_hash"):
            try:
                ubah_password_db(username, password, wajib_ganti=bool(u.get("must_change_password")))
            except Exception:
                pass

        _terapkan_sesi(u)
        buat_sesi(username)

        try:
            supabase.table("admin_users").update(
                {"last_login": datetime.now(timezone.utc).isoformat()}
            ).eq("username", username).execute()
        except Exception:
            pass
        return True
    except Exception as e:
        st.error(t("auth.dberr", e=e))
        return False

def logout_user():
    tok = st.session_state.get("_tok")
    if not tok:
        try:
            tok = st.context.cookies.get(COOKIE)
        except Exception:
            tok = None
    if tok:
        try:
            supabase.table(SESSION_TABLE).delete().eq("token_hash", _hash_token(tok)).execute()
        except Exception:
            pass
    st.session_state["_clear_cookie"] = True
    st.session_state.pop("_tok", None)
    st.session_state["logged_in"] = False
    st.session_state["current_user"] = ""
    st.session_state["current_username"] = ""
    st.session_state["role"] = "dokter"
    st.session_state["must_change_password"] = False