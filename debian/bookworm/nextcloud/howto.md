# Install Nextcloud
```
apt install postgresql
```

```
apt install php8.2 libapache2-mod-php8.2 php8.2-cli
```

```
apt install php8.2-curl php8.2-xml php-gd php-mbstring php-zip php-pgsql php-bz2 php-intl php8.2-bcmath php-fpm php-imagick php-gmp php-apcu php-ldap
```

NOTICE: Not enabling PHP 8.2 FPM by default.
NOTICE: To enable PHP 8.2 FPM in Apache2 do:
NOTICE: a2enmod proxy_fcgi setenvif
NOTICE: a2enconf php8.2-fpm
NOTICE: You are seeing this message because you have apache2 package installed.


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

## Download
```
cd /opt/nextcloud
```

```
wget https://download.nextcloud.com/server/releases/latest.zip
```

```
unzip latest.zip
```

```
mv nextcloud/ www
```

```
rm latest.zip
```

```
chown -R www-data:www-data /opt/nextcloud/www
```

## Database
```
su postgres
```

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
alter database nextcloud OWNER TO nextcloud;
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
a2enmod remoteip
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
vi /etc/php/8.2/apache2/php.ini
```

```
memory_limit = 512M
```


```
service apache2 restart
```

## SSL
```
apt install certbot python3-certbot-apache
```


```
certbot --apache -d nc2.lab1.aprilsoftware.com
```



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
vi /etc/apache2/sites-available/000-default-le-ssl.conf
```

```
...

        ServerAdmin admin@aprilsoftware.com
        DocumentRoot /opt/nextcloud/www

...

    <IfModule mod_headers.c>
      Header always set Strict-Transport-Security "max-age=15552000; includeSubDomains"
    </IfModule>

    RemoteIPProxyProtocol On

...

        </VirtualHost>

        <Directory /opt/nextcloud/www>
                Require all granted
                AllowOverride All
                Options FollowSymLinks MultiViews

                <IfModule mod_dav.c>
                        Dav off
                </IfModule>
        </Directory>
</IfModule>
```


```
a2dissite nextcloud.conf
```

```
systemctl reload apache2
```


```
rm /etc/apache2/sites-available/nextcloud.conf
```

```
service apache2 restart
```


##  apc
```
vi /etc/php/8.2/cli/php.ini
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

# Active Directory
## Filter users
```
(&(|(objectclass=person))(|(|(memberof=CN=Nextcloud Users,CN=Users,DC=example,DC=com)(primaryGroupID=1111))))
```

## Login attributes
```
(&(&(|(objectclass=person)))(samaccountname=%uid))
```


# Upgrade
## Backup

```
pg_dump nextcloud -h localhost -U postgres -f nextcloud-sqlbkp_`date +"%Y%m%d"`.bak
```

## Restore

```
psql
```

```
drop database nextcloud;

create database nextcloud;

alter database nextcloud OWNER TO nextcloud;

\q

```

```
psql -d nextcloud -f nextcloud-sqlbkp.bak
```

## Update eventually /opt/nextcloud/www/config/config.php

## Update Nextcloud

```
vi /etc/php/8.2/mods-available/apcu.ini
```

```
apc.enable_cli=1
```

```
systemctl restart php8.2-fpm
```

```
sudo -u www-data php /opt/nextcloud/www/updater/updater.phar
```