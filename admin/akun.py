import streamlit as st
import pandas as pd
from admin.auth import (supabase, cek_password_user, ubah_password_db, hash_password,
                        buat_password_sementara, hapus_sesi_user)
from navbar.kamus_bahasa import get_lang

# ------------------------------------------------------------------------------
# Teks (ID/EN) disimpan di file ini agar tidak bergantung pada versi kamus_bahasa.py
# ------------------------------------------------------------------------------
TXT = {
    "id": {
        "nav.patients": "Pasien & MRI", "nav.account": "Akun Saya", "nav.staff": "Kelola Staf",
        "role.admin": "Administrator", "role.dokter": "Dokter",
        "acc.title": "Akun Saya", "acc.profile": "Profil",
        "acc.username": "Username", "acc.role": "Peran", "acc.name": "Nama lengkap",
        "acc.spec": "Spesialisasi", "acc.str": "No. STR (opsional)",
        "acc.save": "Simpan profil", "acc.saved": "Profil berhasil diperbarui.",
        "pw.title": "Ubah password", "pw.rule": "Minimal 8 karakter dan berbeda dari password lama.",
        "pw.current": "Password saat ini", "pw.new": "Password baru", "pw.confirm": "Konfirmasi password baru",
        "pw.btn": "Ubah password", "pw.wrong": "Password saat ini salah.",
        "pw.short": "Password baru minimal 8 karakter.", "pw.mismatch": "Konfirmasi password tidak cocok.",
        "pw.same": "Password baru harus berbeda dari password lama.", "pw.ok": "Password berhasil diubah.",
        "pw.force": "Demi keamanan, ganti password sementara Anda sebelum melanjutkan.",
        "stf.title": "Kelola Staf Medis", "stf.only": "Halaman ini khusus administrator.",
        "stf.list": "Daftar staf", "stf.add": "Tambah staf baru",
        "stf.username": "Username", "stf.name": "Nama lengkap", "stf.role": "Peran",
        "stf.temp": "Password sementara", "stf.create": "Buat akun",
        "stf.fill": "Username, nama lengkap, dan password sementara wajib diisi.",
        "stf.exists": "Username sudah dipakai.",
        "stf.created": "Akun {u} dibuat. Staf wajib mengganti password saat login pertama.",
        "stf.edit": "Ubah atau nonaktifkan staf", "stf.pick": "Pilih staf",
        "stf.active": "Akun aktif", "stf.save": "Simpan perubahan", "stf.saved": "Perubahan disimpan.",
        "stf.reset": "Reset password", "stf.resetok": "Password sementara untuk {u}:",
        "stf.once": "Catat sekarang; password ini hanya ditampilkan sekali.",
        "stf.self": "Anda tidak dapat mengubah peran atau menonaktifkan akun Anda sendiri di sini.",
        "stf.err": "Terjadi kesalahan: {e}",
        "logout.title": "Konfirmasi Keluar",
        "logout.q": "Apakah Anda yakin ingin keluar?",
        "logout.note": "Pastikan data pasien dan hasil pemindaian sudah disimpan. Data yang belum disimpan akan hilang.",
        "logout.yes": "Ya, keluar", "logout.no": "Batal",
        "logout.done": "Anda telah keluar dari akun.",
    },
    "en": {
        "nav.patients": "Patients & MRI", "nav.account": "My Account", "nav.staff": "Manage Staff",
        "role.admin": "Administrator", "role.dokter": "Physician",
        "acc.title": "My Account", "acc.profile": "Profile",
        "acc.username": "Username", "acc.role": "Role", "acc.name": "Full name",
        "acc.spec": "Specialization", "acc.str": "License no. (optional)",
        "acc.save": "Save profile", "acc.saved": "Profile updated.",
        "pw.title": "Change password", "pw.rule": "At least 8 characters and different from the old password.",
        "pw.current": "Current password", "pw.new": "New password", "pw.confirm": "Confirm new password",
        "pw.btn": "Change password", "pw.wrong": "Current password is incorrect.",
        "pw.short": "New password must be at least 8 characters.", "pw.mismatch": "Password confirmation does not match.",
        "pw.same": "New password must be different from the old one.", "pw.ok": "Password changed.",
        "pw.force": "For security, replace your temporary password before continuing.",
        "stf.title": "Manage Medical Staff", "stf.only": "This page is for administrators only.",
        "stf.list": "Staff list", "stf.add": "Add new staff",
        "stf.username": "Username", "stf.name": "Full name", "stf.role": "Role",
        "stf.temp": "Temporary password", "stf.create": "Create account",
        "stf.fill": "Username, full name and temporary password are required.",
        "stf.exists": "That username is already taken.",
        "stf.created": "Account {u} created. The staff member must change the password at first login.",
        "stf.edit": "Edit or deactivate staff", "stf.pick": "Select staff",
        "stf.active": "Account active", "stf.save": "Save changes", "stf.saved": "Changes saved.",
        "stf.reset": "Reset password", "stf.resetok": "Temporary password for {u}:",
        "stf.once": "Note it down now; this password is shown only once.",
        "stf.self": "You can't change your own role or deactivate your own account here.",
        "stf.err": "An error occurred: {e}",
        "logout.title": "Confirm Logout",
        "logout.q": "Are you sure you want to log out?",
        "logout.note": "Make sure patient data and scan results are saved. Unsaved data will be lost.",
        "logout.yes": "Yes, log out", "logout.no": "Cancel",
        "logout.done": "You have been logged out.",
    },
}


