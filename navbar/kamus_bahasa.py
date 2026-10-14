"""
Kamus dwibahasa Indonesia (id) <-> Inggris (en).

Cara pakai di file lain:
    from navbar.kamus_bahasa import t
    st.write(t("login.title"))
    st.success(t("pat.ok", nama=nama))      # {nama} diisi lewat argumen

Menambah teks baru: tambahkan kunci yang sama di blok "id" dan "en".
Jika terjemahan Inggris belum ada, otomatis dipakai teks Indonesia.
"""
import streamlit as st
from urllib.parse import quote

TEXT = {
    # ------------------------------------------------------------------ INDONESIA
    "id": {
        # navigasi & umum
        "tab.home": "🏠 Beranda & Edukasi",
        "tab.guide": "📖 Panduan Penggunaan",
        "tab.medic": "🔐 Area Tenaga Medis",
        "brand.tagline": "Diagnostik Tumor Otak Berbasis XAI",
        "splash.loading": "Memuat sistem...",
        # model 3D
        "brain.anat": "Anatomi",
        "brain.lesion": "Area lesi (simulasi)",
        "brain.hint": "Seret untuk memutar &nbsp;&bull;&nbsp; Ganti mode di kiri atas",
        "brain.p1": "Akurat", "brain.p2": "Transparan", "brain.p3": "Dapat dijelaskan",
        # beranda
        "hero.eyebrow": "Sistem Pendukung Keputusan Klinis",
        "hero.title": "Kenali Tumor Otak &amp; Teknologi <span class=\"hl\">XAI</span>",
        "hero.sub": "Platform edukasi dan informasi mengenai deteksi dini tumor otak menggunakan sistem Kecerdasan Buatan yang transparan: setiap hasil disertai alasan visualnya.",
        "fact1.t": "4 kelas", "fact1.d": "Glioma, Meningioma, Pituitary, Normal",
        "fact2.t": "Transparan", "fact2.d": "Hasil dapat ditelusuri (XAI)",
        "fact3.t": "Heatmap", "fact3.d": "Visualisasi Grad-CAM pada citra MRI",
        "fact4.t": "Second opinion", "fact4.d": "Mendukung, bukan menggantikan dokter",
        "what.eyebrow": "Apa itu Tumor Otak?",
        "what.body": "Tumor otak adalah <b>massa atau pertumbuhan sel-sel abnormal</b> di dalam maupun di sekitar otak. Deteksi dini yang akurat sangat penting untuk menentukan langkah perawatan medis yang paling tepat, baik itu <b>pembedahan, radiasi, maupun observasi</b>.",
        "sub.title": "Katalog Subtipe Tumor", "sub.small": "(Subtipe)",
        "sub.desc": "Sistem AI kami dilatih untuk mendeteksi tiga jenis tumor utama, beserta kondisi otak normal.",
        "glioma.tag": "Sel glial",
        "glioma.body": "Tumor yang bermula di sel penyokong otak (<i>sel glial</i>). Bisa jinak, namun banyak yang sangat ganas (seperti <i>Glioblastoma</i>) dan dapat menyebar ke jaringan otak sehat dengan cepat.",
        "mening.tag": "Meninges",
        "mening.body": "Tumor yang tumbuh di selaput pelindung otak dan saraf tulang belakang (<i>meninges</i>). Sebagian besar jinak dan tumbuh lambat, namun ukurannya yang membesar dapat menekan otak.",
        "pit.tag": "Kelenjar pituitari",
        "pit.body": "Tumor yang berkembang di kelenjar pituitari pada dasar otak. Sering kali jinak, namun dapat mengganggu produksi hormon vital yang mengatur berbagai fungsi tubuh.",
        "xai.eyebrow": "Explainable AI",
        "xai.title": "Tentang Sistem Diagnosis AI (XAI)",
        "xai.p": "Biasanya AI bekerja seperti <i>\"kotak gelap\"</i>: komputer memberi jawaban tanpa alasan. Sistem kami menggunakan <b>XAI (Explainable AI)</b> yang transparan dan dapat dipercaya.",
        "xai.c1.tag": "Model klasifikasi",
        "xai.c1.body": "Ibarat asisten dokter yang teliti, model ini telah belajar dari ribuan gambar MRI. Ia mengenali tekstur dan pola mikroskopis yang membedakan satu jenis tumor dari yang lain, secara cepat dan akurat.",
        "xai.c2.tag": "Visualisasi penjelasan",
        "xai.c2.body": "Untuk membuktikan prediksinya, sistem menampilkan <i>heatmap</i> di atas gambar MRI. Warna <b style='color:#D92D2D'>merah</b> menandai area yang paling memengaruhi keputusan AI, sehingga dokter dapat memvalidasinya.",
        "legend.low": "Pengaruh rendah", "legend.high": "Pengaruh tinggi",
        "note.edu": "<b>Catatan:</b> sistem ini adalah alat bantu <i>second opinion</i> dan bukan pengganti diagnosis dokter. Keputusan klinis tetap berada pada tenaga medis.",
        # panduan
        "guide.eyebrow": "Panduan",
        "guide.title": "Panduan Penggunaan Sistem XAI",
        "guide.sub": "Empat langkah terstruktur untuk mendiagnosis citra MRI dengan aplikasi ini.",
        "s1.t": "Proses Autentikasi",
        "s1.b": "<p>Fitur diagnosis inti dikhususkan untuk profesional medis yang memiliki otorisasi. Klik tab <b>'Area Tenaga Medis'</b> di bilah atas, lalu masukkan <i>Username</i> dan <i>Password</i> Anda (gunakan akun yang didaftarkan oleh administrator).</p>",
        "s2.t": "Mengunggah Citra MRI",
        "s2.b": "<p>Setelah <i>login</i>, Anda akan melihat <b>Dashboard Diagnostik XAI</b>. Siapkan hasil <i>scan</i> MRI pasien dalam format gambar biasa (<code>.jpg</code> atau <code>.png</code>). Klik <b>'Browse files'</b> atau seret gambar ke kotak area unggah.</p>",
        "s3.t": "Eksekusi Inferensi AI",
        "s3.b": "<p>Setelah gambar terunggah, sistem memuat model <i>EfficientNetB2</i>. Tunggu beberapa detik; layar akan diburamkan sementara AI mengekstraksi ciri-ciri patologis dari gambar.</p>",
        "s4.t": "Membaca Hasil &amp; Heatmap Grad-CAM",
        "s4.intro": "Sistem menyandingkan dua visualisasi untuk Anda evaluasi:",
        "demo.orig": "MRI asli", "demo.heat": "Heatmap Grad-CAM",
        "s4.l1": "<b>Citra kiri:</b> gambar MRI asli yang diunggah.",
        "s4.l2": "<b>Citra kanan (heatmap):</b> perhatikan area <b style=\"color:#D92D2D\">merah pekat</b>; itu fokus utama model.",
        "s4.l3": "<b>Diagnosis akhir:</b> saran subtipe tumor beserta <i>Confidence Score</i> sebagai landasan <i>second opinion</i>.",
        "note.guide": "<b>Penting:</b> hasil AI adalah alat bantu <i>second opinion</i>, bukan pengganti diagnosis dokter. Selalu validasi dengan pemeriksaan klinis.",
        # login & app
        "login.title": "Portal Autentikasi Tenaga Medis",
        "login.sub": "Masuk menggunakan kredensial terdaftar untuk mengakses instrumen XAI.",
        "login.user": "Username", "login.pass": "Password", "login.btn": "Masuk Sistem",
        "login.fail": "Username atau password salah.",
        "login.eyebrow": "Portal Tenaga Medis", "login.heading": "Masuk ke akun Anda",
        "login.ph.user": "Masukkan username", "login.ph.pass": "Masukkan password",
        "login.empty": "Harap isi username dan password.", "login.checking": "Memeriksa kredensial...",
        "login.help": "Lupa akun? Hubungi administrator sistem.",
        "login.welcome": "Selamat datang kembali",
        "login.lead": "Akses dashboard diagnostik XAI untuk memindai citra MRI dan mengelola rekam medis pasien.",
        "login.b1": "Akses aman untuk tenaga medis terotorisasi",
        "login.b2": "Hasil AI yang dapat dijelaskan dengan Grad-CAM",
        "login.b3": "Rekam medis pasien dalam satu tempat",
        "login.note": "Khusus tenaga medis berwenang",
        "auth.dberr": "Gagal terhubung ke database: {e}",
        "app.connected": "Terkoneksi sebagai", "app.logout": "Logout",
        # manajemen pasien
        "pat.title": "👥 Manajemen Data & Pemindaian MRI",
        "pat.intro": "Tambahkan rekam medis baru, pindai citra MRI secara langsung, dan simpan hasil diagnosis permanen ke Supabase.",
        "pat.expander": "➕ Tambah Rekam Medis & Pindai MRI Pasien Baru",
        "pat.upload": "1. Unggah Citra MRI Pasien (JPG/PNG)",
        "pat.spinner": "Menganalisis matriks citra medis...",
        "pat.cap.orig": "Citra MRI Asli", "pat.cap.cam": "Fokus Area Tumor (Grad-CAM)",
        "pat.result": "**Hasil Diagnostik Tersaran:** {dx} (Tingkat Kepercayaan: {conf:.2f}%)",
        "pat.step2": "### 2. Lengkapi Data Demografi Pasien",
        "pat.rm": "ID / Nomor Rekam Medis", "pat.name": "Nama Lengkap", "pat.age": "Umur",
        "pat.gender": "Jenis Kelamin", "pat.male": "Laki-laki", "pat.female": "Perempuan",
        "pat.save": "Simpan Permanen ke Supabase",
        "pat.ok": "Data rekam medis {nama} beserta hasil MRI berhasil disimpan!",
        "pat.fail": "Gagal menyimpan ke database. Pesan sistem: {e}",
        "pat.warn": "Harap isi Nomor Rekam Medis dan Nama Lengkap.",
        "pat.db.title": "#### ⚙️ Database Rekam Medis (Live Editor)",
        "pat.db.help": "💡 **Cara Edit:** Klik ganda (double-click) pada sel tabel untuk mengubah teks.\n\n💡 **Cara Hapus:** Centang kotak kecil di ujung kiri baris, lalu klik ikon tempat sampah 🗑️ di pojok kanan atas tabel.",
        "pat.savechg": "💾 Simpan Perubahan Tabel",
        "pat.chgok": "Perubahan database berhasil disimpan secara permanen!",
        "pat.empty": "Belum ada data pasien di dalam database.",
        "pat.loadfail": "Gagal memuat atau memperbarui data dari Supabase: {e}",
        "class.glioma": "Glioma", "class.meningioma": "Meningioma", "class.pituitary": "Pituitary",
        "class.notumor": "Tidak ada tumor",
        # chatbot
        "chat.fab": "Tanya Asisten AI",
        "chat.title": "Asisten Tumor Otak",
        "chat.status": "Online · edukasi, bukan diagnosis",
        "chat.close": "Tutup",
        "chat.greet": "Halo! 👋 Saya asisten edukasi tumor otak. Tanyakan tentang jenis tumor, cara kerja AI/Grad-CAM, atau cara memakai website ini.",
        "chat.q1": "Apa beda Glioma & Meningioma?", "chat.q2": "Apa itu Grad-CAM?",
        "chat.q3": "Bagaimana cara memakai website ini?", "chat.q4": "Apakah hasil AI ini akurat?",
        "chat.msg": "Pesan", "chat.placeholder": "Tulis pertanyaan Anda...",
        "chat.clear": "🗑️ Hapus percakapan", "chat.think": "Sedang berpikir",
        "chat.empty": "Maaf, saya belum bisa menjawab itu. Coba tanyakan dengan kalimat lain.",
        "chat.err.key": "⚠️ API key belum diatur. Tambahkan `GROQ_API_KEY` di `.streamlit/secrets.toml`.",
        "chat.err.rate": "⏳ Terlalu banyak permintaan. Tunggu sebentar lalu coba lagi.",
        "chat.err.auth": "🔑 API key tidak valid. Periksa kembali `GROQ_API_KEY`.",
        "chat.err.generic": "⚠️ Terjadi kesalahan: {e}",
        "chat.lang_directive": "\n- Jawab SELALU dalam Bahasa Indonesia.",
    },
    # ------------------------------------------------------------------ ENGLISH
    "en": {
        "tab.home": "🏠 Home & Education",
        "tab.guide": "📖 User Guide",
        "tab.medic": "🔐 Medical Staff Area",
        "brand.tagline": "XAI-Based Brain Tumor Diagnostics",
        "splash.loading": "Loading system...",
        "brain.anat": "Anatomy",
        "brain.lesion": "Lesion area (simulated)",
        "brain.hint": "Drag to rotate &nbsp;&bull;&nbsp; Switch mode at top left",
        "brain.p1": "Accurate", "brain.p2": "Transparent", "brain.p3": "Explainable",
        "hero.eyebrow": "Clinical Decision Support System",
        "hero.title": "Understand Brain Tumors &amp; <span class=\"hl\">XAI</span> Technology",
        "hero.sub": "An education and information platform on early brain tumor detection using a transparent Artificial Intelligence system: every result comes with its visual explanation.",
        "fact1.t": "4 classes", "fact1.d": "Glioma, Meningioma, Pituitary, Normal",
        "fact2.t": "Transparent", "fact2.d": "Results can be traced (XAI)",
        "fact3.t": "Heatmap", "fact3.d": "Grad-CAM visualization on MRI images",
        "fact4.t": "Second opinion", "fact4.d": "Supports, not replaces, the doctor",
        "what.eyebrow": "What is a Brain Tumor?",
        "what.body": "A brain tumor is a <b>mass or growth of abnormal cells</b> inside or around the brain. Accurate early detection is essential to determine the most appropriate medical treatment, whether <b>surgery, radiation, or observation</b>.",
        "sub.title": "Tumor Subtype Catalog", "sub.small": "(Subtypes)",
        "sub.desc": "Our AI system is trained to detect three main tumor types, as well as the normal brain condition.",
        "glioma.tag": "Glial cells",
        "glioma.body": "A tumor that begins in the brain's supporting cells (<i>glial cells</i>). It can be benign, but many are highly malignant (such as <i>Glioblastoma</i>) and can spread quickly into healthy brain tissue.",
        "mening.tag": "Meninges",
        "mening.body": "A tumor that grows in the protective membranes of the brain and spinal cord (<i>meninges</i>). Most are benign and slow-growing, but as they enlarge they can press on the brain.",
        "pit.tag": "Pituitary gland",
        "pit.body": "A tumor that develops in the pituitary gland at the base of the brain. It is often benign, but it can disrupt the production of vital hormones that regulate many bodily functions.",
        "xai.eyebrow": "Explainable AI",
        "xai.title": "About the AI Diagnosis System (XAI)",
        "xai.p": "AI usually works like a <i>\"black box\"</i>: the computer gives an answer without a reason. Our system uses <b>XAI (Explainable AI)</b>, which is transparent and trustworthy.",
        "xai.c1.tag": "Classification model",
        "xai.c1.body": "Like a meticulous doctor's assistant, this model has learned from thousands of MRI images. It recognizes the microscopic textures and patterns that distinguish one tumor type from another, quickly and accurately.",
        "xai.c2.tag": "Explanation visualization",
        "xai.c2.body": "To justify its prediction, the system overlays a <i>heatmap</i> on the MRI image. <b style='color:#D92D2D'>Red</b> marks the areas that most influenced the AI's decision, so doctors can validate it.",
        "legend.low": "Low influence", "legend.high": "High influence",
        "note.edu": "<b>Note:</b> this system is a <i>second opinion</i> aid and not a substitute for a doctor's diagnosis. Clinical decisions remain with medical professionals.",
        "guide.eyebrow": "Guide",
        "guide.title": "XAI System User Guide",
        "guide.sub": "Four structured steps to diagnose MRI images with this application.",
        "s1.t": "Authentication",
        "s1.b": "<p>The core diagnosis feature is reserved for authorized medical professionals. Click the <b>'Medical Staff Area'</b> tab in the top bar, then enter your <i>Username</i> and <i>Password</i> (use the account registered by the administrator).</p>",
        "s2.t": "Uploading the MRI Image",
        "s2.b": "<p>After <i>logging in</i>, you will see the <b>XAI Diagnostic Dashboard</b>. Prepare the patient's MRI <i>scan</i> as a regular image (<code>.jpg</code> or <code>.png</code>). Click <b>'Browse files'</b> or drag the image into the upload area.</p>",
        "s3.t": "Running AI Inference",
        "s3.b": "<p>Once the image is uploaded, the system loads the <i>EfficientNetB2</i> model. Wait a few seconds; the screen will blur while the AI extracts pathological features from the image.</p>",
        "s4.t": "Reading the Results &amp; Grad-CAM Heatmap",
        "s4.intro": "The system places two visualizations side by side for you to evaluate:",
        "demo.orig": "Original MRI", "demo.heat": "Grad-CAM Heatmap",
        "s4.l1": "<b>Left image:</b> the original MRI image you uploaded.",
        "s4.l2": "<b>Right image (heatmap):</b> look at the <b style=\"color:#D92D2D\">deep red</b> areas; that is the model's main focus.",
        "s4.l3": "<b>Final diagnosis:</b> a suggested tumor subtype with its <i>Confidence Score</i> as the basis for your <i>second opinion</i>.",
        "note.guide": "<b>Important:</b> AI results are a <i>second opinion</i> aid, not a substitute for a doctor's diagnosis. Always validate with clinical examination.",
        "login.title": "Medical Staff Authentication Portal",
        "login.sub": "Sign in with your registered credentials to access the XAI instruments.",
        "login.user": "Username", "login.pass": "Password", "login.btn": "Sign In",
        "login.fail": "Incorrect username or password.",
        "login.eyebrow": "Medical Staff Portal", "login.heading": "Sign in to your account",
        "login.ph.user": "Enter your username", "login.ph.pass": "Enter your password",
        "login.empty": "Please enter your username and password.", "login.checking": "Verifying credentials...",
        "login.help": "Forgot your credentials? Contact your system administrator.",
        "login.welcome": "Welcome back",
        "login.lead": "Access the XAI diagnostic dashboard to scan MRI images and manage patient records.",
        "login.b1": "Secure access for authorized medical staff",
        "login.b2": "Explainable AI results with Grad-CAM",
        "login.b3": "Patient records in one place",
        "login.note": "Authorized medical personnel only",
        "auth.dberr": "Failed to connect to the database: {e}",
        "app.connected": "Connected as", "app.logout": "Log out",
        "pat.title": "👥 Patient Data Management & MRI Scanning",
        "pat.intro": "Add new medical records, scan MRI images directly, and permanently save diagnosis results to Supabase.",
        "pat.expander": "➕ Add Medical Record & Scan New Patient MRI",
        "pat.upload": "1. Upload Patient MRI Image (JPG/PNG)",
        "pat.spinner": "Analyzing medical image matrix...",
        "pat.cap.orig": "Original MRI Image", "pat.cap.cam": "Tumor Area Focus (Grad-CAM)",
        "pat.result": "**Suggested Diagnostic Result:** {dx} (Confidence Level: {conf:.2f}%)",
        "pat.step2": "### 2. Complete the Patient Demographic Data",
        "pat.rm": "ID / Medical Record Number", "pat.name": "Full Name", "pat.age": "Age",
        "pat.gender": "Gender", "pat.male": "Male", "pat.female": "Female",
        "pat.save": "Save Permanently to Supabase",
        "pat.ok": "Medical record for {nama} and the MRI result were saved successfully!",
        "pat.fail": "Failed to save to the database. System message: {e}",
        "pat.warn": "Please fill in the Medical Record Number and Full Name.",
        "pat.db.title": "#### ⚙️ Medical Records Database (Live Editor)",
        "pat.db.help": "💡 **How to edit:** double-click a table cell to change its text.\n\n💡 **How to delete:** tick the small box at the left end of a row, then click the 🗑️ icon at the top right of the table.",
        "pat.savechg": "💾 Save Table Changes",
        "pat.chgok": "Database changes were saved permanently!",
        "pat.empty": "There is no patient data in the database yet.",
        "pat.loadfail": "Failed to load or update data from Supabase: {e}",
        "class.glioma": "Glioma", "class.meningioma": "Meningioma", "class.pituitary": "Pituitary",
        "class.notumor": "No tumor",
        "chat.fab": "Ask AI Assistant",
        "chat.title": "Brain Tumor Assistant",
        "chat.status": "Online · education, not diagnosis",
        "chat.close": "Close",
        "chat.greet": "Hello! 👋 I'm the brain tumor education assistant. Ask me about tumor types, how the AI / Grad-CAM works, or how to use this website.",
        "chat.q1": "What's the difference between Glioma & Meningioma?", "chat.q2": "What is Grad-CAM?",
        "chat.q3": "How do I use this website?", "chat.q4": "Is the AI result accurate?",
        "chat.msg": "Message", "chat.placeholder": "Type your question...",
        "chat.clear": "🗑️ Clear chat", "chat.think": "Thinking",
        "chat.empty": "Sorry, I can't answer that yet. Please try rephrasing your question.",
        "chat.err.key": "⚠️ API key is not set. Add `GROQ_API_KEY` to `.streamlit/secrets.toml`.",
        "chat.err.rate": "⏳ Too many requests. Please wait a moment and try again.",
        "chat.err.auth": "🔑 Invalid API key. Please check `GROQ_API_KEY`.",
        "chat.err.generic": "⚠️ An error occurred: {e}",
        "chat.lang_directive": "\n- ALWAYS answer in English.",
    },
}


