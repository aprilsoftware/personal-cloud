# [Wireguard](https://www.wireguard.com/) as a gateway
## On the gateway side
```
apt install wireguard
```

```
cd /etc/wireguard
```

```
umask 077; wg genkey | tee privatekey | wg pubkey > publickey
```

```
vi /etc/wireguard/wg0.conf
```

```
[Interface]
Address = 10.8.0.1/24
SaveConfig = true
ListenPort = 51820
PrivateKey = ...

[Peer]
PublicKey = ...
AllowedIPs = 10.8.0.0/24, 192.168.2.0/24
```

```
vi /etc/sysctl.conf
```

```
net.ipv4.ip_forward=1
```

```
systemctl enable wg-quick@wg0
```

```
systemctl start wg-quick@wg0
```

```
apt install iptables
```

```
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

```
apt install iptables-persistent
```

## On the client side
```
apt install wireguard
```

```
sh -c 'umask 077; touch /etc/wireguard/wg0.conf'
```

```
cd /etc/wireguard
```

```
umask 077; wg genkey | tee privatekey | wg pubkey > publickey
```

```
nano /etc/wireguard/wg0.conf
```

```
[Interface]
PrivateKey = 
Address = 10.8.0.2/24
PreUp = ip route add 192.168.0.0/24 via 192.168.2.1
PostDown = ip route del 192.168.0.0/24 via 192.168.2.1

[Peer]
PublicKey = 
AllowedIPs = 0.0.0.0/0
Endpoint = 3.124.204.47:51820
PersistentKeepalive = 20
```

```
systemctl enable wg-quick@wg0
```

```
systemctl start wg-quick@wg0
```

```
vi /etc/sysctl.conf
```

```
net.ipv4.ip_forward=1
```

```
apt install iptables
```

```
iptables -A FORWARD -i eth0 -j ACCEPT
```

```
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

Limit forward
```
iptables -P FORWARD DROP
iptables -A FORWARD -d 192.168.0.101 -j ACCEPT
iptables -A FORWARD -d 192.168.0.102 -j ACCEPT
```

```
apt install iptables-persistent
```