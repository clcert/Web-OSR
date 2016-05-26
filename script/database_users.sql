-- Crear el usuario
CREATE USER web_osr PASSWORD 'hevia2016';
CREATE USER upload_data_osr PASSWORD 'uploadHevia2016';

-- Crear la base de datos
CREATE DATABASE data_osr OWNER upload_data_osr;