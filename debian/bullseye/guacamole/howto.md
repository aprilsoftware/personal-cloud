# Install [Apache Guacamole](https://guacamole.apache.org/)
## Build Server
```
apt install build-essential
```

```
apt install libcairo2-dev libjpeg62-turbo-dev libjpeg-dev libpng-dev libtool-bin uuid-dev libossp-uuid-dev
```

```
apt install libavcodec-dev libavformat-dev libavutil-dev libswscale-dev
```

```
apt install freerdp2-dev libpango1.0-dev libssh2-1-dev libtelnet-dev libvncserver-dev libwebsockets-dev libpulse-dev
```

```
apt install libssl-dev libvorbis-dev libwebp-dev
```

```
apt install wget
```

```
wget -O guacamole-server-1.5.3.tar.gz https://apache.org/dyn/closer.lua/guacamole/1.5.3/source/guacamole-server-1.5.3.tar.gz?action=download
```

```
tar -xzf guacamole-server-1.5.3.tar.gz
```

```
cd guacamole-server-1.5.3
```

```
./configure --with-init-dir=/etc/init.d
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

## Build Client or download the WAR file
```
apt install openjdk-11-jdk-headless
```

```
apt install tomcat9
```

Build
```
apt install maven npm
```

```
wget -O guacamole-client-1.5.3.tar.gz https://apache.org/dyn/closer.lua/guacamole/1.5.3/source/guacamole-client-1.5.3.tar.gz?action=download
```

```
tar -xzf  guacamole-client-1.5.3.tar.gz
```

```
cd guacamole-client-1.5.3
```

```
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/
export OPENSSL_CONF=/dev/null
```

```
mvn package
```

```
cp guacamole/target/guacamole-client.1.5.3.war /var/lib/tomcat9/webapps
```

Or download WAR file
```
wget -O guacamole-1.5.3.war https://apache.org/dyn/closer.lua/guacamole/1.5.3/binary/guacamole-1.5.3.war?action=download
```

```
mv guacamole-1.5.3.war /var/lib/tomcat9/webapps
```

# Configuration
```
mkdir -p /etc/guacamole
```

```
touch /etc/guacamole/guacamole.properties
```

## User mapping example
```
echo -n "@Password" | md5sum
```

```
vi /etc/guacamole/user-mapping.xml
```

```
user-mapping>
  <authorize username="user" password="XXXX" encoding="md5">
        <connection name="vd1.example.com">
            <protocol>rdp</protocol>
            <param name="hostname">ws1.example.com</param>
            <param name="port">3389</param>
            <param name="username">user</param>
            <param name="domain">example</param>
            <param name="ignore-cert">true</param>
        </connection>
  </authorize>
</user-mapping>
```

## Extensions
Active Directory / LDAP
```
wget -O guacamole-auth-ldap-1.5.3.tar.gz https://apache.org/dyn/closer.lua/guacamole/1.5.3/binary/guacamole-auth-ldap-1.5.3.tar.gz?action=download
```

JDBC
```
wget -O guacamole-auth-jdbc-1.5.3.tar.gz https://apache.org/dyn/closer.lua/guacamole/1.5.3/binary/guacamole-auth-jdbc-1.5.3.tar.gz?action=download
```

[2FA](https://fr.wikipedia.org/wiki/Double_authentification)
```
wget -O guacamole-auth-totp-1.5.3.tar.gz https://apache.org/dyn/closer.lua/guacamole/1.5.3/binary/guacamole-auth-totp-1.5.3.tar.gz?action=download
```

```
mkdir /etc/guacamole/extensions
```

```
mv guacamole-auth-jdbc-postgresql-1.5.3.jar /etc/guacamole/extensions
mv guacamole-auth-ldap-1.5.3.jar /etc/guacamole/extensions
mv guacamole-auth-totp-1.5.3.jar /etc/guacamole/extensions
```

## [PostgreSQL](https://www.postgresql.org/)
```
apt install postgresql
```

Download postgresql driver
```
wget -O postgresql-42.5.4.jar https://jdbc.postgresql.org/download/postgresql-42.5.4.jar
```

```
mkdir /etc/guacamole/lib
```

```
mv postgresql-42.5.4.jar /etc/guacamole/lib
```

### Create DB
```
createdb guacamole
```

```
cat schema/*.sql | psql -d guacamole -f -
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
ldap-search-bind-password:xxx
```


# Connection Variables
```
${GUAC_USERNAME}
```

```
${GUAC_PASSWORD}
```

## TLS
```
sudo apt install certbot 
```

```
sudo certbot certonly --standalone -d vd1.example.com
```

```
mkdir /etc/tomcat9/ssl
```

```
cd /etc/tomcat9/ssl
```

```
cp /etc/letsencrypt/live/vd1.example.com/cert.pem ./
cp /etc/letsencrypt/live/vd1.example.com/chain.pem ./
cp /etc/letsencrypt/live/vd1.example.com/privkey.pem ./
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