def _bahasa_awal() -> str:
    """Bahasa awal mengikuti bahasa browser (EN jika diawali 'en'), selain itu Indonesia."""
    try:
        loc = (st.context.locale or "").lower()
        return "en" if loc.startswith("en") else "id"
    except Exception:
        return "id"


def get_lang() -> str:
    """Bahasa aktif: 'id' atau 'en' (dibaca dari tombol ID | EN)."""
    v = st.session_state.get("lang_ctrl")
    if v in ("ID", "EN"):
        st.session_state["_lang_last"] = v.lower()
    if "_lang_last" not in st.session_state:
        st.session_state["_lang_last"] = _bahasa_awal()
    return st.session_state["_lang_last"]


def t(key: str, **kw) -> str:
    """Ambil teks sesuai bahasa aktif. Argumen kw mengisi placeholder {nama}."""
    s = TEXT.get(get_lang(), {}).get(key) or TEXT["id"].get(key, key)
    return s.format(**kw) if kw else s


_FLAG_ID = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 3 2'><rect width='3' height='1' fill='#E70011'/>"
            "<rect y='1' width='3' height='1' fill='#fff'/></svg>")
_FLAG_EN = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 30'><clipPath id='s'><path d='M0,0 v30 h60 v-30 z'/></clipPath>"
            "<clipPath id='t'><path d='M30,15 h30 v15 z v15 h-30 z h-30 v-15 z v-15 h30 z'/></clipPath>"
            "<g clip-path='url(#s)'><path d='M0,0 v30 h60 v-30 z' fill='#012169'/>"
            "<path d='M0,0 L60,30 M60,0 L0,30' stroke='#fff' stroke-width='6'/>"
            "<path d='M0,0 L60,30 M60,0 L0,30' clip-path='url(#t)' stroke='#C8102E' stroke-width='4'/>"
            "<path d='M30,0 v30 M0,15 h60' stroke='#fff' stroke-width='10'/>"
            "<path d='M30,0 v30 M0,15 h60' stroke='#C8102E' stroke-width='6'/></g></svg>")


