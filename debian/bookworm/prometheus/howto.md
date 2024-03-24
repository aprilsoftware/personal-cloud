# [Prometeus](https://prometheus.io/)
## On the server
```
apt install prometheus prometheus-node-exporter
```

```
systemctl enable prometheus prometheus-node-exporter
```

URL:
```
http://mon1.example.com:9090
```

## On the clients
```
apt install prometheus-node-exporter
```

```
systemctl enable prometheus-node-exporter
```

Optional

```
apt install prometheus-libvirt-exporter
```

# [Grafana](https://grafana.com)
```
apt install apt-transport-https software-properties-common wget
```

```
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
```

```
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
```

```
apt update
```

```
apt install grafana
```

```
systemctl enable grafana-server
```

URL
```
http://mon1.example.com:3000/
```

## TLS ([Public Key Infrastructure](../pki/howto.md))
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
certbot certonly --standalone -d mon1.example.com --server https://pki1.example.com/acme/acme/directory
```

```
chmod 444 /etc/letsencrypt/archive/mon1.example.com/privkey1.pem
```

```
chmod 444 /etc/letsencrypt/archive/mon1.example.com/fullchain1.pem
```

```
ln -s /etc/letsencrypt/live/mon1.example.com/privkey.pem /etc/grafana/grafana.key
```

```
ln -s /etc/letsencrypt/live/mon1.example.com/fullchain.pem /etc/grafana/grafana.crt
```

```
chgrp -R grafana /etc/letsencrypt/*
```

```
chmod -R g+rx /etc/letsencrypt/*
```

```
chgrp -R grafana /etc/grafana/grafana.crt /etc/grafana/grafana.key
```

```
chmod 400 /etc/grafana/grafana.crt /etc/grafana/grafana.key
```

```
vi /etc/grafana/grafana.ini
```

```
domain = example.com
protocol = https
cert_file = /etc/grafana/grafana.crt
cert_key = /etc/grafana/grafana.key
```

```
apt install iptables
```

```
iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 3000
```

```
apt install iptables-persistent
```

```
systemctl restart grafana-server
```

## [Dashboards](https://grafana.com/grafana/dashboards/)
- [Node Exporter Full](https://grafana.com/grafana/dashboards/1860-node-exporter-full/)





