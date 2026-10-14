# NeuroSight — Brain Tumor Diagnostics with Explainable AI

NeuroSight is a web application for **early detection support of brain tumors from MRI images**. It combines:

- an **education website** for the public (what brain tumors are, how the AI works), and
- a **protected clinical area** where authorized medical staff upload an MRI slice, get an AI suggestion **with a Grad-CAM heatmap that shows why the AI decided that way**, and save the result in a patient record database.

> **Disclaimer:** NeuroSight is a research / thesis project. It provides a *second opinion* only and is **not a medical device**. It does not replace a doctor's diagnosis. Use anonymized or consented data only.

---

## 1. What the system does

| Part | Who uses it | What it does |
|---|---|---|
| **Home & Education** | Anyone | Explains brain tumors (Glioma, Meningioma, Pituitary), Explainable AI, and shows an interactive 3D brain with *Anatomy / Grad-CAM / X-ray* views. |
| **User Guide** | Anyone | Step-by-step guide for medical staff. |
| **AI Chatbot** (bubble, bottom-right) | Anyone | Answers education questions about tumors, MRI, Grad-CAM and how to use the site. It does not diagnose. |
| **Medical Staff Area** | Logged-in staff | MRI upload → AI classification + Grad-CAM → save patient record; edit records; manage own account; (admin) manage staff. |
| **Language switch** | Anyone | Indonesian (ID) / English (EN), top-right. |

**AI model:** EfficientNetB2 (transfer learning, Keras), input 260×260 RGB, 4 classes:
`glioma`, `meningioma`, `notumor`, `pituitary`. Explanations use **Grad-CAM** (last conv layer `top_conv`). The model was trained on a public brain tumor MRI dataset from Kaggle.

**Tech stack:** Python 3.11 · Streamlit · TensorFlow/Keras · OpenCV · Supabase (PostgreSQL) · Groq (chatbot) · Three.js (3D brain).

---

## 2. Requirements

- **Windows / macOS / Linux** laptop with internet (the site loads fonts, the 3D library, Supabase and Groq online)
- **Python 3.11** (TensorFlow does not support the newest Python versions) — <https://www.python.org/downloads/>
- A free **Supabase** project — <https://supabase.com>
- A free **Groq** API key (for the chatbot) — <https://console.groq.com/keys>
- ~3 GB free disk space (TensorFlow is large)

---

## 3. Installation

### 3.1 Get the project
Download or clone the project folder and open a terminal in it:

```powershell
cd path\to\Skripsi_Web_Tumor
```

The folder must contain `app.py`, `requirements.txt` and the model file **`brain_tumor_efficientnetb2.keras`** (in the same folder as `app.py`).

### 3.2 Create a virtual environment (recommended)

**Windows (PowerShell)**
```powershell
py -3.11 -m venv venv
.\venv\Scripts\activate
```
If PowerShell blocks the script, run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

**macOS / Linux**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3.3 Install the libraries
```powershell
pip install -r requirements.txt
```
This takes several minutes the first time.

### 3.4 Configure secrets
Create the file **`.streamlit/secrets.toml`** (folder `.streamlit` is in the project root):

```toml
SUPABASE_URL = "https://YOUR-PROJECT.supabase.co"
SUPABASE_KEY = "YOUR-SUPABASE-KEY"
GROQ_API_KEY = "gsk_YOUR_GROQ_KEY"
```

- Supabase values: Project Settings → API (Project URL and API key).
- **Never upload `secrets.toml` to GitHub.** Add `.streamlit/secrets.toml` to `.gitignore`.

The file `.streamlit/config.toml` (website theme) should also exist:

```toml
[theme]
base = "light"
primaryColor = "#2F6BFF"
backgroundColor = "#F1F5FF"
secondaryBackgroundColor = "#EAF0FF"
textColor = "#0B1B3A"
font = "sans serif"
```

### 3.5 Prepare the database (Supabase)
Open **Supabase → SQL Editor**, paste and run:

```sql
-- Patient records
create table if not exists patients (
  id bigint generated always as identity primary key,
  no_rekam_medis text not null unique,
  nama_lengkap text not null,
  usia int,
  jenis_kelamin text,
  diagnosis_tumor text,
  kepercayaan_ai double precision,
  tanggal_scan date,
  scanned_by text,
  created_at timestamptz default now()
);

-- Medical staff accounts
create table if not exists admin_users (
  id bigint generated always as identity primary key,
  username text not null unique,
  nama_lengkap text not null,
  password text not null default '',
  password_hash text,
  role text not null default 'dokter',        -- 'admin' or 'dokter'
  spesialisasi text,
  no_str text,
  is_active boolean not null default true,
  must_change_password boolean not null default false,
  last_login timestamptz
);

-- Login sessions (keeps staff logged in after a page refresh)
create table if not exists admin_sessions (
  token_hash text primary key,
  username text not null,
  expires_at timestamptz not null,
  created_at timestamptz not null default now()
);
create index if not exists admin_sessions_user_idx on admin_sessions (username);
```

Create the **first administrator** (change the password right after your first login):

