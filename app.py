import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="🎓 Prediksi Risiko Dropout Mahasiswa", layout="wide")
st.title("🎓 Prediksi Risiko Dropout Mahasiswa")

# === LOAD MODEL ===
model = joblib.load("best_pipeline_lgbm.pkl")  # Ubah ke nama file modelmu

# === FORM INPUT ===
st.header("📝 Masukkan Data Mahasiswa")

col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Jenis Kelamin", ["male", "female"])
    course = st.selectbox("Program Studi", ["Nursing", "Management", "Social Service", "Informatics"])
    scholarship = st.selectbox("Penerima Beasiswa", ["yes", "no"])
    debtor = st.selectbox("Memiliki Utang Akademik", ["yes", "no"])
    displaced = st.selectbox("Status Displaced", ["yes", "no"])

with col2:
    admission_grade = st.number_input("Nilai Masuk (Admission Grade)", min_value=0.0, max_value=20.0, step=0.1)
    age = st.number_input("Usia Saat Mendaftar", min_value=16, max_value=60, step=1)
    first_sem_grade = st.number_input("Rata-rata Nilai Semester 1", min_value=0.0, max_value=20.0, step=0.1)
    second_sem_grade = st.number_input("Rata-rata Nilai Semester 2", min_value=0.0, max_value=20.0, step=0.1)
    attendance = st.selectbox("Jadwal Kuliah", ["daytime", "evening"])

# === KONVERSI INPUT KE DATAFRAME ===
input_dict = {
    "Gender": gender,
    "Course": course,
    "Scholarship_holder": scholarship,
    "Debtor": debtor,
    "Displaced": displaced,
    "Admission_grade": admission_grade,
    "Age_at_enrollment": age,
    "Curricular_units_1st_sem_grade": first_sem_grade,
    "Curricular_units_2nd_sem_grade": second_sem_grade,
    "Daytime_evening_attendance": attendance
}
input_df = pd.DataFrame([input_dict])

# === PASTIKAN INPUT SESUAI DENGAN PIPELINE MODEL ===
expected_features = model.named_steps['pre'].feature_names_in_

# Tambahkan kolom yang hilang secara otomatis
for col in expected_features:
    if col not in input_df.columns:
        input_df[col] = 0  # Default: numerik 0 / string "0" (nanti diatur)

# Urutkan kolom sesuai pipeline
input_df = input_df[expected_features]

# Ambil fitur numerik & kategorikal dari pipeline
preprocessor = model.named_steps['pre']
num_features = preprocessor.transformers_[0][2]
cat_features = preprocessor.transformers_[1][2]

# Format kolom sesuai: numerik & kategorikal
for col in input_df.columns:
    if col in num_features:
        input_df[col] = pd.to_numeric(input_df[col], errors='coerce').fillna(0)
    elif col in cat_features:
        input_df[col] = input_df[col].astype(str)

# === PREDIKSI ===
if st.button("🔍 Prediksi Risiko Dropout"):
    prediction = model.predict(input_df)[0]
    probas = model.predict_proba(input_df)[0]

    # Ambil probabilitas kelas "Dropout"
    if "Dropout" in model.classes_:
        idx = list(model.classes_).index("Dropout")
        prob_dropout = probas[idx]
    else:
        prob_dropout = probas[1]  # fallback binary

    st.subheader("📊 Hasil Prediksi")
    st.write(f"**Status Prediksi:** {prediction}")
    st.write(f"**Probabilitas Dropout:** {prob_dropout:.2%}")

    if prediction == "Dropout" or prob_dropout > 0.5:
        st.error("⚠️ Mahasiswa ini berisiko tinggi mengalami dropout.")
    else:
        st.success("✅ Mahasiswa ini diprediksi aman dari dropout.")