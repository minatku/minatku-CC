-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 17 Des 2023 pada 14.16
-- Versi server: 10.4.27-MariaDB
-- Versi PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_minatku`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `major_predict`
--

CREATE TABLE `major_predict` (
  `id_major_predict` int(11) NOT NULL,
  `top_1` varchar(50) NOT NULL,
  `top_2` varchar(50) NOT NULL,
  `top_3` varchar(50) NOT NULL,
  `top_4` varchar(50) NOT NULL,
  `top_5` varchar(50) NOT NULL,
  `id_user` int(11) NOT NULL,
  `create_at` datetime DEFAULT current_timestamp(),
  `update_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `major_predict`
--

INSERT INTO `major_predict` (`id_major_predict`, `top_1`, `top_2`, `top_3`, `top_4`, `top_5`, `id_user`, `create_at`, `update_at`) VALUES
(1, 'Technology', 'Science', 'Social', 'Economics', 'Arts and Literature', 1, '2023-12-17 16:19:57', NULL),
(2, 'Science', 'Technology', 'Social', 'Arts and Literature', 'Economics', 1, '2023-12-17 16:23:27', NULL),
(3, 'Social', 'Economics', 'Technology', 'Arts and Literature', 'Science', 1, '2023-12-17 20:08:39', NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `pertanyaan`
--

CREATE TABLE `pertanyaan` (
  `id_pertanyaan` int(11) NOT NULL,
  `isi_pertanyaan` varchar(255) NOT NULL,
  `kode` varchar(10) NOT NULL,
  `kelas_pertanyaan` varchar(50) NOT NULL,
  `create_at` datetime DEFAULT current_timestamp(),
  `update_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `pertanyaan`
--

INSERT INTO `pertanyaan` (`id_pertanyaan`, `isi_pertanyaan`, `kode`, `kelas_pertanyaan`, `create_at`, `update_at`) VALUES
(1, 'Menguji kualitas komponen sebelum pengiriman', 'R1', 'Realistic', '2023-12-17 16:16:03', NULL),
(2, 'Bekerja di anjungan pengeboran minyak lepas pantai', 'R2', 'Realistic', '2023-12-17 16:16:03', NULL),
(3, 'Mempelajari struktur tubuh manusia', 'I1', 'Investigative', '2023-12-17 16:16:03', NULL),
(4, 'Mempelajari perilaku hewan', 'I2', 'Investigative', '2023-12-17 16:16:03', NULL),
(5, 'Memimpin paduan suara musik', 'A1', 'Artistic', '2023-12-17 16:16:03', NULL),
(6, 'Menyutradarai sebuah drama', 'A2', 'Artistic', '2023-12-17 16:16:03', NULL),
(7, 'Memberikan bimbingan karir kepada orang-orang', 'S1', 'Social', '2023-12-17 16:16:03', NULL),
(8, 'Melakukan pekerjaan sukarela di organisasi', 'S2', 'Social', '2023-12-17 16:16:03', NULL),
(9, 'Menjual waralaba restoran kepada perorangan', 'E1', 'Enterprising', '2023-12-17 16:16:03', NULL),
(10, 'Menjual barang dagangan di toserba', 'E2', 'Enterprising', '2023-12-17 16:16:03', NULL),
(11, 'Membuat cek gaji bulanan untuk sebuah kantor', 'C1', 'Conventional', '2023-12-17 16:16:03', NULL),
(12, 'Menggunakan program komputer untuk menghasilkan tagihan pelanggan', 'C2', 'Conventional', '2023-12-17 16:16:03', NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `user`
--

CREATE TABLE `user` (
  `id_user` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `username` varchar(50) NOT NULL,
  `nama_lengkap` varchar(100) DEFAULT NULL,
  `password` varchar(100) NOT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `gender` enum('Laki-laki','Perempuan','Lainnya') DEFAULT NULL,
  `no_telepon` varchar(15) DEFAULT NULL,
  `lokasi` varchar(100) DEFAULT NULL,
  `is_premium` tinyint(1) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT 0,
  `foto_profil` varchar(255) DEFAULT NULL,
  `create_at` datetime DEFAULT current_timestamp(),
  `update_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`id_user`, `email`, `username`, `nama_lengkap`, `password`, `tanggal_lahir`, `gender`, `no_telepon`, `lokasi`, `is_premium`, `is_admin`, `foto_profil`, `create_at`, `update_at`) VALUES
(1, 'test@gmail.com', 'test_123', 'testing', 'sha256$J3NPk7cBh4OJVCQm$22d59206e86ad2c71001641068d0a321ea5d523abc4d7345f0e97930e8336dba', '2003-12-17', 'Laki-laki', '081234567890', 'Bandung', NULL, 0, 'https://storage.googleapis.com/minatku_bucket/3c67505c-46db-4672-bd17-2124051a99d7.png', '2023-12-17 16:17:16', '2023-12-17 13:05:51');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `major_predict`
--
ALTER TABLE `major_predict`
  ADD PRIMARY KEY (`id_major_predict`),
  ADD KEY `idx_majorpredict_user` (`id_user`);

--
-- Indeks untuk tabel `pertanyaan`
--
ALTER TABLE `pertanyaan`
  ADD PRIMARY KEY (`id_pertanyaan`),
  ADD UNIQUE KEY `kode` (`kode`),
  ADD KEY `idx_pertanyaan_kode` (`kode`);

--
-- Indeks untuk tabel `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `uk_username` (`username`),
  ADD UNIQUE KEY `uk_email` (`email`),
  ADD KEY `idx_user_email` (`email`),
  ADD KEY `idx_user_username` (`username`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `major_predict`
--
ALTER TABLE `major_predict`
  MODIFY `id_major_predict` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `pertanyaan`
--
ALTER TABLE `pertanyaan`
  MODIFY `id_pertanyaan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT untuk tabel `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `major_predict`
--
ALTER TABLE `major_predict`
  ADD CONSTRAINT `major_predict_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