```sql
insert into admin_users (username, nama_lengkap, password, role)
values ('admin', 'Administrator', 'ChangeMe123', 'admin');
```

> If you enabled **Row Level Security (RLS)** on these tables, either turn it off for this thesis project or add policies that allow your app key to read and write them. Otherwise saving will fail with a permission error.

---

## 4. Run the application

```powershell
streamlit run app.py
```

If the command `streamlit` is not recognized, use:
```powershell
py -3.11 -m streamlit run app.py
```

Your browser opens **<http://localhost:8501>**. The first MRI scan is slower because the model loads into memory once.

To stop the app press `Ctrl + C` in the terminal.

---

## 5. How to use the website

### 5.1 Home page (no login needed)
1. **Home & Education** — read about brain tumors and the AI. In the 3D brain, drag to rotate and use the buttons *Anatomy*, *Grad-CAM*, *X-ray* to switch views.
2. **User Guide** — the four-step workflow for medical staff.
3. **Chatbot** — click **Ask AI Assistant** (bottom-right) and type a question or tap a suggested one. Use the **X** to close it.
4. **Language** — click the **ID** or **EN** flag button (top-right).

### 5.2 Medical Staff Area (login required)
Open the **Medical Staff Area** tab and sign in with an account registered by the administrator.

**A. Patients & MRI**
1. Open **"Add Medical Record & Scan New Patient MRI"**.
2. Upload a patient's MRI image (**JPG / PNG**, one brain slice).
3. The system shows the **original image** and the **Grad-CAM heatmap** side by side, plus the **suggested diagnosis and confidence**. Red areas are the regions that influenced the AI most.
4. Review the result as a *second opinion*, fill in the patient data (medical record number, name, age, gender) and click **Save**. The record stores the diagnosis, confidence, date and the staff member who scanned it.
5. In **Medical Records Database (Live Editor)** you can double-click a cell to edit, tick a row and press the trash icon to delete, then click **Save Table Changes**.

**B. My Account** (every staff member)
- Update your name, specialization and license number.
- Change your password (minimum 8 characters).

**C. Manage Staff** (administrators only)
- See all staff accounts, add a new account (with a temporary password shown once), edit role/specialization, deactivate an account, or reset a password. A reset forces the person to choose a new password at next login.

**D. Logout**
Click **Logout** and confirm in the popup. Staff stay logged in for **8 hours**, even after refreshing the page, until they log out.

| Role | Patients & MRI | My Account | Manage Staff |
|---|---|---|---|
| `dokter` (physician) | ✅ | ✅ | ❌ |
| `admin` | ✅ | ✅ | ✅ |

---

## 6. Project structure

```
Skripsi_Web_Tumor/
├── app.py                          # entry point (tabs, login, chatbot)
├── requirements.txt
├── logo.png                        # logo used in header and login
├── brain_tumor_efficientnetb2.keras  # trained model
├── .streamlit/
│   ├── config.toml                 # theme
│   └── secrets.toml                # keys (do NOT upload)
├── admin/
│   ├── auth.py                     # login, hashed passwords, persistent sessions
│   ├── akun.py                     # My Account, Manage Staff, logout popup
│   └── manajemen_pasien.py         # MRI upload, AI + Grad-CAM, patient database
└── navbar/
    ├── header.py                   # logo, brand name, splash screen, language buttons
    ├── ui_halaman.py               # Home & User Guide pages, 3D brain
    ├── login_ui.py                 # login page
    ├── chatbot.py                  # floating AI chatbot
    ├── kamus_bahasa.py             # ID/EN translations
    ├── edukasi.py / panduan.py     # page entry points
```

---

## 7. Troubleshooting

| Problem | Fix |
|---|---|
| `streamlit` is not recognized | Run `py -3.11 -m streamlit run app.py`, or activate the venv first. |
| `ModuleNotFoundError: No module named ...` | You are using a different Python. Activate the venv and run `pip install -r requirements.txt`. |
| Model file not found | Put `brain_tumor_efficientnetb2.keras` in the same folder as `app.py`. |
| Login or saving fails with a database error | Check `SUPABASE_URL` / `SUPABASE_KEY`, that the SQL in section 3.5 was run, and RLS settings. |
| Logged out after refreshing the page | The `admin_sessions` table is missing, or RLS blocks it. A yellow warning appears after login in that case. |
| Chatbot error `model_not_found` (404) | Groq retires models over time. Edit the `MODELS` list at the top of `navbar/chatbot.py` using the current names at <https://console.groq.com/docs/models>. |
| Chatbot says API key invalid | Check `GROQ_API_KEY` in `secrets.toml`. |
| Page looks broken or content missing | Hard refresh the browser with `Ctrl + Shift + R`. |
| 3D brain or fonts do not appear | Check your internet connection (libraries load from CDNs). |

---

## 8. Limitations

- The AI only knows the **four classes** it was trained on and **always picks one of them**, even for an image that is not a brain MRI. Only upload brain MRI slices.
- Results depend on the training dataset and image quality; confidence is not a guarantee of correctness.
- This is a support tool for education and research, not for clinical decisions on its own.