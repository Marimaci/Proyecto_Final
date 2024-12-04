ALTER USER 'root'@'localhost' IDENTIFIED WITH 'mysql_native_password' BY '12345678';
FLUSH PRIVILEGES;


CREATE DATABASE celulares;
USE celulares;

CREATE TABLE tiendas (
    id_tienda INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    precio DECIMAL(10, 2),
    valoracion DECIMAL(3, 2),
    marca VARCHAR(100),
    id_tienda INT,
    FOREIGN KEY (id_tienda) REFERENCES tiendas(id_tienda)
);

SELECT * FROM tiendas;
SELECT * FROM productos;