def L(key, **kw):
    s = TXT.get(get_lang(), {}).get(key) or TXT["id"].get(key, key)
    return s.format(**kw) if kw else s


def _me() -> dict:
    r = supabase.table("admin_users").select("*").eq("username", st.session_state.get("current_username", "")).limit(1).execute()
    return r.data[0] if r.data else {}


# ==============================================================================
# GANTI PASSWORD (dipakai di "Akun Saya" dan sebagai layar wajib setelah reset)
# ==============================================================================
def tampilkan_ganti_password(wajib: bool = False):
    if wajib:
        st.warning(L("pw.force"))
    st.markdown(f"#### {L('pw.title')}")
    st.caption(L("pw.rule"))
    with st.form("form_ganti_pw", clear_on_submit=True):
        lama = st.text_input(L("pw.current"), type="password")
        baru = st.text_input(L("pw.new"), type="password")
        ulang = st.text_input(L("pw.confirm"), type="password")
        kirim = st.form_submit_button(L("pw.btn"), type="primary")
    if not kirim:
        return
    try:
        user = _me()
        if not user or not cek_password_user(user, lama):
            st.error(L("pw.wrong"))
        elif len(baru) < 8:
            st.error(L("pw.short"))
        elif baru != ulang:
            st.error(L("pw.mismatch"))
        elif baru == lama:
            st.error(L("pw.same"))
        else:
            ubah_password_db(st.session_state["current_username"], baru, wajib_ganti=False)
            st.session_state["must_change_password"] = False
            st.success(L("pw.ok"))
            if wajib:
                st.rerun()
    except Exception as e:
        st.error(L("stf.err", e=e))


# ==============================================================================
# AKUN SAYA (semua staf)
# ==============================================================================
def tampilkan_akun_saya():
    st.markdown(f"### {L('acc.title')}")
    try:
        u = _me()
    except Exception as e:
        st.error(L("stf.err", e=e)); return
    role = (u.get("role") or "dokter").lower()

    st.markdown(f"#### {L('acc.profile')}")
    c1, c2 = st.columns(2)
    c1.text_input(L("acc.username"), value=u.get("username", ""), disabled=True)
    c2.text_input(L("acc.role"), value=L(f"role.{role}"), disabled=True)

    with st.form("form_profil"):
        nama = st.text_input(L("acc.name"), value=u.get("nama_lengkap") or "")
        a, b = st.columns(2)
        spes = a.text_input(L("acc.spec"), value=u.get("spesialisasi") or "")
        no_str = b.text_input(L("acc.str"), value=u.get("no_str") or "")
        if st.form_submit_button(L("acc.save"), type="primary"):
            try:
                supabase.table("admin_users").update(
                    {"nama_lengkap": nama.strip() or u.get("username"), "spesialisasi": spes.strip(), "no_str": no_str.strip()}
                ).eq("username", u["username"]).execute()
                st.session_state["current_user"] = nama.strip() or u.get("username")
                st.success(L("acc.saved"))
            except Exception as e:
                st.error(L("stf.err", e=e))

    st.divider()
    tampilkan_ganti_password()


