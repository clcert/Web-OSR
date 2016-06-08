METADATA_SERVICE_PRODUCT = "SELECT data#>>'{metadata, service, product}' AS name, COUNT(*) AS total " \
                           "FROM http_port_80 WHERE date=%s AND data#>>'{metadata, service, product}'!='' " \
                           "GROUP BY name ORDER BY total DESC;"
