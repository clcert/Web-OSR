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
	port INTEGER NOT NULL,
	date DATE NOT NULL,
	product TEXT NOT NULL,
	version TEXT,
	total INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS http_os (
	port INTEGER NOT NULL,
	date DATE NOT NULL,
	os TEXT NOT NULL,
	version TEXT,
	total INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS http_type (
	port INTEGER NOT NULL,
	date DATE NOT NULL,
	type TEXT NOT NULL,
	total INTEGER NOT NULL
);

-- Permisos de la tabla

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

-- http_os
ALTER TABLE http_os OWNER TO upload_data_osr;
GRANT ALL ON http_os TO upload_data_osr;
GRANT SELECT ON http_os TO web_osr;

-- http_type
ALTER TABLE http_type OWNER TO upload_data_osr;
GRANT ALL ON http_type TO upload_data_osr;
GRANT SELECT ON http_type TO web_osr;