"""
Penjaga unggahan citra MRI. Dijalankan SEBELUM model AI dipakai.
"""
import numpy as np
from PIL import Image, UnidentifiedImageError
from navbar.kamus_bahasa import get_lang

MAKS_MB = 10              # batas ukuran file (MB)
MIN_SISI = 128            # sisi terpendek minimal (px)
MAKS_RASIO = 1.6          # diperketat: rasio lebar:tinggi maksimal (MRI selalu mendekati persegi)
MAKS_WARNA = 15           # diperketat: batas toleransi warna (0 = abu-abu murni)
MIN_STD = 12              # simpangan baku kecerahan minimal
MIN_LATAR_GELAP = 0.15    # minimal 15% piksel harus gelap (latar khas MRI)
MAKS_LATAR_TERANG = 0.35  # maksimal 35% piksel putih terang (menolak screenshot/diagram berlatar putih)
KEPERCAYAAN_MIN = 70.0    # persen; di bawah ini hasil AI dianggap tidak pasti

TXT = {
    "id": {
        "val.rules": "Syarat citra: satu irisan MRI otak, format JPG/PNG, maksimal {max} MB, sisi terpendek minimal {min} px.",
        "val.big": "Ukuran file {mb} MB melebihi batas {max} MB. Perkecil atau kompres citra, lalu unggah kembali.",
        "val.corrupt": "File tidak dapat dibaca sebagai gambar (rusak atau bukan gambar yang valid). Unggah citra MRI berformat JPG atau PNG.",
        "val.small": "Resolusi terlalu kecil ({w}×{h} px). Sisi terpendek minimal {min} px.",
        "val.ratio": "Rasio gambar tidak wajar ({w}×{h} px). Satu irisan MRI biasanya mendekati persegi.",
        "val.color": "Ditolak: Gambar mengandung warna, bukan citra MRI skala abu-abu (grayscale). Unggah irisan MRI otak asli, bukan foto, diagram, atau tangkapan layar berwarna.",
        "val.blank": "Ditolak: Gambar hampir kosong atau terlalu seragam. Unggah irisan MRI otak yang jelas.",
        "val.dark": "Ditolak: Latar gambar terlalu terang/putih (bukan karakteristik MRI otak yang berlatar gelap). Jangan unggah dokumen, diagram, atau foto biasa.",
        "val.uncertain": "Hasil tidak pasti: kepercayaan AI hanya {conf}% (batas minimal {min}%). Citra mungkin bukan MRI otak atau kualitasnya kurang baik, sehingga diagnosis tidak ditampilkan dan tidak dapat disimpan.",
        "val.blocked": "Penyimpanan diblokir karena hasil AI tidak pasti. Unggah citra MRI otak yang sesuai.",
    },
    "en": {
        "val.rules": "Image requirements: a single brain MRI slice, JPG/PNG format, at most {max} MB, shortest side at least {min} px.",
        "val.big": "File size {mb} MB exceeds the {max} MB limit. Reduce or compress the image and upload it again.",
        "val.corrupt": "The file cannot be read as an image (corrupted or not a valid image). Upload an MRI image in JPG or PNG format.",
        "val.small": "Resolution is too small ({w}×{h} px). The shortest side must be at least {min} px.",
        "val.ratio": "Unusual image proportions ({w}×{h} px). A single MRI slice is normally close to square.",
        "val.color": "Rejected: This is a colour image, not a grayscale MRI. Upload a real brain MRI slice, not a colour photo, diagram, or screenshot.",
        "val.blank": "Rejected: The image is almost blank or too uniform. Upload a clear brain MRI slice.",
        "val.dark": "Rejected: The image background is too bright/white (unlike a typical dark-background MRI). Do not upload documents, diagrams, or regular photos.",
        "val.uncertain": "Uncertain result: AI confidence is only {conf}% (minimum {min}%). The image may not be a brain MRI or its quality may be poor, so the diagnosis is not shown and cannot be saved.",
        "val.blocked": "Saving is blocked because the AI result is uncertain. Upload a suitable brain MRI image.",
    },
}


def L(key, **kw):
    s = TXT.get(get_lang(), {}).get(key) or TXT["id"].get(key, key)
    return s.format(**kw) if kw else s


def pesan(item) -> str:
    """item = (kunci, {argumen}) seperti yang dikembalikan validasi_file()."""
    return L(item[0], **item[1])


def aturan_unggah() -> str:
    return L("val.rules", max=MAKS_MB, min=MIN_SISI)


def validasi_file(uploaded_file):
    """Mengembalikan (gambar_PIL, galat, peringatan)."""
    ukuran_mb = (getattr(uploaded_file, "size", 0) or 0) / 1024 / 1024
    if ukuran_mb > MAKS_MB:
        return None, ("val.big", {"mb": f"{ukuran_mb:.1f}", "max": MAKS_MB}), []

    try:
        uploaded_file.seek(0)
        Image.open(uploaded_file).verify()
        uploaded_file.seek(0)
        img = Image.open(uploaded_file).convert("RGB")
    except (UnidentifiedImageError, OSError, ValueError, SyntaxError, Exception):
        return None, ("val.corrupt", {}), []
    finally:
        try:
            uploaded_file.seek(0)
        except Exception:
            pass

    w, h = img.size
    if min(w, h) < MIN_SISI:
        return None, ("val.small", {"w": w, "h": h, "min": MIN_SISI}), []
    if max(w, h) / min(w, h) > MAKS_RASIO:
        return None, ("val.ratio", {"w": w, "h": h}), []

    arr = np.asarray(img).astype(np.int16)
    selisih_kanal = (np.abs(arr[..., 0] - arr[..., 1]) + np.abs(arr[..., 1] - arr[..., 2])) / 2.0
    
    # Mengecek rata-rata warna DAN persentil ke-90 (agar gambar putih dengan kotak berwarna seperti diagram langsung tertangkap)
    warna_mean = float(np.mean(selisih_kanal))
    warna_p90 = float(np.percentile(selisih_kanal, 90))
    if warna_mean > MAKS_WARNA or warna_p90 > (MAKS_WARNA * 1.5):
        return None, ("val.color", {}), []

    abu = arr.mean(axis=2)
    if float(abu.std()) < MIN_STD:
        return None, ("val.blank", {}), []

    # Menolak tegas jika latar belakang terlalu terang/putih (seperti diagram/dokumen) atau kurang gelap
    proporsi_gelap = float((abu < 45).mean())
    proporsi_terang = float((abu > 220).mean())
    if proporsi_gelap < MIN_LATAR_GELAP or proporsi_terang > MAKS_LATAR_TERANG:
        return None, ("val.dark", {}), []

    peringatan = []
    return img, None, peringatan


def hasil_tidak_pasti(kepercayaan_persen: float) -> bool:
    return kepercayaan_persen < KEPERCAYAAN_MIN