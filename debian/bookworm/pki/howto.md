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

# Run manually
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
step-ca $(step path)/config/ca.json
```

# Run as a service
```
useradd --system --home /usr/local/step --shell /bin/bash step
```

```
setcap CAP_NET_BIND_SERVICE=+eip $(which step-ca)
```

```
mkdir -p /usr/local/step
```

```
chown -R step:step /usr/local/step
```

```
su step
```

```
step ca init
```

```
step ca provisioner add acme --type ACME
```

```
vi /usr/local/step/.step/password.txt
```

```
ca-password
```

```
exit
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
ConditionFileNotEmpty=/usr/local/step/.step/config/ca.json
ConditionFileNotEmpty=/usr/local/step/.step/password.txt

[Service]
Type=simple
User=step
Group=step
Environment=STEPPATH=/usr/local/step/.step
WorkingDirectory=/usr/local/step/.step
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
ReadWriteDirectories=/usr/local/step/.step/db

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