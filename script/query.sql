select 80 as port, date, data#>>'{metadata, service, product}' as product, data#>>'{metadata, service, version}' as version, count(*) as total from http_port_80 where data#>>'{metadata, service, product}'!='' group by product, version, port, date;