# ==============================================================================
# KELOLA STAF (khusus admin)
# ==============================================================================
def tampilkan_kelola_staf():
    st.markdown(f"### {L('stf.title')}")
    if st.session_state.get("role") != "admin":
        st.warning(L("stf.only")); return

    try:
        data = supabase.table("admin_users").select("*").order("username").execute().data or []
    except Exception as e:
        st.error(L("stf.err", e=e)); return

    # ---- daftar ----
    st.markdown(f"#### {L('stf.list')}")
    kolom = ["username", "nama_lengkap", "role", "spesialisasi", "no_str", "is_active", "last_login"]
    df = pd.DataFrame(data)
    st.dataframe(df[[c for c in kolom if c in df.columns]] if not df.empty else df, width="stretch", hide_index=True)

    # ---- tambah ----
    with st.expander(f"➕ {L('stf.add')}"):
        with st.form("form_tambah_staf", clear_on_submit=True):
            a, b = st.columns(2)
            uname = a.text_input(L("stf.username"))
            nama = b.text_input(L("stf.name"))
            c, d = st.columns(2)
            role = c.selectbox(L("stf.role"), ["dokter", "admin"], format_func=lambda r: L(f"role.{r}"))
            spes = d.text_input(L("acc.spec"))
            pw = st.text_input(L("stf.temp"), value=buat_password_sementara())
            if st.form_submit_button(L("stf.create"), type="primary"):
                uname = uname.strip()
                if not (uname and nama.strip() and pw):
                    st.warning(L("stf.fill"))
                elif any(x["username"] == uname for x in data):
                    st.error(L("stf.exists"))
                else:
                    try:
                        supabase.table("admin_users").insert({
                            "username": uname, "nama_lengkap": nama.strip(), "role": role, "spesialisasi": spes.strip(),
                            "is_active": True, "must_change_password": True,
                            "password_hash": hash_password(pw), "password": "",
                        }).execute()
                        st.success(L("stf.created", u=uname))
                        st.code(pw)
                        st.caption(L("stf.once"))
                    except Exception as e:
                        st.error(L("stf.err", e=e))

    # ---- ubah / nonaktifkan / reset ----
    if not data:
        return
    st.markdown(f"#### {L('stf.edit')}")
    pilih = st.selectbox(L("stf.pick"), [x["username"] for x in data], key="stf_pick")
    cur = next(x for x in data if x["username"] == pilih)
    diri_sendiri = pilih == st.session_state.get("current_username")
    if diri_sendiri:
        st.info(L("stf.self"))

    with st.form("form_edit_staf"):
        a, b = st.columns(2)
        nama = a.text_input(L("stf.name"), value=cur.get("nama_lengkap") or "")
        spes = b.text_input(L("acc.spec"), value=cur.get("spesialisasi") or "")
        c, d = st.columns(2)
        roles = ["dokter", "admin"]
        role = c.selectbox(L("stf.role"), roles, index=roles.index((cur.get("role") or "dokter").lower()) if (cur.get("role") or "dokter").lower() in roles else 0,
                           format_func=lambda r: L(f"role.{r}"), disabled=diri_sendiri)
        aktif = d.checkbox(L("stf.active"), value=cur.get("is_active") is not False, disabled=diri_sendiri)
        if st.form_submit_button(L("stf.save"), type="primary"):
            try:
                upd = {"nama_lengkap": nama.strip(), "spesialisasi": spes.strip()}
                if not diri_sendiri:
                    upd.update({"role": role, "is_active": aktif})
                supabase.table("admin_users").update(upd).eq("username", pilih).execute()
                if not diri_sendiri and not aktif:
                    hapus_sesi_user(pilih)          # akun dinonaktifkan -> langsung keluar dari semua perangkat
                st.success(L("stf.saved"))
                st.rerun()
            except Exception as e:
                st.error(L("stf.err", e=e))

    if st.button(f"🔑 {L('stf.reset')}", key="stf_reset"):
        try:
            sementara = buat_password_sementara()
            ubah_password_db(pilih, sementara, wajib_ganti=True)
            hapus_sesi_user(pilih)                  # paksa login ulang dengan password sementara
            st.success(L("stf.resetok", u=pilih))
            st.code(sementara)
            st.caption(L("stf.once"))
        except Exception as e:
            st.error(L("stf.err", e=e))


# ==============================================================================
# POPUP KONFIRMASI LOGOUT
# ==============================================================================
_DLG_CSS = """
<style>
div[data-testid="stDialog"] div[role="dialog"]{border-radius:22px;box-shadow:0 30px 70px -30px rgba(11,27,58,.55)}
.lo-wrap{text-align:center;padding:.4rem .5rem .8rem}
.lo-ic{width:64px;height:64px;border-radius:50%;margin:0 auto 1rem;background:#FDECEC;display:flex;align-items:center;justify-content:center}
.lo-ic svg{width:30px;height:30px;stroke:#D92D2D;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.lo-q{font-weight:800;font-size:1.2rem;color:#0B1B3A;margin-bottom:.5rem}
.lo-n{color:#5E6C84;font-size:.92rem;line-height:1.6;margin:0}
</style>
"""


def buka_dialog_logout(logout_fn):
    """Tampilkan popup 'Yakin ingin keluar?'. Panggil saat tombol Logout ditekan."""
    @st.dialog(L("logout.title"), width="small")
    def _dlg():
        st.markdown(" ".join(_DLG_CSS.split()) + (
            '<div class="lo-wrap"><div class="lo-ic"><svg viewBox="0 0 24 24"><path d="M12 2v10"/>'
            '<path d="M18.4 6.6a9 9 0 1 1-12.8 0"/></svg></div>'
            f'<div class="lo-q">{L("logout.q")}</div><p class="lo-n">{L("logout.note")}</p></div>'),
            unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button(L("logout.no"), use_container_width=True, key="lo_no"):
            st.rerun()                                   # menutup popup
        if c2.button(L("logout.yes"), type="primary", use_container_width=True, key="lo_yes"):
            logout_fn()
            st.session_state["_toast_logout"] = True
            st.rerun()
    _dlg()