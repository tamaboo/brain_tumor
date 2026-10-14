import streamlit as st
from supabase import create_client, Client
from datetime import date
import tensorflow as tf
from tensorflow.keras.models import load_model, Model
import numpy as np
import cv2
from PIL import Image
import pandas as pd
from navbar.kamus_bahasa import t

# ==============================================================================
# 1. KONFIGURASI SUPABASE & MODEL AI
# ==============================================================================
@st.cache_resource
def get_supabase_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase_client()

CLASS_NAMES = ["glioma", "meningioma", "notumor", "pituitary"]
IMG_SIZE = (260, 260)

@st.cache_resource
def load_tumor_model():
    return load_model(r"E:\Skripsi_Web_Tumor\brain_tumor_efficientnetb2.keras")

# ==============================================================================
# 2. FUNGSI GRAD-CAM (XAI)
# ==============================================================================
def get_gradcam_heatmap(model, img_array):
    base_model = model.get_layer("efficientnetb2")
    grad_base_model = Model(
        inputs=base_model.inputs,
        outputs=[base_model.get_layer("top_conv").output, base_model.output]
    )
    with tf.GradientTape() as tape:
        x = model.layers[1](img_array, training=False)
        conv_outputs, x = grad_base_model(x, training=False)
        for layer in model.layers[3:]:
            x = layer(x, training=False)
        predictions = x
        class_idx = tf.argmax(predictions[0])
        loss = predictions[:, class_idx]

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0)

    max_heatmap = tf.reduce_max(heatmap)
    if max_heatmap == 0:
        max_heatmap = 1e-8
    heatmap = heatmap / max_heatmap

    return heatmap.numpy(), class_idx.numpy(), predictions.numpy()[0]

def overlay_heatmap(img, heatmap, alpha=0.4):
    heatmap_resized = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap_uint8 = np.uint8(255 * heatmap_resized)
    heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    return cv2.addWeighted(img, 1 - alpha, heatmap_color, alpha, 0)

# ==============================================================================
# 3. ANTARMUKA MANAJEMEN PASIEN TERINTEGRASI MRI
# ==============================================================================
JK_DB = ["Laki-laki", "Perempuan"]
JK_LABEL = {"Laki-laki": "pat.male", "Perempuan": "pat.female"}

def tampilkan_manajemen_pasien():
    st.markdown(f"<h2 style='text-align: center;'>{t('pat.title')}</h2>", unsafe_allow_html=True)
    st.write(t("pat.intro"))

    model = load_tumor_model()

    # Form Integrasi (Pindai AI + Input Data Pasien)
    with st.expander(t("pat.expander"), expanded=False):
        
