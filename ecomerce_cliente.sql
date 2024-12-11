-- Table for Addresses
CREATE TABLE address (
    address_id INT AUTO_INCREMENT PRIMARY KEY, -- ID único para o endereço
    user_id INT NOT NULL, -- Chave estrangeira associada ao cliente
    street VARCHAR(255) NOT NULL, -- Nome da rua
    number VARCHAR(10) NOT NULL, -- Número da casa
    neighborhood VARCHAR(100) NOT NULL, -- Bairro
    complement VARCHAR(255), -- Complemento (opcional)
    city VARCHAR(100) NOT NULL, -- Cidade
    state VARCHAR(50) NOT NULL, -- Estado
    zip_code VARCHAR(20) NOT NULL, -- CEP
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data de criação
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Data de atualização
    FOREIGN KEY (user_id) REFERENCES customer(customer_id) -- Chave estrangeira para a tabela de clientes
);

-- Table for Customers
CREATE TABLE customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    address_id INT,
    FOREIGN KEY (address_id) REFERENCES address(address_id) ON DELETE SET NULL
);

-- Table for Products
CREATE TABLE product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255),
    product_price DECIMAL(10, 2),
    stock_quantity INT,
    product_description TEXT,
    product_rating DECIMAL(3, 2),
    product_image VARCHAR(255)
);

-- Table for Cart (to register products added to the customer cart)
CREATE TABLE cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    id INT,
    quantity INT,
    price DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (id) REFERENCES product(product_id) ON DELETE CASCADE
);

-- Table for Orders
CREATE TABLE request (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    customer_address_id INT,
    shipping_date DATE,
    total_amount DECIMAL(10, 2),
    order_status VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_address_id) REFERENCES address(address_id) ON DELETE SET NULL
);

-- Table for Order Items (registers the products purchased in an order)
CREATE TABLE request_item (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    product_price DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES order(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE
);
