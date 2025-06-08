# 📦 Proyek Visualisasi 3D: Meja Belajar dengan Lampu

**Nama**  : [Angga Surya Tri Putra]  
**NIM**   : [202310370311305]  
**Kelas** : [Grafika Komputer D]

---

## 🧠 Deskripsi Model

Proyek ini merupakan model 3D interaktif sebuah **meja belajar** yang dibangun menggunakan **Python** dengan bantuan pustaka **Plotly** dan **NumPy**.

Model terdiri dari:
- Meja utama berbentuk balok
- Empat kaki meja berbentuk silinder
- Sebuah lampu belajar lengkap dengan dasar, tiang, sendi, lengan horizontal, tudung, dan bohlam
- Aksesoris berupa buku dan pensil di atas meja

Model ini dirancang untuk menampilkan pemahaman geometri dasar 3D, transformasi posisi, serta penggunaan `Mesh3d` pada Plotly.

---

## 🧱 Bagian-Bagian Model

| Bagian           | Bentuk Geometri | Warna        | Fungsi                                      |
|------------------|------------------|---------------|----------------------------------------------|
| Meja             | Balok            | #8B4513 (coklat kayu) | Permukaan utama                              |
| Kaki Meja        | Silinder         | #654321       | Menopang meja di keempat sudut               |
| Dasar Lampu      | Balok            | #A9A9A9       | Pondasi lampu di pojok kiri meja             |
| Tiang Lampu      | Silinder         | #696969       | Vertikal menopang sendi lampu                |
| Sendi Lampu      | Bola             | #333333       | Titik sambungan antara tiang dan lengan      |
| Lengan Lampu     | Balok horizontal | #696969       | Menjulur ke kanan (ke dalam meja)            |
| Tudung Lampu     | Kerucut          | #FFD700 (emas) | Penutup lampu di ujung lengan                |
| Bohlam           | Bola             | #FFFFE0 (kuning pucat) | Sumber cahaya lampu                          |
| Buku             | Balok            | #4169E1 (biru) | Diletakkan di atas meja                      |
| Pensil           | Silinder         | #FF0000 (merah) | Diletakkan di atas meja                      |

---

## ⚙️ Cara Menjalankan

### 1. Menjalankan secara Lokal (Python)

Pastikan Python sudah terinstal, lalu jalankan perintah berikut:

```bash
pip install plotly numpy
python main.py
lalu run saja

### 2. Menjalankan HTML menggunakan Live Server

-Pastikan anda sudah menginstall extension Live Server dari Ritwick Dey
-Setelah itu klik kanan pada Index.html lalu klik "Open with Live Server"
