-- Crear las tablas
CREATE TABLE IF NOT EXISTS zmap_log (
	port integer not null,
	date date not null,
	time varchar(15) not null,
	send integer not null,
	send_avg varchar(15) not null,
	recv integer not null,
	recv_avg varchar(15) not null,
	hits varchar(15) not null,
	PRIMARY KEY (port, date)
);

CREATE TABLE IF NOT EXISTS http_port_80 (
	ip inet not null,
	date date not null,
	data JSON not null,
  PRIMARY KEY (ip, date)
);

CREATE TABLE IF NOT EXISTS http_port_443 (
	ip inet not null,
	date date not null,
	data JSON not null,
  PRIMARY KEY (ip, date)
);

CREATE TABLE IF NOT EXISTS http_port_8000 (
	ip inet not null,
	date date not null,
	data JSON not null,
  PRIMARY KEY (ip, date)
);

CREATE TABLE IF NOT EXISTS http_port_8080 (
	ip inet not null,
	date date not null,
	data JSON not null,
  PRIMARY KEY (ip, date)
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