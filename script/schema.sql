-- Crear las tablas
CREATE TABLE IF NOT EXISTS zmap_log (
	port integer not null,
	date date not null,
	time integer not null,
	send integer not null,
	recv integer not null,
	hits float not null,
	PRIMARY KEY (port, date)
);

CREATE TABLE IF NOT EXISTS http_port_80 (
	ip inet not null,
	date date not null,
	success boolean not null,
	data JSONB not null,
  PRIMARY KEY (ip, date)
);

CREATE TABLE IF NOT EXISTS http_port_443 (
	ip inet not null,
	date date not null,
	success boolean not null,
	data JSONB not null,
  PRIMARY KEY (ip, date)
);

CREATE TABLE IF NOT EXISTS http_port_8000 (
	ip inet not null,
	date date not null,
	success boolean not null,
	data JSONB not null,
  PRIMARY KEY (ip, date)
);

CREATE TABLE IF NOT EXISTS http_port_8080 (
	ip inet not null,
	date date not null,
	success boolean not null,
	data JSONB not null,
  PRIMARY KEY (ip, date)
);

-- Tablas Intermedias
CREATE TABLE IF NOT EXISTS http_product (
	port integer not null,
	date date not null,
  product text not null,
  version text,
  total integer not null
);

CREATE TABLE IF NOT EXISTS http_operating_system (
	port integer not null,
	date date not null,
  operation_system text not null,
  version text,
  total integer not null
);

-- Permisos

-- zmap_log
ALTER TABLE zmap_log OWNER TO upload_data_osr;
GRANT ALL ON zmap_log TO upload_data_osr;
GRANT SELECT ON zmap_log TO web_osr;

-- http_port_80
ALTER TABLE http_port_80 OWNER TO upload_data_osr;
GRANT ALL ON http_port_80 TO upload_data_osr;
GRANT SELECT ON http_port_80 TO web_osr;

-- http_port_443
ALTER TABLE http_port_443 OWNER TO upload_data_osr;
GRANT ALL ON http_port_443 TO upload_data_osr;
GRANT SELECT ON http_port_443 TO web_osr;

-- http_port_8000
ALTER TABLE http_port_8000 OWNER TO upload_data_osr;
GRANT ALL ON http_port_8000 TO upload_data_osr;
GRANT SELECT ON http_port_8000 TO web_osr;

-- http_port_8080
ALTER TABLE http_port_8080 OWNER TO upload_data_osr;
GRANT ALL ON http_port_8080 TO upload_data_osr;
GRANT SELECT ON http_port_8080 TO web_osr;

-- http_product
ALTER TABLE http_product OWNER TO upload_data_osr;
GRANT ALL ON http_product TO upload_data_osr;
GRANT SELECT ON http_product TO web_osr;

-- http_operating_system
ALTER TABLE http_operating_system OWNER TO upload_data_osr;
GRANT ALL ON http_operating_system TO upload_data_osr;
GRANT SELECT ON http_operating_system TO web_osr;