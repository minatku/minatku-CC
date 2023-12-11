-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 11 Des 2023 pada 15.13
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
-- Database: `minatku`
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
  `tanggal` datetime NOT NULL DEFAULT current_timestamp(),
  `id_user` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `major_predict`
--

INSERT INTO `major_predict` (`id_major_predict`, `top_1`, `top_2`, `top_3`, `top_4`, `top_5`, `tanggal`, `id_user`) VALUES
(1, 'Science', 'Technology', 'Social', 'Arts and Literature', 'Economics', '2023-12-11 21:09:31', 1),
(2, 'Technology', 'Science', 'Social', 'Economics', 'Arts and Literature', '2023-12-11 21:10:02', 1);

-- --------------------------------------------------------

--
-- Struktur dari tabel `pertanyaan`
--

CREATE TABLE `pertanyaan` (
  `id_pertanyaan` int(11) NOT NULL,
  `kode` varchar(10) NOT NULL,
  `isi_pertanyaan` text NOT NULL,
  `kelas_pertanyaan` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `pertanyaan`
--

INSERT INTO `pertanyaan` (`id_pertanyaan`, `kode`, `isi_pertanyaan`, `kelas_pertanyaan`) VALUES
(1, 'R1', 'Menguji kualitas komponen sebelum pengiriman', 'Realistic'),
(2, 'R2', 'Bekerja di anjungan pengeboran minyak lepas pantai', 'Realistic'),
(3, 'I1', 'Mempelajari struktur tubuh manusia', 'Investigative'),
(4, 'I2', 'Mempelajari perilaku hewan', 'Investigative'),
(5, 'A1', 'Memimpin paduan suara musik', 'Artistic'),
(6, 'A2', 'Menyutradarai sebuah drama', 'Artistic'),
(7, 'S1', 'Memberikan bimbingan karir kepada orang-orang', 'Social'),
(8, 'S2', 'Melakukan pekerjaan sukarela di organisasi', 'Social'),
(9, 'E1', 'Menjual waralaba restoran kepada perorangan', 'Enterprising'),
(10, 'E2', 'Menjual barang dagangan di toserba', 'Enterprising'),
(11, 'C1', 'Membuat cek gaji bulanan untuk sebuah kantor', 'Conventional'),
(12, 'C2', 'Menggunakan program komputer untuk menghasilkan tagihan pelanggan', 'Conventional');

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
  `gender` enum('Male','Female','Other') DEFAULT NULL,
  `no_telepon` varchar(15) DEFAULT NULL,
  `lokasi` varchar(100) DEFAULT NULL,
  `is_premium` tinyint(1) DEFAULT NULL,
  `foto_profil` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`id_user`, `email`, `username`, `nama_lengkap`, `password`, `tanggal_lahir`, `gender`, `no_telepon`, `lokasi`, `is_premium`, `foto_profil`) VALUES
(1, 'test1@gmail.com', 'test1', 'test 1', 'sha256$u5d7e59uIqUu1uxT$696e4161b318fd7fa28df18dbfed1aed592437945dc4fa1da2ef2bae78e06b0b', NULL, NULL, NULL, NULL, NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `major_predict`
--
ALTER TABLE `major_predict`
  ADD PRIMARY KEY (`id_major_predict`),
  ADD KEY `id_user` (`id_user`);

--
-- Indeks untuk tabel `pertanyaan`
--
ALTER TABLE `pertanyaan`
  ADD PRIMARY KEY (`id_pertanyaan`);

--
-- Indeks untuk tabel `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `major_predict`
--
ALTER TABLE `major_predict`
  MODIFY `id_major_predict` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

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
