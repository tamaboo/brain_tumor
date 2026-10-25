import os
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
from admin.validasi_mri import (
    validasi_file,
    pesan,
    aturan_unggah,
    hasil_tidak_pasti,
    KEPERCAYAAN_MIN,
)

# ==============================================================================
# 1. KONFIGURASI SUPABASE & MODEL AI
# ==============================================================================
BASE_DIR = os.getcwd()

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
    model_path = os.path.join(BASE_DIR, "brain_tumor_efficientnetb2.keras")
    if os.path.exists(model_path):
        return load_model(model_path)
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
# 3. ANTARMUKA MANAJEMEN PASIEN TERINTEGRASI MRI & TEMPLATE DOSEN
# ==============================================================================
JK_DB = ["Laki-laki", "Perempuan"]
JK_LABEL = {"Laki-laki": "pat.male", "Perempuan": "pat.female"}

@st.fragment
def tampilkan_manajemen_pasien():
    st.markdown(f"<h2 style='text-align: center;'>{t('pat.title')}</h2>", unsafe_allow_html=True)
    st.write(t("pat.intro"))

    model = load_tumor_model()

    if "diagnosis_ai" not in st.session_state:
        st.session_state.diagnosis_ai = ""
    if "akurasi_ai" not in st.session_state:
        st.session_state.akurasi_ai = 0.0

    with st.expander(t("pat.expander"), expanded=True):
        st.info("💡 **Standar Input Medis:** Sistem CAD ini hanya menerima citra MRI Otak (potongan Axial, Coronal, atau Sagittal). Jangan unggah CT-Scan, foto rontgen, atau dokumen.")
        st.write("Harap pastikan gambar yang diunggah menyerupai salah satu format potongan MRI berikut:")
        
        try:
            col_t1, col_t2, col_t3 = st.columns(3)
            with col_t1:
                img_sagittal = Image.open(os.path.join(BASE_DIR, "assets", "sagittal.jpeg")).resize((250, 250))
                st.image(img_sagittal, caption="Sagittal (Samping)")
            with col_t2:
                img_axial = Image.open(os.path.join(BASE_DIR, "assets", "axial.jpg")).resize((250, 250))
                st.image(img_axial, caption="Axial (Atas)")
            with col_t3:
                img_coronal = Image.open(os.path.join(BASE_DIR, "assets", "coronal.jpeg")).resize((250, 250))
                st.image(img_coronal, caption="Coronal (Depan)")
        except Exception:
            st.warning("⚠️ Berkas aset template gambar (sagittal, axial, coronal) tidak ditemukan di folder assets/.")

        st.divider()
        st.caption(aturan_unggah())

        uploaded_file = st.file_uploader(t("pat.upload"), type=None, key="mri_upload")

        if uploaded_file is not None:
            image, galat, peringatan = validasi_file(uploaded_file)

            if galat is not None:
                st.error(f"❌ {pesan(galat)}")
                st.stop()

            for item_peringatan in peringatan:
                st.warning(f"⚠️ {pesan(item_peringatan)}")

            img_array_original = np.array(image)
            img_resized = cv2.resize(img_array_original, IMG_SIZE)
            img_batch = np.expand_dims(img_resized, axis=0)

            with st.spinner(t("pat.spinner")):
                heatmap, pred_class_idx, probabilities = get_gradcam_heatmap(model, img_batch)
                overlayed_img = overlay_heatmap(img_resized, heatmap)

                kelas = CLASS_NAMES[pred_class_idx]
                st.session_state.diagnosis_ai = kelas.capitalize()
                st.session_state.akurasi_ai = float(probabilities[pred_class_idx] * 100)

            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.image(image, caption=t("pat.cap.orig"), width="stretch")
            with col_img2:
                st.image(overlayed_img, caption=t("pat.cap.cam"), width="stretch")

            if hasil_tidak_pasti(st.session_state.akurasi_ai):
                st.warning(f"⚠️ {pesan(('val.uncertain', {'conf': f'{st.session_state.akurasi_ai:.2f}', 'min': KEPERCAYAAN_MIN}))}")
                st.error(f"🔒 {pesan(('val.blocked', {}))}")
                st.stop()

            st.success(t("pat.result", dx=t(f"class.{kelas}"), conf=st.session_state.akurasi_ai))

            # 4. FORMULIR REKAM MEDIS PASIEN
            st.markdown(t("pat.step2"))
            with st.form("form_pasien", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    no_rm = st.text_input(t("pat.rm"))
                    nama = st.text_input(t("pat.name"))
                with col2:
                    umur = st.number_input(t("pat.age"), min_value=1, max_value=120, value=30)
                    jk = st.selectbox(t("pat.gender"), JK_DB, format_func=lambda v: t(JK_LABEL[v]))

                # --- PERBAIKAN: Tombol diubah menjadi "Save" saja ---
                submit_pasien = st.form_submit_button("Save", type="primary")
                
                if submit_pasien:
                    if no_rm and nama:
                        try:
                            supabase.table("patients").insert({
                                "no_rekam_medis": no_rm,
                                "nama_lengkap": nama,
                                "usia": umur,
                                "jenis_kelamin": jk,
                                "diagnosis_tumor": st.session_state.diagnosis_ai,
                                "kepercayaan_ai": st.session_state.akurasi_ai,
                                "tanggal_scan": str(date.today()),
                                "scanned_by": st.session_state.get("current_user", "")
                            }).execute()
                            st.success(t("pat.ok", nama=nama))
                        except Exception as e:
                            st.error(t("pat.fail", e=e))
                    else:
                        st.warning(t("pat.warn"))

    # ==============================================================================
    # 5. LIVE DATABASE EDITOR
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
                width="stretch",
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
        else:
            st.info(t("pat.empty"))
    except Exception as e:
        st.error(t("pat.loadfail", e=e))