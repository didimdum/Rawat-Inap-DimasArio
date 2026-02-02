-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 26, 2026 at 04:24 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rawatinap_dimas`
--

-- --------------------------------------------------------

--
-- Table structure for table `kamar_dimas`
--

CREATE TABLE `kamar_dimas` (
  `id_kamar` varchar(10) NOT NULL,
  `no_kamar` int(5) NOT NULL,
  `kelas` varchar(15) NOT NULL,
  `status_kamar` varchar(15) NOT NULL,
  `deskripsi` varchar(150) NOT NULL,
  `harga` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kamar_dimas`
--

INSERT INTO `kamar_dimas` (`id_kamar`, `no_kamar`, `kelas`, `status_kamar`, `deskripsi`, `harga`) VALUES
('KI-001', 1, 'II', 'Tidak Tersedia', 'Fasilitas hanya sederhana (seadanya)', 50000),
('KI-002', 2, 'I', 'Tersedia', 'Fasilitas lumayan lengkap', 900000),
('KI-003', 3, 'VIP', 'Tersedia', 'Fasilitas sangat lengkap, ruang tv, ac, PS4 dan Wifi', 1300000);

-- --------------------------------------------------------

--
-- Table structure for table `pasien_dimas`
--

CREATE TABLE `pasien_dimas` (
  `id_pasien` varchar(10) NOT NULL,
  `nama` varchar(60) NOT NULL,
  `alamat` varchar(60) NOT NULL,
  `kontak` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pasien_dimas`
--

INSERT INTO `pasien_dimas` (`id_pasien`, `nama`, `alamat`, `kontak`) VALUES
('P-001', 'Jamal', 'Jalan Timur No. 60', '089647956125'),
('P-002', 'Maulana', 'Jalan jalan No. 8', '085469125746'),
('P-003', 'Azzam', 'Cihanjuang No 99', '086497513596'),
('P-004', 'Moy', 'Jalan Pegangsaan Timur', '089645876235'),
('P-005', 'Ario', 'Kamarung', '089675388778');

-- --------------------------------------------------------

--
-- Table structure for table `rawat_inap_dimas`
--

CREATE TABLE `rawat_inap_dimas` (
  `id_rawat` varchar(10) NOT NULL,
  `id_pasien` varchar(10) NOT NULL,
  `id_kamar` varchar(10) NOT NULL,
  `tgl_masuk` date NOT NULL,
  `tgl_keluar` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rawat_inap_dimas`
--

INSERT INTO `rawat_inap_dimas` (`id_rawat`, `id_pasien`, `id_kamar`, `tgl_masuk`, `tgl_keluar`) VALUES
('R-001', 'P-001', 'KI-002', '2026-01-07', '2026-01-11'),
('R-002', 'P-002', 'KI-003', '2026-01-10', '2026-01-12'),
('R-003', 'P-003', 'KI-002', '2026-01-10', '2026-01-22'),
('R-004', 'P-004', 'KI-003', '2026-01-01', '2026-01-11'),
('R-005', 'P-005', 'KI-003', '2026-01-05', '2026-01-15');

-- --------------------------------------------------------

--
-- Table structure for table `tarnsaksi_dimas`
--

CREATE TABLE `tarnsaksi_dimas` (
  `id_transaksi` varchar(10) NOT NULL,
  `id_pasien` varchar(10) NOT NULL,
  `total_biaya` int(11) NOT NULL,
  `status_pembayaran` varchar(30) NOT NULL,
  `tanggal_transaksi` date NOT NULL,
  `id_rawat` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tarnsaksi_dimas`
--

INSERT INTO `tarnsaksi_dimas` (`id_transaksi`, `id_pasien`, `total_biaya`, `status_pembayaran`, `tanggal_transaksi`, `id_rawat`) VALUES
('T-001', 'P-001', 3600000, 'Lunas', '2026-01-12', 'R-001'),
('T-002', 'P-002', 1300000, 'Lunas', '2026-01-12', 'R-003'),
('T-003', 'P-003', 3600000, 'Lunas', '2026-02-03', 'R-001');

-- --------------------------------------------------------

--
-- Table structure for table `user_dimas`
--

CREATE TABLE `user_dimas` (
  `id_user` varchar(10) NOT NULL,
  `username` varchar(60) NOT NULL,
  `password` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_dimas`
--

INSERT INTO `user_dimas` (`id_user`, `username`, `password`) VALUES
('U-001', 'Almira', 'orang1'),
('U-002', 'Adira', 'orang2'),
('U-003', 'Denis', 'orang3'),
('U-004', 'Adit', 'orang4'),
('U-005', 'Moy', 'orang5');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `kamar_dimas`
--
ALTER TABLE `kamar_dimas`
  ADD PRIMARY KEY (`id_kamar`);

--
-- Indexes for table `pasien_dimas`
--
ALTER TABLE `pasien_dimas`
  ADD PRIMARY KEY (`id_pasien`);

--
-- Indexes for table `rawat_inap_dimas`
--
ALTER TABLE `rawat_inap_dimas`
  ADD PRIMARY KEY (`id_rawat`),
  ADD KEY `id_pasien` (`id_pasien`),
  ADD KEY `id_kamar` (`id_kamar`);

--
-- Indexes for table `tarnsaksi_dimas`
--
ALTER TABLE `tarnsaksi_dimas`
  ADD PRIMARY KEY (`id_transaksi`),
  ADD KEY `id_pasien` (`id_pasien`),
  ADD KEY `id_rawat` (`id_rawat`);

--
-- Indexes for table `user_dimas`
--
ALTER TABLE `user_dimas`
  ADD PRIMARY KEY (`id_user`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `rawat_inap_dimas`
--
ALTER TABLE `rawat_inap_dimas`
  ADD CONSTRAINT `rawat_inap_dimas_ibfk_1` FOREIGN KEY (`id_pasien`) REFERENCES `pasien_dimas` (`id_pasien`),
  ADD CONSTRAINT `rawat_inap_dimas_ibfk_2` FOREIGN KEY (`id_kamar`) REFERENCES `kamar_dimas` (`id_kamar`);

--
-- Constraints for table `tarnsaksi_dimas`
--
ALTER TABLE `tarnsaksi_dimas`
  ADD CONSTRAINT `tarnsaksi_dimas_ibfk_1` FOREIGN KEY (`id_pasien`) REFERENCES `pasien_dimas` (`id_pasien`),
  ADD CONSTRAINT `tarnsaksi_dimas_ibfk_2` FOREIGN KEY (`id_rawat`) REFERENCES `rawat_inap_dimas` (`id_rawat`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
