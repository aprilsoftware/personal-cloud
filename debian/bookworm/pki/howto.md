# Public Key Infrastructure - ([step-certificate](https://github.com/smallstep/certificates))
```
apt install wget
```

```
wget https://dl.smallstep.com/cli/docs-ca-install/latest/step-cli_amd64.deb
```

```
wget https://dl.smallstep.com/certificates/docs-ca-install/latest/step-ca_amd64.deb
```

```
sudo dpkg -i step-cli_amd64.deb
```

```
sudo dpkg -i step-ca_amd64.deb
```

# CA init
```
step ca init
```

```
vi /root/.step/password.txt
```

```
ca-password
```

```
step ca provisioner add acme --type ACME
```

```
step-ca $(step path)/config/ca.json
```


# Run as a service
```
useradd --user-group --system --home /etc/step-ca --shell /bin/false step
```

```
setcap CAP_NET_BIND_SERVICE=+eip $(which step-ca)
```

```
mkdir -p /etc/step-ca
```

```
mv $(step path)/* /etc/step-ca
```

```
chown -R step:step /etc/step-ca
```

```
apt install jq
```

```
cat <<< $(jq '.root = "/etc/step-ca/certs/root_ca.crt"' /etc/step-ca/config/ca.json) > /etc/step-ca/config/ca.json
```

```
cat <<< $(jq '.crt = "/etc/step-ca/certs/intermediate_ca.crt"' /etc/step-ca/config/ca.json) > /etc/step-ca/config/ca.json
```

```
cat <<< $(jq '.key = "/etc/step-ca/secrets/intermediate_ca_key"' /etc/step-ca/config/ca.json) > /etc/step-ca/config/ca.json
```

```
cat <<< $(jq '.db.dataSource = "/etc/step-ca/db"' /etc/step-ca/config/ca.json) > /etc/step-ca/config/ca.json
```



```
vi /etc/systemd/system/step-ca.service
```

```
[Unit]
Description=step-ca service
Documentation=https://smallstep.com/docs/step-ca
Documentation=https://smallstep.com/docs/step-ca/certificate-authority-server-production
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=30
StartLimitBurst=3
ConditionFileNotEmpty=/etc/step-ca/config/ca.json
ConditionFileNotEmpty=/etc/step-ca/password.txt

[Service]
Type=simple
User=step
Group=step
Environment=STEPPATH=/etc/step-ca
WorkingDirectory=/etc/step-ca
ExecStart=/usr/bin/step-ca config/ca.json --password-file password.txt
ExecReload=/bin/kill --signal HUP $MAINPID
Restart=on-failure
RestartSec=5
TimeoutStopSec=30
StartLimitInterval=30
StartLimitBurst=3

; Process capabilities & privileges
AmbientCapabilities=CAP_NET_BIND_SERVICE
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
SecureBits=keep-caps
NoNewPrivileges=yes

; Sandboxing
ProtectSystem=full
ProtectHome=true
RestrictNamespaces=true
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
PrivateTmp=true
PrivateDevices=true
ProtectClock=true
ProtectControlGroups=true
ProtectKernelTunables=true
ProtectKernelLogs=true
ProtectKernelModules=true
LockPersonality=true
RestrictSUIDSGID=true
RemoveIPC=true
RestrictRealtime=true
SystemCallFilter=@system-service
SystemCallArchitectures=native
MemoryDenyWriteExecute=true
ReadWriteDirectories=/etc/step-ca/db

[Install]
WantedBy=multi-user.target
```

```
systemctl enable step-ca
```

```
systemctl start step-ca
```

# On the client side
copy root_ca.crt to /usr/local/share/ca-certificates

```
sudo cp root_ca.crt /usr/local/share/ca-certificates
```

```
sudo update-ca-certificates
```

```
apt install certbot
```

```
certbot certonly --standalone -d test1.example.com --server https://pki1.example.com/acme/acme/directory
```

# Renew certificates
```
certbot renew
```