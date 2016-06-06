# Web-OSR

## Instalación

### Base de Datos
Instalar PostgreSQL 9.4 o superior.

### CentOS / Fedora
```sh
sudo yum -y install python-pip
sudo yum install python-devel postgresql-devel
sudo pip install virtualenv
virtualenv mi_proyecto
. mi_proyecto/bin/activate
pip install -r requirements.txt
```


### Ubuntu

```sh
sudo apt-get install python-pip
sudo apt-get install libpq-dev python-dev
sudo pip install virtualenv
virtualenv mi_proyecto
. mi_proyecto/bin/activate
pip install -r requirements.txt
```

