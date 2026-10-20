# Space Impact — Scratch 3

Game arcade tembak-tembakan luar angkasa yang dibuat sebagai **proyek Scratch 3 asli**, bukan simulasi HTML.

## Bermain

1. Download `Space_Impact.sb3` dari repositori ini.
2. Buka [Scratch Editor](https://scratch.mit.edu/projects/editor/), lalu pilih **File → Load from your computer**.
3. Klik **bendera hijau**, kemudian tekan **Spasi** untuk memulai.
4. Gerakkan pesawat dengan **tombol panah** atau **WASD**, tahan **Spasi** untuk menembak.

## Isi permainan

- 3 gelombang musuh, 2 variasi pesawat lawan.
- Pertarungan bos dengan 28 HP dan peluru plasma yang mengarah ke pemain.
- 3 nyawa, invulnerability sementara setelah terkena serangan.
- Skor +10 tiap musuh dan +5 tiap peluru mengenai bos.
- Layar pembuka, menang, dan kalah; efek suara sintetis orisinal.
- Sprite, latar, suara, dan seluruh skrip Scratch dapat diedit di Scratch Editor.

## Rebuild

Jalankan `python3 build.py` dari root repo untuk menghasilkan `Space_Impact.sb3`, `project.json` dan direktori `assets/`. Hanya memakai Python standard library. `Space_Impact.sb3` merupakan berkas yang diimpor ke Scratch, sedangkan `build.py` menyediakan generator proyek untuk pengembangan.

**Author:** Balya Rochmadi
