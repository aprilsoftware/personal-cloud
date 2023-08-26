# Install NextCloud
```
apt install postgresql
```

```
apt install php7.4 libapache2-mod-php7.4 php7.4-cli
```

```
apt install php7.4-curl php7.4-xml php-gd php7.4-json php-mbstring php-zip php-pgsql php-bz2 php-intl php7.4-bcmath php-fpm php-imagick php-gmp php-apcu
```

## Create a new partition
```
apt install xfsprogs
```

```
fdisk /dev/vdb
```

```
mkfs.xfs /dev/vdb1
```

```
mkdir /opt/nextcloud
```

```
vi /etc/fstab
```

```
/dev/vdb1       /opt/nextcloud xfs defaults    0       0
```

## Database
```
psql
```

```
create database nextcloud;
```

```
\c nextcloud
```

```
create user nextcloud;
```

```
alter user nextcloud password 'xxx';
```

```
alter database nextcloud set tablespace ts_nextcloud;
```

## Apache 2
```
vi /etc/apache2/sites-available/nextcloud.conf
```

```
Alias /nextcloud "/opt/nextcloud/www"

<Directory /opt/nextcloud/www>
  Require all granted
  AllowOverride All
  Options FollowSymLinks MultiViews

  <IfModule mod_dav.c>
    Dav off
  </IfModule>

</Directory>
```

```
a2ensite nextcloud.conf
```

```
a2enmod rewrite
```

```
a2enmod headers
a2enmod env
a2enmod dir
a2enmod mime
```

```
a2enmod setenvif
```

```
service apache2 restart
```

```
chown -R www-data:www-data /var/www/nextcloud/
```

## SSL
```
a2enmod ssl
a2ensite default-ssl
service apache2 reload
```

```
vi /etc/apache2/sites-enabled/000-default.conf
```

```
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
```

```
vi /etc/apache2/sites-enabled/default-ssl.conf
```
```
SSLCertificateFile /etc/apache2/ssl/server.crt
SSLCertificateKeyFile /etc/apache2/ssl/server.key
```

##  apc
```
vi /etc/php/7.4/cli/php.ini
```

```
apc.enable_cli=1
```

# Maintenance mode
```
sudo -u www-data php occ maintenance:mode --on
```

# Move DB
```
mkdir /opt/nextcloud/pg_nextcloud
```

```
chown postgres:postgres pg_nextcloud
```

```
create tablespace ts_nextcloud location '/opt/nextcloud/ts_nextcloud';
```

```
alter database nextcloud set tablespace ts_nextcloud;
```

# Increase timout installing app
```
vi /opt/nextcloud/www/lib/private/Installer.php
```

```
timeout -> 500 instead of 120
```