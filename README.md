
# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan

## Business Understanding

Jaya Jaya Institut adalah institusi pendidikan tinggi yang mengalami tantangan signifikan dalam mempertahankan mahasiswa hingga kelulusan. Tingginya angka *dropout* (~32%) berdampak pada reputasi dan efektivitas program pendidikan. Saat ini belum tersedia sistem prediktif dan dashboard pemantauan risiko yang dapat membantu tim akademik dalam mengambil intervensi tepat waktu.

### Permasalahan Bisnis

* Tingginya angka dropout mahasiswa (~32%).
* Kurangnya visibilitas: tidak ada dashboard interaktif untuk memantau risiko berdasarkan segmen (jurusan, jenis kelamin, beasiswa, dsb.).
* Intervensi akademik terlambat: biasanya dilakukan setelah nilai semester menurun.
* Keterbatasan sumber daya: tidak bisa melakukan pendampingan menyeluruh kepada seluruh mahasiswa.

### Cakupan Proyek

* Data preprocessing dan EDA pada dataset performa mahasiswa Jaya Jaya Institut.
* Pengembangan model klasifikasi (LightGBM, Random Forest) untuk memprediksi risiko dropout.
* Pembuatan dashboard analitik di Looker Studio untuk pemantauan bisnis.
* Pembuatan prototype aplikasi prediksi menggunakan Streamlit.
* Implementasi sistem prediktif end-to-end untuk mendukung intervensi dini.

## Persiapan

### Dataset

* **Sumber data**: Dataset performa mahasiswa Jaya Jaya Institut
* **Jumlah data**: 4.424 baris, 37 kolom
* **Fitur utama**:
  * Numerik: `Admission_grade`, `Age_at_enrollment`, `Curricular_units_1st_sem_grade`, dll.
  * Kategorikal: `Gender`, `Course`, `Scholarship_holder`, `Debtor`, dll.
* **Target variabel**: `Status` (Dropout, Enrolled, Graduate)

🔗 [Link Dataset](https://github.com/dicodingacademy/dicoding_dataset/tree/main/students_performance)

### Setup Environment

Buat virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
````

Install dependencies:

```bash
pip install -r requirements.txt
```

Atau install manual:

```bash
pip install pandas scikit-learn matplotlib seaborn streamlit joblib lightgbm 
```

## Business Dashboard

Dashboard **Student Dropout Monitoring** dibuat dengan Looker Studio dan terhubung langsung ke data model prediksi.

### Insight Utama yang Ditampilkan:

* Distribusi status mahasiswa (`Dropout`, `Enrolled`, `Graduate`)
* Dropout rate berdasarkan `Gender`, `Course`, `Scholarship_holder`, `Debtor`, dan `Attendance Time`
* Rata-rata probabilitas dropout (`Prob_Dropout`)
* Visualisasi hubungan `Admission_grade`, `Nilai semester 1`, dan evaluasi akademik dengan status akhir
* Tabel mahasiswa berisiko tinggi berdasarkan probabilitas prediksi

### Fitur Interaktif:

* Filter berdasarkan jurusan, jenis kelamin, dan status beasiswa
* Segmentasi mahasiswa berdasarkan skor risiko
* Pemantauan performa akademik terhadap risiko dropout

🔗 [Dashboard Pemantauan Dropout – Looker Studio](https://lookerstudio.google.com/reporting/4e4aaf14-5de9-4f17-9616-5a9a92c639f9)

## Menjalankan Sistem Machine Learning

Aplikasi prediksi risiko dropout tersedia dalam bentuk prototipe Streamlit.
saya menggunakan model lightgbm walaupun model catboost akurasinya paling tinggi. Namun, karena **model CatBoost tidak kompatibel dengan Streamlit Cloud (Python 3.13)**, maka untuk keperluan deployment digunakan model terbaik kedua, yaitu **LightGBM Classifier**.
Jalankan server Streamlit:

```bash
streamlit run app.py
```

Link aplikasi:
🔗 [https://dashboard-permasalahan-pendidikan-jaya-jaya-maju-xqdj5vn7xa8rd.streamlit.app/](https://dashboard-permasalahan-pendidikan-jaya-jaya-maju-xqdj5vn7xa8rd.streamlit.app/)

## Model & Hasil

Model terbaik adalah **Catboost Classifier** dengan skor sebagai berikut:

* **Accuracy**: 0.77
* **Recall Macro**: 0.77

Pipeline preprocessing mencakup:

* Imputasi missing value
* Encoding kategorikal
* Scaling fitur numerik
* Split stratifikasi berdasarkan kelas target

### Temuan Penting:

* Mahasiswa **kelas malam**, **tanpa beasiswa**, dan **berstatus Debtor** lebih rentan dropout.
* Dropout tinggi ditemukan pada jurusan seperti **Social Service**.
* Nilai akademik rendah pada semester awal menjadi indikator kuat risiko dropout.

## Rekomendasi Action Items

| No | Insight Utama                                              | Action Item                                          | KPI / Target                                  | Pemilik                  | Waktu Implementasi |
| -- | ---------------------------------------------------------- | ---------------------------------------------------- | --------------------------------------------- | ------------------------ | ------------------ |
| 1  | Jurusan Social Service dominan dalam dropout               | Program remedial + mentoring jurusan spesifik        | Dropout turun ≥20% di jurusan ini             | Ketua Program Studi      | Semester 1 2025/26 |
| 2  | Mahasiswa kelas malam memiliki dropout lebih tinggi        | Evaluasi ulang beban dan dukungan kelas malam        | Dropout malam turun ke <25%                   | Wakil Dekan Akademik     | Semester 2 2025/26 |
| 3  | Mahasiswa dengan admission grade rendah cenderung dropout  | Program remedial dan mentoring awal tahun akademik   | Retensi naik ≥15% pada mahasiswa nilai rendah | Tim Akademik & Kurikulum | Semester 1 2025/26 |
| 4  | Perempuan sedikit lebih banyak dropout dibanding laki-laki | Mentoring berbasis gender + dukungan sosial tambahan | Selisih rasio dropout antar gender <5%        | Academic Advising Team   | Semester 1 2025/26 |
| 5  | Mahasiswa tanpa beasiswa lebih berisiko                    | Review dan alokasi beasiswa berbasis prediksi risiko | Dropout kelompok non-beasiswa turun ≥15%      | Biro Kemahasiswaan       | Semester 2 2025/26 |
| 6  | Mahasiswa Debtor lebih rentan dropout                      | Integrasi reminder akademik + konseling keuangan     | Dropout dari kelompok ini turun ≥20%          | Biro Keuangan & Akademik | Q3 2025            |
| 7  | Mahasiswa dengan Prob\_Dropout > 0.7 perlu intervensi awal | Sistem alert dan pemantauan otomatis via dashboard   | ≥70% mahasiswa risiko tinggi tetap bertahan   | Academic Advising Team   | Mulai Agustus 2025 |

