# Install Postfix

## Certificate
```
apt install certbot
```

```
certbot certonly --standalone -d mail1.example.com
```

```
/etc/letsencrypt/live/mail1.example.com/cert.pem
/etc/letsencrypt/live/mail1.example.com/chain.pem
/etc/letsencrypt/live/mail1.example.com/fullchain.pem
/etc/letsencrypt/live/mail1.example.com/privkey.pem
```

## Postfix

```
apt install postfix
```

General type of mail configuration
```
Internet Site
```

System mail name
```
example.com
```

## LDAP
```
apt install postfix-ldap
```

## Edit config files
[Edit /etc/postfix/main.cf](https://github.com/aprilsoftware/personal-cloud/blob/main/debian/bullseye/email/postfix/main.cf)

[Edit /etc/postfix/master.cf](https://github.com/aprilsoftware/personal-cloud/blob/main/debian/bullseye/email/postfix/master.cf)

[Edit /etc/postfix/vmail/example_com_aliases.cf](https://github.com/aprilsoftware/personal-cloud/blob/main/debian/bullseye/email/postfix/vmail/example_com_aliases.cf)

[Edit /etc/postfix/vmail/example_com_auth.cf](https://github.com/aprilsoftware/personal-cloud/blob/main/debian/bullseye/email/postfix/vmail/example_com_auth.cf)

[Edit /etc/postfix/vmail/example_com_mailboxes.cf](https://github.com/aprilsoftware/personal-cloud/blob/main/debian/bullseye/email/postfix/vmail/example_com_mailboxes.cf)

## vmail

```
groupadd -g 5000 vmail
```

```
useradd -m -u 5000 -g 5000 -s /bin/false vmail
```

```
postmap -q user@example.com ldap:/etc/postfix/vmail/example_com_aliases.cf
```

# Install Dovecot
```
apt install dovecot-core dovecot-imapd dovecot-lmtpd
```

```
vi /etc/dovecot/dovecot.conf
```

```
haproxy_trusted_networks = 192.168.0.100
haproxy_timeout = 3s
```

```
vi /etc/dovecot/conf.d/10-auth.conf
```

```
disable_plaintext_auth = yes
auth_mechanisms = plain login
```

```
vi /etc/dovecot/conf.d/10-mail.conf
```

```
mail_location = maildir:~/
mail_privileged_group = vmail
```

```
vi /etc/dovecot/conf.d/10-master.conf
```

```
service imap-login {
  inet_listener imap {
    port = 143
  }
  inet_listener imaps {
    port = 993
    ssl = yes
  }

  inet_listener imap_haproxy {
    port = 10143
    haproxy = yes
  }
  inet_listener imaps_haproxy {
    port = 10993
    ssl = yes
    haproxy = yes
  }

service auth {
  # Postfix smtp-auth
  unix_listener /var/spool/postfix/private/auth {
    mode = 0660
    user = postfix
    group = postfix  
  }
}

service lmtp {
  unix_listener /var/spool/postfix/private/dovecot-lmtp {
    mode = 0600
    user = postfix
    group = postfix
  }
}
```

```
vi /etc/dovecot/conf.d/10-ssl.conf
```

```
ssl = required

ssl_cert = </etc/letsencrypt/live/mail1.example.com/fullchain.pem
ssl_key = </etc/letsencrypt/live/mail1.example.com/privkey.pem

ssl_prefer_server_ciphers = yes
ssl_min_protocol = TLSv1.2
```

```
adduser dovecot vmail
```

## Check ports
```
ss -lnpt | grep dovecot
```

## LDAP Dovecot
```
apt install dovecot-ldap
```

[Edit /etc/dovecot/conf.d/auth-ldap.conf.ext](https://github.com/aprilsoftware/personal-cloud/blob/main/debian/bullseye/email/dovecot/auth-ldap.conf.ext)

[Edit /etc/dovecot/dovecot-ldap.conf.ext](https://github.com/aprilsoftware/personal-cloud/blob/main/debian/bullseye/email/dovecot/dovecot-ldap.conf.ext)

```
vi /etc/dovecot/conf.d/10-auth.conf
```

```
#!include auth-system.conf.ext
!include auth-ldap.conf.ext
```

## Test
```
doveadm auth test user@example.com xxx
```

```
doveadm user user@example.com
```

# HAProxy
[Edit /etc/haproxy/haproxy.cfg](https://github.com/aprilsoftware/personal-cloud/blob/main/debian/bullseye/email/haproxy/haproxy.cfg)

# SPF
Add DNS entry

```
example.com. 900 TXT "v=spf1 mx ~all"
```

```
apt install postfix-policyd-spf-python
```

```
vi /etc/postfix/master.cf
```

```
policyd-spf  unix  -       n       n       -       0       spawn
    user=policyd-spf argv=/usr/bin/policyd-spf
```

```
vi /etc/postfix/main.cf
```

```
policyd-spf_time_limit = 3600
smtpd_recipient_restrictions =
   permit_mynetworks,
   permit_sasl_authenticated,
   reject_unauth_destination,
   check_policy_service unix:private/policyd-spf
```

# DKIM
```
apt install opendkim opendkim-tools
```

```
gpasswd -a postfix opendkim
```

```
vi /etc/opendkim.conf
```

```
Logwhy			yes

Mode			sv
SubDomains		no

AutoRestart		yes
AutoRestartRate		10/1M
Background		yes
DNSTimeout		5
SignatureAlgorithm	rsa-sha256

KeyTable		refile:/etc/opendkim/key.table
SigningTable		refile:/etc/opendkim/signing.table
InternalHosts		refile:/etc/opendkim/trusted.hosts
ExternalIgnoreList	refile:/etc/opendkim/trusted.hosts
```

```
mkdir /etc/opendkim
mkdir /etc/opendkim/keys
chown -R opendkim:opendkim /etc/opendkim
chmod go-rw /etc/opendkim/keys
```

```
vi /etc/opendkim/signing.table
```

```
*@example.com    default._domainkey.example.com
*@*.example.com    default._domainkey.example.com
```

```
vi /etc/opendkim/key.table
```

```
default._domainkey.example.com     example.com:default:/etc/opendkim/keys/example.com/default.private
```

```
vi /etc/opendkim/trusted.hosts
```

```
127.0.0.1
localhost

.example.com
```

```
mkdir /etc/opendkim/keys/example.com
```

```
opendkim-genkey -b 2048 -d example.com -D /etc/opendkim/keys/example.com -s default -v
```

```
chown opendkim:opendkim /etc/opendkim/keys/example.com/default.private
```

```
chmod 600 /etc/opendkim/keys/example.com/default.private
```

Publish key

```
cat /etc/opendkim/keys/example.com/default.txt
```

Concatenate all removing spaces and keeping only begining and closing quotes

## DNS
```
default._domainkey 900 TXT "v=DKIM1; h=sha256; k=rsa;p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2nHrFtenqI8rKZg2r+Nybi3wzMPA4OvQSQlAIPUZnZZvS4PBpe02geOsq0EkJqXvQ07yPSabONX42U4h8ZGxSuN5EStupIiDc7BbuAEzPxF3fl2tS4sdbKYK5V20kKJacbYjLJOv62Cwm1QkxNsxpk9BeNKTVnLzb/3Q6Dj5v3V/RjQt5YEm8dRStVKik20qLEIr9lO5y7bCg2N2JoBUHnZ6Boaji1D/Ixr3NFwW4MouIjdsHKHWoBcNnxZrwHpAg3tuU6/NjqEOzNpOLKHyIqGI04nn3RMUoouYTzxM/EZvrh8NqANUajUedGhe+N78qPYCSUqxS5DvMjQbM2uI+wIDAQAB"
```

## Connect to postfix
```
mkdir /var/spool/postfix/opendkim
```

```
chown opendkim:postfix /var/spool/postfix/opendkim
```

```
vi /etc/opendkim.conf
```

```
#Socket                 local:/run/opendkim/opendkim.sock
#Socket                 inet:8891@localhost
#Socket                 inet:8891
Socket                  local:/var/spool/postfix/opendkim/opendkim.sock
```

```
vi /etc/default/opendkim
```

```
#SOCKET=local:$RUNDIR/opendkim.sock
SOCKET=local:/var/spool/postfix/opendkim/opendkim.sock
```

```
vi /etc/postfix/main.cf
```

```
milter_default_action = accept
milter_protocol = 6
smtpd_milters = local:opendkim/opendkim.sock
non_smtpd_milters = $smtpd_milters
```

# DMARC
Add DNS entry
```
 _dmarc.example.com 900 TXT "v=DMARC1; p=none"
```

```
apt install opendmarc
```

Choose No to the question "Configure database for opendmarc with dbconfig-common"

```
systemctl enable opendmarc
 ```

```
vi /etc/opendmarc.conf
```

```
AuthservID OpenDMARC
RejectFailures true
TrustedAuthservIDs mail1.example.com
IgnoreAuthenticatedClients true
RequiredHeaders true
SPFSelfValidate true
Socket local:/var/spool/postfix/opendmarc/opendmarc.sock
```

```
mkdir -p /var/spool/postfix/opendmarc
chown opendmarc:opendmarc /var/spool/postfix/opendmarc -R
chmod 750 /var/spool/postfix/opendmarc/ -R
adduser postfix opendmarc
 ```

```
systemctl restart opendmarc
```

```
vi /etc/postfix/main.cf
```

```
milter_default_action = accept
milter_protocol = 6
smtpd_milters = local:opendkim/opendkim.sock,local:opendmarc/opendmarc.sock
non_smtpd_milters = $smtpd_milters
```

# SpamAssassin
```
apt install spamassassin spamc
```

```
systemctl enable spamassassin
```

```
systemctl start spamassassin
```

```
apt install spamass-milter
```

```
vi /etc/postfix/main.cf
```

```
milter_default_action = accept
milter_protocol = 6
smtpd_milters = local:opendkim/opendkim.sock,local:opendmarc/opendmarc.sock,local:spamass/spamass.sock
non_smtpd_milters = $smtpd_milters
```

```
vi /etc/default/spamass-milter
```

```
OPTIONS="${OPTIONS} -r 8"
```

```
systemctl restart postfix spamass-milter
```

```
vi /etc/default/spamassassin
```

```
CRON=1
```

# Move spam to junk
```
apt install dovecot-sieve
```

```
vi /etc/dovecot/conf.d/15-lda.conf
```

```
protocol lda {
    # Space separated list of plugins to load (default is global mail_plugins).
    mail_plugins = $mail_plugins sieve
}
```

```
vi /etc/dovecot/conf.d/20-lmtp.conf
```

```
protocol lmtp {
      mail_plugins = quota sieve
}
```

```
vi /etc/dovecot/conf.d/10-mail.conf
```

```
mail_home = /home/vmail/%d/%n/
```

```
vi /etc/dovecot/conf.d/90-sieve.conf
```

```
sieve_before = /etc/dovecot/SpamToJunk.sieve
```

```
vi /etc/dovecot/SpamToJunk.sieve
```

```
require "fileinto";

if header :contains "X-Spam-Flag" "YES"
{
   fileinto "Junk";
   stop;
}
```

```
sievec /etc/dovecot/SpamToJunk.sieve
```

```
systemctl restart dovecot
```

```
vi /etc/default/spamass-milter
```

```
#Spamc options
OPTIONS="${OPTIONS} -- --max-size=5120000"
```

# Restart
```
systemctl restart postfix
```

```
systemctl restart dovecot
```

```
systemctl restart spamass-milter
```

# Test email
https://www.mail-tester.com