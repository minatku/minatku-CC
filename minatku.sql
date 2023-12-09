-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 09 Des 2023 pada 15.53
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
  `id_major` int(11) DEFAULT NULL,
  `foto_profil` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`id_user`, `email`, `username`, `nama_lengkap`, `password`, `tanggal_lahir`, `gender`, `no_telepon`, `lokasi`, `is_premium`, `id_major`, `foto_profil`) VALUES
(7, 'your_email@example.com', 'your_username', 'Your Full Name', 'sha256$cA6s5TzAATMk7POU$1824bfcfbf6a1aff4306e5eae3c80fb6e358727a7d3bb4899e4382068db8498b', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(8, 'your_emal@example.com', 'your_usrname', 'Your Full Name', 'sha256$M0bbAd9irkkYXecG$0e576f62e108ce96ae2d32d86165978540c178d6b46afea2c67ece44758ceaa8', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(9, 'string', 'string', 'string', 'sha256$XkehOIzKjo8ctCJX$1a65e9d2d98d48199715f809ada43ade3ade59eb107b846eb5980a59a85e0975', '2023-12-09', '', 'string', 'string', 1, 0, 'string'),
(10, 'coba@gmail.com', 'cobain', 'nyoba aja', 'sha256$DXAtmkmlYwTSb5mx$4a62ade0c33d25991cc461a8043162d3b34e9641e2a1adf935092e9c8b4eb724', NULL, NULL, NULL, NULL, NULL, NULL, NULL);

--
-- Indexes for dumped tables
--

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
-- AUTO_INCREMENT untuk tabel `pertanyaan`
--
ALTER TABLE `pertanyaan`
  MODIFY `id_pertanyaan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT untuk tabel `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
