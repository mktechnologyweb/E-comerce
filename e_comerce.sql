-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 11-Dez-2024 às 13:24
-- Versão do servidor: 10.4.32-MariaDB
-- versão do PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `e_comerce`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `address`
--

CREATE TABLE `address` (
  `address_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `street` varchar(255) NOT NULL,
  `number` varchar(10) NOT NULL,
  `neighborhood` varchar(100) NOT NULL,
  `complement` varchar(255) DEFAULT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(50) NOT NULL,
  `zip_code` varchar(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `address`
--

INSERT INTO `address` (`address_id`, `user_id`, `street`, `number`, `neighborhood`, `complement`, `city`, `state`, `zip_code`, `created_at`, `updated_at`) VALUES
(126, 1, 'aaaa', 'aaa', 'aa', 'a', 'aa', 'aaaa', 'aaa', '2024-10-21 02:43:15', '2024-10-21 02:43:15'),
(127, 2, 'b', 'b', 'b', 'b', 'b', 'b', 'b', '2024-10-21 02:53:03', '2024-10-21 02:53:03'),
(128, 3, 'x', 'x', 'x', 'x', 'x', 'x', 'x', '2024-10-21 17:20:45', '2024-10-21 17:20:45'),
(129, 4, 'rua ui', '5', 'teste', '1', 'ui', 'ui', 'ui', '2024-10-26 22:19:53', '2024-12-09 19:16:41');

-- --------------------------------------------------------

--
-- Estrutura da tabela `cart`
--

CREATE TABLE `cart` (
  `cart_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` decimal(10,0) DEFAULT NULL,
  `totalPriceElement` decimal(10,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `cart`
--

INSERT INTO `cart` (`cart_id`, `customer_id`, `id`, `quantity`, `price`, `totalPriceElement`) VALUES
(135, 1, 60, 2, 4000, 0),
(136, 4, 60, 1, 4000, 0),
(145, 4, 61, 1, 699, 699);

-- --------------------------------------------------------

--
-- Estrutura da tabela `categorias`
--

CREATE TABLE `categorias` (
  `id_categoria` int(11) NOT NULL,
  `nome_categoria` varchar(255) NOT NULL,
  `id_categoria_pai` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `categorias`
--

INSERT INTO `categorias` (`id_categoria`, `nome_categoria`, `id_categoria_pai`) VALUES
(42, 'Telefones e Celulares', NULL),
(43, 'Smartphones', 42),
(44, 'Android', 43),
(45, 'Informática', NULL),
(46, 'Notebook', 45),
(47, 'windows 11', 46),
(48, 'TV e Vídeo', NULL),
(49, 'Televisores', 48),
(50, 'TV 4K', 49),
(51, 'Móveis', NULL),
(52, 'Sala de Estar', 51),
(53, 'Racks e Painéis', 52),
(54, 'Eletroportáteis', NULL),
(55, 'Fritadeiras', 54),
(56, 'Fritadeiras Elétricas', 55),
(60, 'Eletrodomésticos', NULL),
(61, 'Refrigeradores', 60),
(62, 'Geladeira 2 Portas', 61),
(63, 'Fogões', 60),
(64, 'Fogão Piso 4 Bocas', 63);

-- --------------------------------------------------------

--
-- Estrutura da tabela `customer`
--

CREATE TABLE `customer` (
  `customer_id` int(11) NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `customer`
--

INSERT INTO `customer` (`customer_id`, `first_name`, `last_name`, `email`, `password`) VALUES
(1, 'aa', 'bbb', 'teste@teste.com', '1234'),
(2, 'd', 'd', 'd@d', '1234'),
(3, 'use3', '3use', '3@teste', '1234'),
(4, 'uiteste', 'yu', 'uitest@teste.com', '$2b$12$5lF0HCTwt25VrX54/ao7regrVeQQms3Jr/ZB.lfukmYT6QJmrLt6G');

-- --------------------------------------------------------

--
-- Estrutura da tabela `favorites`
--

CREATE TABLE `favorites` (
  `id_fav` int(11) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL,
  `image` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `favorites`
--

INSERT INTO `favorites` (`id_fav`, `id_user`, `id`, `image`) VALUES
(30, 1, 51, 'http://127.0.0.1:8000/uploads/fogao.png');

-- --------------------------------------------------------

--
-- Estrutura da tabela `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `customer_address_id` int(11) DEFAULT NULL,
  `shipping_date` date DEFAULT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `order_status` enum('Pending','Processing','Shipped','Delivered','Canceled') DEFAULT 'Pending',
  `order_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `cart_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `orders`
--

INSERT INTO `orders` (`order_id`, `customer_id`, `customer_address_id`, `shipping_date`, `total_amount`, `order_status`, `order_date`, `cart_id`) VALUES
(267, 1, 126, NULL, 0.00, 'Pending', '2024-10-24 18:44:33', 135),
(269, 4, 129, NULL, 0.00, 'Shipped', '2024-10-26 22:20:57', 136),
(270, 4, 129, NULL, 0.00, 'Pending', '2024-12-09 19:15:42', 145),
(271, 4, 129, NULL, 0.00, 'Pending', '2024-12-09 19:23:47', 145);

-- --------------------------------------------------------

--
-- Estrutura da tabela `order_item`
--

CREATE TABLE `order_item` (
  `order_item_id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `order_item`
--

INSERT INTO `order_item` (`order_item_id`, `order_id`, `product_id`, `quantity`, `price`) VALUES
(132, 267, 60, 1, 4000.18),
(134, 269, 60, 1, 4000.18),
(135, 270, 61, 1, 699.00),
(136, 271, 61, 1, 699.00);

-- --------------------------------------------------------

--
-- Estrutura da tabela `payments`
--

CREATE TABLE `payments` (
  `payment_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `payment_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `payment_status` varchar(50) DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `card_number` varchar(16) DEFAULT NULL,
  `card_name` varchar(255) DEFAULT NULL,
  `expiry_date` varchar(5) DEFAULT NULL,
  `cvv` varchar(3) DEFAULT NULL,
  `user_pyment_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `payments`
--

INSERT INTO `payments` (`payment_id`, `order_id`, `payment_date`, `payment_status`, `amount`, `card_number`, `card_name`, `expiry_date`, `cvv`, `user_pyment_id`) VALUES
(111, 135, '2024-10-24 18:44:33', 'sucesso', 100.00, '5500 0000 0000 0', 'MasterCard', '12/25', '123', 1),
(112, 136, '2024-10-26 22:20:57', 'sucesso', 100.00, '6011 0000 0000 0', 'Discover', '12/25', '123', 4);

-- --------------------------------------------------------

--
-- Estrutura da tabela `product`
--

CREATE TABLE `product` (
  `product_id` int(11) NOT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `product_mark` varchar(50) NOT NULL,
  `product_price` decimal(10,2) DEFAULT NULL,
  `discount_price` decimal(10,2) NOT NULL,
  `stock_quantity` int(11) DEFAULT NULL,
  `product_description` text DEFAULT NULL,
  `product_rating` int(11) DEFAULT NULL,
  `product_image` varchar(255) DEFAULT NULL,
  `id_categoria` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `product`
--

INSERT INTO `product` (`product_id`, `product_name`, `product_mark`, `product_price`, `discount_price`, `stock_quantity`, `product_description`, `product_rating`, `product_image`, `id_categoria`) VALUES
(60, 'Geladeira Electrolux', 'Electrolux', 4000.40, 4000.18, 5, '<p><span style=\"background-color:rgb(255,255,255);color:rgb(87,87,87);\">Design Sofisticado e Tecnologia para sua Cozinha</span><br><span style=\"background-color:rgb(255,255,255);color:rgb(87,87,87);\">A Geladeira Duplex Electrolux 480L Inox oferece versatilidade incomparável, adaptando-se a diversos ambientes. Com as tecnologias AutoSense e SmartBivolt, ela garante mais sabor e frescor para as refeições da sua família, mantendo os alimentos frescos por mais tempo e proporcionando maior flexibilidade no uso.</span><br><br><span style=\"background-color:rgb(255,255,255);color:rgb(87,87,87);\">Frescor Prolongado com Eficiência Energética</span><br><span style=\"background-color:rgb(255,255,255);color:rgb(87,87,87);\">A Gaveta HortiNatura possui uma vedação especial que evita o contato direto com a temperatura da geladeira, preservando o frescor de frutas e vegetais por até 2x mais tempo. Para reduzir o impacto ambiental, a eficiência energética mantém a temperatura mais estável e garante condições ideais para preservar os alimentos, além de ter classificação A+++ e economizar até 47% de energia.</span><br><br><span style=\"background-color:rgb(255,255,255);color:rgb(87,87,87);\">Versatilidade e Inovação em seu Dia a Dia</span><br><span style=\"background-color:rgb(255,255,255);color:rgb(87,87,87);\">A Geladeira Duplex IT70S está equipada com a tecnologia SmartBivolt, que permite você conectar sua geladeira tanto na tensão 127V quanto na 220V. Com isso, você tem mais flexibilidade e maior resistência à oscilação de tensão, garantindo que sua geladeira opere sem interrupções entre 90V e 310V e suporte picos de tensão de até 350V. Conte também com a flexibilidade das prateleiras reversíveis e FastAdapt, que permitem você adaptar o espaço interno da geladeira da forma que desejar.</span></p>', 5, 'http://127.0.0.1:8000/uploads/Geladeira_2_Portas.png', 62),
(61, 'Smartphone Motorola', '', 777.00, 699.00, 5, NULL, 0, 'http://127.0.0.1:8000/uploads/Android.png', 44),
(62, 'Smart TV', '', 2.18, 2.07, 5, NULL, 0, 'http://127.0.0.1:8000/uploads/Smart_TV.png', 50),
(63, 'Fogão Atlas 4', '', 776.00, 737.00, 5, NULL, 0, 'http://127.0.0.1:8000/uploads/fogao.png', 64),
(64, 'Painel Home', '', 699.00, 629.00, 5, NULL, 0, 'http://127.0.0.1:8000/uploads/Racks_e_Paineis.png', 53),
(65, 'Fritadeira ', '', 199.00, 269.00, 5, NULL, 0, 'http://127.0.0.1:8000/uploads/Fritadeiras.png', 56),
(66, 'Notebook ', '', 6.00, 5.40, 5, NULL, 0, 'http://127.0.0.1:8000/uploads/notebook.png', 47);

-- --------------------------------------------------------

--
-- Estrutura da tabela `promotional_slide`
--

CREATE TABLE `promotional_slide` (
  `slide_id` int(11) NOT NULL,
  `slide_image` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `promotional_slide`
--

INSERT INTO `promotional_slide` (`slide_id`, `slide_image`) VALUES
(12, 'http://127.0.0.1:8000/uploads/sale-concept-clock.jpg'),
(13, 'http://127.0.0.1:8000/uploads/sale-with-special-discount-vr-glasses.jpg'),
(14, 'http://127.0.0.1:8000/uploads/sale-with-special-discounts.jpg');

-- --------------------------------------------------------

--
-- Estrutura da tabela `usuarios_admin`
--

CREATE TABLE `usuarios_admin` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('superadmin','store_admin','support_admin') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `usuarios_admin`
--

INSERT INTO `usuarios_admin` (`id`, `username`, `password`, `role`, `created_at`) VALUES
(8, 'ju', '$2b$12$z6VpsI9BuPOoZy82YEHr9OVOGzZKoa.217AywRsMq8iKxR6VhJpJ.', 'superadmin', '2024-10-06 20:01:16'),
(13, 'suport', '$2b$12$AOVRvyBFtXjg2ZEcgMLubOdwH1qmkF6pYD87OI7yhDEcn.Xx7PuW6', 'support_admin', '2024-10-26 19:14:29'),
(14, 'store_admin', '$2b$12$ZzaRzq7spTzQjjh1vnYKIe/2nwEAhRByjKSya4q/EwZjp88D37.l.', 'store_admin', '2024-10-26 19:14:46');

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `address`
--
ALTER TABLE `address`
  ADD PRIMARY KEY (`address_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Índices para tabela `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`cart_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `product_id` (`id`);

--
-- Índices para tabela `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id_categoria`),
  ADD KEY `categorias_ibfk_1` (`id_categoria_pai`);

--
-- Índices para tabela `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Índices para tabela `favorites`
--
ALTER TABLE `favorites`
  ADD PRIMARY KEY (`id_fav`),
  ADD KEY `id_user` (`id_user`);

--
-- Índices para tabela `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `customer_address_id` (`customer_address_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `cart_id` (`cart_id`);

--
-- Índices para tabela `order_item`
--
ALTER TABLE `order_item`
  ADD PRIMARY KEY (`order_item_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `order_item_ibfk_5` (`order_id`);

--
-- Índices para tabela `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`payment_id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `user_pyment_id` (`user_pyment_id`);

--
-- Índices para tabela `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`product_id`),
  ADD KEY `id_categoria` (`id_categoria`);

--
-- Índices para tabela `promotional_slide`
--
ALTER TABLE `promotional_slide`
  ADD PRIMARY KEY (`slide_id`);

--
-- Índices para tabela `usuarios_admin`
--
ALTER TABLE `usuarios_admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `address`
--
ALTER TABLE `address`
  MODIFY `address_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=130;

--
-- AUTO_INCREMENT de tabela `cart`
--
ALTER TABLE `cart`
  MODIFY `cart_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=146;

--
-- AUTO_INCREMENT de tabela `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT de tabela `customer`
--
ALTER TABLE `customer`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de tabela `favorites`
--
ALTER TABLE `favorites`
  MODIFY `id_fav` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de tabela `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=272;

--
-- AUTO_INCREMENT de tabela `order_item`
--
ALTER TABLE `order_item`
  MODIFY `order_item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=137;

--
-- AUTO_INCREMENT de tabela `payments`
--
ALTER TABLE `payments`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=113;

--
-- AUTO_INCREMENT de tabela `product`
--
ALTER TABLE `product`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=75;

--
-- AUTO_INCREMENT de tabela `promotional_slide`
--
ALTER TABLE `promotional_slide`
  MODIFY `slide_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de tabela `usuarios_admin`
--
ALTER TABLE `usuarios_admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `address`
--
ALTER TABLE `address`
  ADD CONSTRAINT `address_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `customer` (`customer_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Limitadores para a tabela `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`id`) REFERENCES `product` (`product_id`) ON DELETE CASCADE;

--
-- Limitadores para a tabela `categorias`
--
ALTER TABLE `categorias`
  ADD CONSTRAINT `categorias_ibfk_1` FOREIGN KEY (`id_categoria_pai`) REFERENCES `categorias` (`id_categoria`) ON DELETE SET NULL ON UPDATE SET NULL;

--
-- Limitadores para a tabela `favorites`
--
ALTER TABLE `favorites`
  ADD CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `customer` (`customer_id`);

--
-- Limitadores para a tabela `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`customer_address_id`) REFERENCES `address` (`address_id`) ON DELETE SET NULL,
  ADD CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `orders_ibfk_4` FOREIGN KEY (`cart_id`) REFERENCES `cart` (`cart_id`) ON DELETE CASCADE;

--
-- Limitadores para a tabela `order_item`
--
ALTER TABLE `order_item`
  ADD CONSTRAINT `order_item_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_item_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_item_ibfk_3` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_item_ibfk_4` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  ADD CONSTRAINT `order_item_ibfk_5` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  ADD CONSTRAINT `order_item_ibfk_6` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  ADD CONSTRAINT `order_item_ibfk_7` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  ADD CONSTRAINT `order_item_ibfk_8` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE;

--
-- Limitadores para a tabela `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `cart` (`cart_id`),
  ADD CONSTRAINT `payments_ibfk_2` FOREIGN KEY (`user_pyment_id`) REFERENCES `customer` (`customer_id`);

--
-- Limitadores para a tabela `product`
--
ALTER TABLE `product`
  ADD CONSTRAINT `product_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
