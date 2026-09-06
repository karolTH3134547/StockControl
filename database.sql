CREATE DATABASE IF NOT EXISTS inventario_barrio;
USE inventario_barrio;

CREATE TABLE productos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  categoria VARCHAR(50),
  cantidad INT NOT NULL,
  precio_compra DECIMAL(10,2),
  precio_venta DECIMAL(10,2),
  proveedor VARCHAR(100)
);

CREATE TABLE usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario VARCHAR(50),
  clave VARCHAR(100)
);

INSERT INTO usuarios(usuario, clave) VALUES ('admin','1234');
