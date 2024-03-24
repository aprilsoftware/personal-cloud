# Install [Samba](https://www.samba.org/) as an Active Directory

```
apt install samba krb5-config winbind smbclient ntp
```

```
Default Kerberos version 5 realm
EXAMPLE.COM
Kerberos servers for your realm
DC1.EXAMPLE.COM
Administrative server for your Kerberos realm
DC1.EXAMPLE.COM
```

```
mv /etc/samba/smb.conf /etc/samba/smb.conf.org
```

```
samba-tool domain provision
```

```
cp /var/lib/samba/private/krb5.conf /etc/
```

```
systemctl stop smbd nmbd winbind
```

```
systemctl disable smbd nmbd winbind
```

```
systemctl unmask samba-ad-dc
```

```
systemctl start samba-ad-dc
```

```
systemctl enable samba-ad-dc
```

## Create user
```
samba-tool user create username
```

## DNS
```
vi /etc/resolv.conf
```

```
nameserver 192.168.0.101
```

```
samba-tool dns zonecreate example.com 0.168.192.in-addr.arpa -U Administrator
```

```
samba-tool dns add 192.168.0.101 8.168.192.in-addr.arpa 1 PTR dc1.example.com -U Administrator
```

```
systemctl stop samba-ad-dc
```

```
systemctl start samba-ad-dc
```


# Optional Feature for Windows 11

## TLS ([Public Key Infrastructure](../pki/howto.md))
192.168.0.102 being the IP of pki1.example.com
```
samba-tool dns add dc1.example.com example.com pki1 A 192.168.0.102 -U Administrator
```

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
apt install certbot
```

```
certbot certonly --standalone -d dc1.example.com --server https://pki1.example.com/acme/acme/directory
```

```
vi /etc/samba/smb.conf
```

Section [global]

```
workgroup = YOUR DOMAIN
tls enabled  = yes
tls keyfile  = /etc/letsencrypt/live/dc1.example.com/privkey.pem
tls certfile = /etc/letsencrypt/live/dc1.example.com/fullchain.pem
tls cafile   = 
```

```
systemctl stop samba-ad-dc
```

```
systemctl start samba-ad-dc
```

## Secure samba

```
vi /etc/samba/smb.conf
```

Section [global]

```
...

ntlm auth = mschapv2-and-ntlmv2-only
disable netbios = yes
smb ports = 445
 
printcap name = /dev/null
load printers = no
disable spoolss = yes
printing = bsd

...
```

```
systemctl stop samba-ad-dc
```

```
systemctl start samba-ad-dc
```

# Debian join domain

```
vi /etc/resolv.conf
```

```
apt -y install realmd sssd sssd-tools libnss-sss libpam-sss adcli samba-common-bin oddjob oddjob-mkhomedir packagekit 
```

```
vi  /etc/pam.d/common-session
```

```
session optional        pam_mkhomedir.so skel=/etc/skel umask=077
```

```
apt install sssd realmd 
```

```
realm join --user=administrator example.com
```

```
vi /etc/sssd/sssd.conf
```

Change

```
use_fully_qualified_names = False
```

Remove

```
services = nss, pam
```

Add to avoid Forcing GPO even if the file does not exist

```
ad_gpo_access_control = permissive
```


## Test
```
id username@example.com
```

```
getent passwd username@example.com
```

## Reset Administrator password
```
samba-tool user setpassword Administrator
```