def _uri(svg: str) -> str:
    return "data:image/svg+xml;utf8," + quote(svg)


_LANG_CSS = """
<style>
.st-key-lang_wrap{display:flex;justify-content:flex-end}
.st-key-lang_wrap [data-testid="stHorizontalBlock"]{gap:0!important;width:fit-content;background:#fff;border:1px solid #DCE5FA;
  border-radius:999px;padding:3px;box-shadow:0 8px 20px -14px rgba(47,107,255,.6)}
.st-key-lang_wrap [data-testid="stColumn"]{width:auto!important;flex:0 0 auto!important;min-width:0!important}
.st-key-lang_wrap button{display:flex;align-items:center;justify-content:center;gap:.5rem;min-height:2.2rem;padding:0 1rem;
  border-radius:999px;border:none;font-weight:700;font-size:.82rem;transition:background .15s}
.st-key-lang_wrap button p{margin:0;font-weight:700}
.st-key-lang_wrap button[kind="secondary"]{background:transparent;color:#5E6C84}
.st-key-lang_wrap button[kind="secondary"]:hover{background:#EAF0FF;color:#1F4FD6}
.st-key-lang_wrap button[kind="primary"]{background:#2F6BFF;color:#fff}
.st-key-lang_wrap button::before{content:"";flex:none;width:22px;height:15px;border-radius:3px;background-size:cover;
  background-position:center;box-shadow:0 0 0 1px rgba(0,0,0,.15)}
.st-key-lang_id button::before{background-image:url("__ID__")}
.st-key-lang_en button::before{background-image:url("__EN__")}
</style>
""".replace("__ID__", _uri(_FLAG_ID)).replace("__EN__", _uri(_FLAG_EN))


def _set_lang(kode: str):
    st.session_state["_lang_last"] = kode


def tombol_bahasa():
    """Tombol bahasa berbendera: [ID] | [EN]. Dipanggil sekali (di header)."""
    cur = get_lang()
    with st.container(key="lang_wrap"):
        st.markdown(" ".join(_LANG_CSS.split()), unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="small")
        with c1.container(key="lang_id"):
            st.button("ID", key="lang_btn_id", type="primary" if cur == "id" else "secondary",
                      on_click=_set_lang, args=("id",))
        with c2.container(key="lang_en"):
            st.button("EN", key="lang_btn_en", type="primary" if cur == "en" else "secondary",
                      on_click=_set_lang, args=("en",))