# --- PERMINTAAN DOSEN: TEMPLATE VISUAL & EDUKASI ---
        st.info("💡 **Standar Input Medis:** Sistem CAD ini hanya menerima citra MRI Otak (potongan Axial, Coronal, atau Sagittal). Jangan unggah CT-Scan, foto rontgen, atau dokumen.")
        st.write("Harap pastikan gambar yang diunggah menyerupai salah satu format potongan MRI berikut:")
        
        # Menggunakan 5 kolom agar gambar terpusat di tengah
        col_spasi_kiri, col_t1, col_t2, col_t3, col_spasi_kanan = st.columns([1, 2, 2, 2, 1])
        
        with col_t1:
            img_sagittal = Image.open(r"E:\Skripsi_Web_Tumor\assets\sagittal.jpeg").resize((300, 300))
            st.image(img_sagittal, caption="Sagittal (Samping)", width="stretch")
        with col_t2:
            img_axial = Image.open(r"E:\Skripsi_Web_Tumor\assets\axial.jpg").resize((300, 300))
            st.image(img_axial, caption="Axial (Atas)", width="stretch")
        with col_t3:
            img_coronal = Image.open(r"E:\Skripsi_Web_Tumor\assets\coronal.jpeg").resize((300, 300))
            st.image(img_coronal, caption="Coronal (Depan)", width="stretch")
        st.divider()
        # ----------------------------------------------------
        
        uploaded_file = st.file_uploader(t("pat.upload"), type=["jpg", "png", "jpeg"], key="mri_upload")

        diagnosis_ai = ""
        akurasi_ai = 0.0

        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file).convert("RGB")
                
                # --- PERMINTAAN DOSEN: BLOKIR GAMBAR SEMBARANGAN ---
                width, height = image.size
                if width < 120 or height < 120:
                    st.error("❌ Ditolak: Resolusi gambar terlalu kecil atau tidak masuk akal. Harap unggah citra pemindaian MRI yang standar.")
                    st.stop() # Menghentikan kode AI berjalan agar tidak error
                # ---------------------------------------------------

                img_array_original = np.array(image)
                img_resized = cv2.resize(img_array_original, IMG_SIZE)
                img_batch = np.expand_dims(img_resized, axis=0)

                with st.spinner(t("pat.spinner")):
                    heatmap, pred_class_idx, probabilities = get_gradcam_heatmap(model, img_batch)
                    overlayed_img = overlay_heatmap(img_resized, heatmap)

                    kelas = CLASS_NAMES[pred_class_idx]
                    diagnosis_ai = kelas.capitalize()
                    akurasi_ai = float(probabilities[pred_class_idx] * 100)

                col_img1, col_img2 = st.columns(2)
                with col_img1:
                    st.image(image, caption=t("pat.cap.orig"), width="stretch")
                with col_img2:
                    st.image(overlayed_img, caption=t("pat.cap.cam"), width="stretch")

                st.success(t("pat.result", dx=t(f"class.{kelas}"), conf=akurasi_ai))

                # Form Data Diri (Hanya muncul jika MRI sudah dianalisis dan lolos validasi)
                st.markdown(t("pat.step2"))
                with st.form("form_pasien"):
                    col1, col2 = st.columns(2)
                    with col1:
                        no_rm = st.text_input(t("pat.rm"))
                        nama = st.text_input(t("pat.name"))
                    with col2:
                        umur = st.number_input(t("pat.age"), min_value=1, max_value=120, value=30)
                        jk = st.selectbox(t("pat.gender"), JK_DB, format_func=lambda v: t(JK_LABEL[v]))

                    submit = st.form_submit_button(t("pat.save"), type="primary")
                    if submit:
                        if no_rm and nama:
                            try:
                                supabase.table("patients").insert({
                                    "no_rekam_medis": no_rm,
                                    "nama_lengkap": nama,
                                    "usia": umur,
                                    "jenis_kelamin": jk,
                                    "diagnosis_tumor": diagnosis_ai,
                                    "kepercayaan_ai": akurasi_ai,
                                    "tanggal_scan": str(date.today()),
                                    "scanned_by": st.session_state.get("current_user", "")
                                }).execute()
                                st.success(t("pat.ok", nama=nama))
                                st.rerun()
                            except Exception as e:
                                st.error(t("pat.fail", e=e))
                        else:
                            st.warning(t("pat.warn"))

            except Exception as e:
                # Menangkap jika dokter iseng mengubah nama file PDF menjadi .jpg
                st.error("❌ Format berkas rusak atau tidak dikenali sebagai citra medis. Sistem hanya menerima matriks citra yang valid.")

    # ==============================================================================
    # 4. LIVE DATABASE EDITOR (CRUD)
    # ==============================================================================
    st.divider()
    st.markdown(t("pat.db.title"))
    st.info(t("pat.db.help"))

    try:
        response = supabase.table("patients").select("*").execute()

        if response.data:
            df = pd.DataFrame(response.data)

            edited_df = st.data_editor(
                df,
                num_rows="dynamic",
                use_container_width=True,
                hide_index=True,
                key="editor_db"
            )

            if st.button(t("pat.savechg"), type="primary"):
                perubahan = st.session_state["editor_db"]

                if perubahan.get("deleted_rows"):
                    for idx in perubahan["deleted_rows"]:
                        id_hapus = df.iloc[idx]["no_rekam_medis"]
                        supabase.table("patients").delete().eq("no_rekam_medis", id_hapus).execute()

                if perubahan.get("edited_rows"):
                    for idx, edit_data in perubahan["edited_rows"].items():
                        id_edit = df.iloc[idx]["no_rekam_medis"]
                        supabase.table("patients").update(edit_data).eq("no_rekam_medis", id_edit).execute()

                if perubahan.get("added_rows"):
                    for baris_baru in perubahan["added_rows"]:
                        supabase.table("patients").insert(baris_baru).execute()

                st.success(t("pat.chgok"))
                st.rerun()

        else:
            st.info(t("pat.empty"))
    except Exception as e:
        st.error(t("pat.loadfail", e=e))