# Install [Apache Guacamole](https://guacamole.apache.org/)
## Build Server
```
apt install build-essential
```

```
apt install libcairo2-dev libjpeg62-turbo-dev libjpeg-dev libpng-dev libtool-bin libwebsockets-dev
```

```
apt install uuid-dev libossp-uuid-dev
```

```
apt install libavcodec-dev libavformat-dev libavutil-dev libswscale-dev
```

```
apt install freerdp2-dev libpango1.0-dev libssh2-1-dev libtelnet-dev libvncserver-dev
```

```
apt install libwebsockets-dev libpulse-dev libssl-dev libvorbis-dev libwebp-dev
```

```
apt install wget
```

```
wget -O guacamole-server-1.5.4.tar.gz https://downloads.apache.org/guacamole/1.5.4/source/guacamole-server-1.5.4.tar.gz
```

```
tar -xzf guacamole-server-1.5.4.tar.gz
```

```
cd guacamole-server-1.5.4
```

```
export CFLAGS="-Wno-error"
```

```
./configure --with-systemd-dir=/etc/systemd/system
```

```
make
```

```
make install
```

```
ldconfig
```

```
mkdir /etc/guacamole
```

```
vi /etc/guacamole/guacd.conf
```

```
[server]
bind_host = 127.0.0.1
bind_port = 4822
```

```
systemctl enable guacd
```

```
systemctl start guacd
```

## Clean install folder
```
cd ..
```

```
rm -r guacamole-server-1.5.4*
```

```
apt remove build-essential
```

```
apt autoremove
```


## Install Client
```
apt install openjdk-17-jdk-headless
```

Tomcat10 not yet supported
```
echo "deb http://deb.debian.org/debian/ bullseye main" | sudo tee /etc/apt/sources.list.d/bullseye.list &> /dev/null
```

```
apt update
```

```
apt install tomcat9
```

```
wget -O guacamole-1.5.4.war https://downloads.apache.org/guacamole/1.5.4/binary/guacamole-1.5.4.war
```

```
systemctl stop tomcat9
```

```
rm -r /var/lib/tomcat9/webapps/ROOT
```

```
mv guacamole-1.5.4.war /var/lib/tomcat9/webapps/ROOT.war
```

# Configuration
```
touch /etc/guacamole/guacamole.properties
```

## Extensions
Active Directory / LDAP
```
wget -O guacamole-auth-ldap-1.5.4.tar.gz https://downloads.apache.org/guacamole/1.5.4/binary/guacamole-auth-ldap-1.5.4.tar.gz
```

JDBC
```
wget -O guacamole-auth-jdbc-1.5.4.tar.gz https://downloads.apache.org/guacamole/1.5.4/binary/guacamole-auth-jdbc-1.5.4.tar.gz
```

[2FA](https://fr.wikipedia.org/wiki/Double_authentification)
```
wget -O guacamole-auth-totp-1.5.4.tar.gz https://downloads.apache.org/guacamole/1.5.4/binary/guacamole-auth-totp-1.5.4.tar.gz
```

```
mkdir /etc/guacamole/extensions
```

```
tar -zxvf guacamole-auth-ldap-1.5.4.tar.gz -C ./
```

```
tar -zxvf guacamole-auth-jdbc-1.5.4.tar.gz -C ./
```

```
tar -zxvf guacamole-auth-totp-1.5.4.tar.gz -C ./
```

```
cp guacamole-auth-ldap-1.5.4/guacamole-auth-ldap-1.5.4.jar /etc/guacamole/extensions
```

```
cp guacamole-auth-jdbc-1.5.4/postgresql/guacamole-auth-jdbc-postgresql-1.5.4.jar /etc/guacamole/extensions
```

```
cp guacamole-auth-totp-1.5.4/guacamole-auth-totp-1.5.4.jar /etc/guacamole/extensions
```

## Install [PostgreSQL](https://www.postgresql.org/)
```
apt install postgresql
```

Download postgresql driver
```
wget -O postgresql-42.7.3.jar https://jdbc.postgresql.org/download/postgresql-42.7.3.jar
```

```
mkdir /etc/guacamole/lib
```

```
mv postgresql-42.7.3.jar /etc/guacamole/lib
```

### Create PostgreSQL Database
```
mkdir -p /var/lib/postgresql/guacamole
```

```
chown -R postgres:postgres /var/lib/postgresql/guacamole
```

```
cp -r guacamole-auth-jdbc-1.5.4/postgresql/schema /var/lib/postgresql/guacamole
```

```
sudo -u postgres -i
```

```
createdb guacamole
```

```
cat guacamole/schema/*.sql | psql -d guacamole -f -
```

```
psql -d guacamole
```

```
CREATE USER guacamole WITH PASSWORD 'xxx';
```

```
GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA public TO guacamole;
```

```
GRANT SELECT,USAGE ON ALL SEQUENCES IN SCHEMA public TO guacamole;
```

```
\q
```

```
exit
```

```
rm -r /var/lib/postgresql/guacamole
```

## Configure PostgreSQL and LDAP properties
```
vi /etc/guacamole/guacamole.properties
```

```
postgresql-hostname: localhost
postgresql-database: guacamole
postgresql-username: guacamole
postgresql-password: xxx

ldap-hostname:dc1.example.com
ldap-port:636
ldap-encryption-method:ssl
ldap-user-base-dn:ou=IT,dc=example,dc=com
ldap-config-base-dn:ou=IT,dc=example,dc=com
ldap-username-attribute:sAMAccountName
ldap-user-search-filter:(&(|(objectclass=person))(|(|(memberof=CN=VDI Users,OU=Users,OU=IT,DC=example,DC=com)(primaryGroupID=1121))))
ldap-search-bind-dn:cn=nextcloud,cn=Users,dc=example,dc=com
ldap-search-bind-password: xxx
```

## Clean install
```
rm -r guacamole-auth-*
```

## TLS ([Public Key Infrastructure](../pki/howto.md))
```
apt install wget
```

```
wget -O /usr/local/share/ca-certificates/domain.crt --no-check-certificate https://pki1.example.com/roots.pem
```

```
update-ca-certificates
```

```
sudo apt install certbot 
```

```
certbot certonly --standalone -d vdi1.example.com --server https://pki1.example.com/acme/acme/directory
```

```
mkdir /etc/tomcat9/ssl
```

```
cd /etc/tomcat9/ssl
```

```
cp /etc/letsencrypt/live/vdi1.example.com/cert.pem ./
cp /etc/letsencrypt/live/vdi1.example.com/chain.pem ./
cp /etc/letsencrypt/live/vdi1.example.com/privkey.pem ./
```

```
chown tomcat *.pem
```

```
vi /etc/tomcat9/server.xml
```

```
<Connector port="8443" protocol="org.apache.coyote.http11.Http11NioProtocol"
            maxThreads="150" SSLEnabled="true">
    <SSLHostConfig>
        <Certificate certificateFile="conf/ssl/cert.pem"
                certificateKeyFile="conf/ssl/privkey.pem"
                certificateChainFile="conf/ssl/chain.pem" />
    </SSLHostConfig>
</Connector>
```

```
systemctl start tomcat9
```

# Redirect
```
apt install iptables
```

```
iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 8443
```

```
apt install iptables-persistent
```


# First connection

https://vdi1.example.com

```
User: guacadmin
Password: guacadmin
```

# Connection Variables
```
${GUAC_USERNAME}
```

```
${GUAC_PASSWORD}
```