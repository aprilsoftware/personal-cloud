# Cluster

> Debian Bookworm
>
> node1.local | node1.example.com | 192.168.0.50
>
> node2.local | node2.example.com | 192.168.0.51
>
> node3.local | node3.example.com | 192.168.0.52

***Repeate the procedure for each node***

## Networks

```
apt install avahi-daemon
```

```
vi /etc/network/interfaces
```

Add

```
iface enp9s0f0 inet static  
address 192.168.0.50  
netmask 255.255.255.0  
gateway 192.168.0.1

allow-hotplug enp9s0f1  
iface enp9s0f1 inet manual

allow-hotplug enp7s0  
iface enp7s0 inet manual

allow-hotplug enp8s0  
iface enp8s0 inet manual
```

## libvirt

```
apt install qemu-system libvirt-daemon-system
```


```
vi /etc/libvirt/qemu.conf
```

update

> security_driver = "none"

## admin

```
mkdir -p /home/admin
```

```
useradd -d /home/admin -s /bin/bash admin ; echo 'admin:your password' | chpasswd
```

```
chown admin:admin /home/admin
```

```
adduser admin sudo
```

```
adduser admin libvirt
```

```
adduser admin libvirt-qemu
```

```
passwd admin
```

## Firmware & Tools

```
apt install firmware-realtek
```

```
apt install firmware-linux
```

```
apt install iotop htop
```

## Prometheus

```
apt install prometheus-node-exporter
```

```
systemctl enable prometheus-node-exporter
```

```
apt install prometheus-libvirt-exporter
```

## xfs

```
apt install xfsprogs
```

## Disk Encryption

```
apt install clevis clevis-luks clevis-systemd
```

```
systemctl enable clevis-luks-askpass.path
```

```
reboot
```

## gv0/brick1

```
cryptsetup luksFormat /dev/nvme1n1
```

**Use a different passphrase than the definitive one**

```
cryptsetup luksOpen /dev/nvme1n1 nvme1n1_crypt
```

```
dd if=/dev/zero of=/dev/mapper/nvme1n1_crypt bs=128M status=progress
```

```
cryptsetup luksClose nvme1n1_crypt
```

```
dd if=/dev/urandom of=/dev/nvme1n1 bs=512 count=20480 status=progress
```

```
cryptsetup luksFormat /dev/nvme1n1
```

**Use the definitive passphrase**

```
cryptsetup luksOpen /dev/nvme1n1 nvme1n1_crypt
```

```
vgcreate gv0_brick1 /dev/mapper/nvme1n1_crypt
```

```
lvcreate --thinpool gv0_brick1/brick1_pool --size 1.78T --chunksize 256K --poolmetadatasize 16G --zero n
```

```
lvcreate --thin --name brick1 --virtualsize 1.78T gv0_brick1/brick1_pool
```

```
mkfs.xfs -i size=512 -n size=8192 /dev/mapper/gv0_brick1-brick1
```

```
mkdir -p /data/glusterfs/gv0/brick1
```

```
echo "nvme1n1_crypt /dev/nvme1n1 none luks,discard"  >> /etc/crypttab
```

```
echo "/dev/mapper/gv0_brick1-brick1 /data/glusterfs/gv0/brick1 xfs _netdev,inode64,noatime 0 0"  >> /etc/fstab
```

```
clevis luks bind -d /dev/nvme1n1 tang '{"url":"http://192.168.0.2"}'
```

## gv1/brick1

```
cryptsetup luksFormat /dev/sda
```

**Use a different passphrase than the definitive one**

```
cryptsetup luksOpen /dev/sda sda_crypt
```

```
dd if=/dev/zero of=/dev/mapper/sda_crypt bs=128M status=progress
```

```
cryptsetup luksClose sda_crypt
```

```
dd if=/dev/urandom of=/dev/sda bs=512 count=20480 status=progress
```

```
cryptsetup luksFormat /dev/sda
```

**Use the definitive passphrase**

```
cryptsetup luksOpen /dev/sda sda_crypt
```

```
vgcreate gv1_brick1 /dev/mapper/sda_crypt
```

```
lvcreate --thinpool gv1_brick1/brick1_pool --size 3.60T --chunksize 256K --poolmetadatasize 16G --zero n
```

```
lvcreate --thin --name brick1 --virtualsize 3.60T gv1_brick1/brick1_pool
```

```
mkfs.xfs -i size=512 -n size=8192 /dev/mapper/gv1_brick1-brick1
```

```
mkdir -p /data/glusterfs/gv1/brick1
```

```
echo "sda_crypt /dev/sda none luks,discard"  >> /etc/crypttab
```

```
echo "/dev/mapper/gv1_brick1-brick1 /data/glusterfs/gv1/brick1 xfs _netdev,inode64,noatime 0 0"  >> /etc/fstab
```

```
clevis luks bind -d /dev/sda tang '{"url":"http://192.168.0.2"}'
```

## gv1/brick2

```
cryptsetup luksFormat /dev/sdb
```

**Use a different passphrase than the definitive one**

```
cryptsetup luksOpen /dev/sdb sdb_crypt
```

```
dd if=/dev/zero of=/dev/mapper/sdb_crypt bs=128M status=progress
```

```
cryptsetup luksClose sdb_crypt
```

```
dd if=/dev/urandom of=/dev/sdb bs=512 count=20480 status=progress
```

```
cryptsetup luksFormat /dev/sdb
```

**Use the definitive passphrase**

```
cryptsetup luksOpen /dev/sdb sdb_crypt
```

```
vgcreate gv1_brick2 /dev/mapper/sdb_crypt
```

```
lvcreate --thinpool gv1_brick2/brick2_pool --size 3.60T --chunksize 256K --poolmetadatasize 16G --zero n
```

```
lvcreate --thin --name brick2 --virtualsize 3.60T gv1_brick2/brick2_pool
```

```
mkfs.xfs -i size=512 -n size=8192 /dev/mapper/gv1_brick2-brick2
```

```
mkdir -p /data/glusterfs/gv1/brick2
```

```
echo "sdb_crypt /dev/sdb none luks,discard"  >> /etc/crypttab
```

```
echo "/dev/mapper/gv1_brick2-brick2 /data/glusterfs/gv1/brick2 xfs _netdev,inode64,noatime 0 0"  >> /etc/fstab
```

```
clevis luks bind -d /dev/sdb tang '{"url":"http://192.168.0.2"}'
```

## bmv0

```
cryptsetup luksFormat /dev/sdc
```

**Use a different passphrase than the definitive one**

```
cryptsetup luksOpen /dev/sdc sdc_crypt
```

```
dd if=/dev/zero of=/dev/mapper/sdc_crypt bs=128M status=progress
```

```
cryptsetup luksClose sdc_crypt
```

```
dd if=/dev/urandom of=/dev/sdc bs=512 count=20480 status=progress
```

```
cryptsetup luksFormat /dev/sdc
```

**Use the definitive passphrase**

```
cryptsetup luksOpen /dev/sdc sdc_crypt
```

```
vgcreate bmvg0 /dev/mapper/sdc_crypt
```

```
lvcreate -L 3.62T -n bmv0 bmvg0
```

```
mkfs.xfs /dev/mapper/bmvg0-bmv0
```

```
mkdir -p /mnt/bmv0 
```

```
echo "sdc_crypt /dev/sdc none luks,discard"  >> /etc/crypttab
```

```
echo "/dev/mapper/bmvg0-bmv0 /mnt/bmv0 xfs _netdev,inode64,noatime 0 0"  >> /etc/fstab 
```

```
clevis luks bind -d /dev/sdc tang '{"url":"http://192.168.0.2"}'
```

## Hosts

Add all hosts in /etc/hosts file

```
192.168.0.50   node1.local    node1
192.168.0.51   node2.local    node2
192.168.0.52   node3.local    node3
```

## GlusterFS

```
apt-get install ntp
```

```
apt-get install glusterfs-server
```

```
systemctl enable glusterd
```

```
systemctl start glusterd
```

```
gluster peer probe node2.local
```

```
gluster peer probe node3.local
```

```
gluster volume create gv0 replica 3 node{1..3}.local:/data/glusterfs/gv0/brick1/brick
```

```
gluster volume create gv1 replica 3 node{1..3}.local:/data/glusterfs/gv1/brick1/brick node{1..3}.local:/data/glusterfs/gv1/brick2/brick
```

```
gluster volume start gv0
```

```
gluster volume start gv1
```

```
mkdir /mnt/gv0
```

```
mkdir /mnt/gv1
```

```
echo "node1.local:/gv0 /mnt/gv0 glusterfs defaults,noatime,_netdev 0 0"  >> /etc/fstab
```

```
echo "node1.local:/gv1 /mnt/gv1 glusterfs defaults,noatime,_netdev 0 0"  >> /etc/fstab
```

## TLS

```
cd /etc/ssl/
```

```
openssl genrsa -out glusterfs.key 2048
```

```
openssl req -new -x509 -days 3650 -key glusterfs.key -subj "/CN=node1.local" -out glusterfs.pem
```

```
openssl req -new -x509 -days 3650 -key glusterfs.key -subj "/CN=node2.local" -out glusterfs.pem
```

```
openssl req -new -x509 -days 3650 -key glusterfs.key -subj "/CN=node3.local" -out glusterfs.pem
```

```
mkdir -p /mnt/gv0/certificates
```

```
cp glusterfs.pem /mnt/gv0/certificates/node1.local.pem
```

```
cp glusterfs.pem /mnt/gv0/certificates/node2.local.pem
```

```
cp glusterfs.pem /mnt/gv0/certificates/node3.local.pem
```

```
cd /mnt/gv0/certificates
```

```
cat node1.local.pem node2.local.pem node3.local.pem > glusterfs.ca
```

```
cd /etc/ssl
```

```
cp /mnt/gv0/certificates/glusterfs.ca ./
```

```
chmod 644 glusterfs.key
```

```
cd /usr/lib/ssl
```

```
ln -s /etc/ssl/glusterfs.pem glusterfs.pem
```

```
ln -s /etc/ssl/glusterfs.ca glusterfs.ca
```

```
ln -s /etc/ssl/glusterfs.key glusterfs.key
```

```
echo "option transport.socket.ssl-cert-depth 1" >  /var/lib/glusterd/secure-access
```

```
gluster volume stop gv0
```

```
gluster volume stop gv1
```

```
volume set gv0 auth.ssl-allow node1.local,node2.local,node3.local
```

```
volume set gv1 auth.ssl-allow node1.local,node2.local,node3.local
```

```
volume set gv0 client.ssl on
```

```
volume set gv1 client.ssl on
```

```
volume set gv0 server.ssl on
```

```
volume set gv1 server.ssl on
```

```
vi /etc/glusterfs/glusterd.vol
```
Add
> 
>
> option rpc-auth-allow-insecure on

```
gluster volume set gv0 server.allow-insecure on
```

```
gluster volume set gv1 server.allow-insecure on
```

```
gluster volume set gv0 storage.owner-uid 64055
```

```
gluster volume set gv0 storage.owner-gid 64055
```

```
gluster volume set gv1 storage.owner-uid 64055
```

```
gluster volume set gv1 storage.owner-gid 64055
```

```
gluster volume set gv0 features.shard enable
```

```
gluster volume set gv1 features.shard enable
```

```
reboot
```

```
volume start gv0
```

```
volume start gv1
```

## SDN

```
apt install openvswitch-switch
```

```
ovs-vsctl add-br br0
```

```
ovs-vsctl add-port br0 enp9s0f1
```

```
ovs-vsctl add-br wan0
```

```
ovs-vsctl add-port wan0 enp7s0
```

```
ovs-vsctl add-br wan1
```

```
ovs-vsctl add-port wan1 enp8s0
```

```
ovs-vsctl add-br lab1-2 br0 2
```


```
cd /etc/libvirt/qemu/networks
```

```
vi br0.xml
```

    <network>
      <name>br0</name>
      <forward mode='bridge'/>
      <bridge name='br0'/>
      <virtualport type='openvswitch'/>
    </network>

```
virsh net-define br0.xml
```

```
virsh net-start br0
```

```
virsh net-autostart br0
```

```
vi lab1-2.xml
```

    <network>
      <name>lab1-2</name>
      <forward mode='bridge'/>
      <bridge name='lab1-2'/>
      <virtualport type='openvswitch'/>
    </network>

```
virsh net-define lab1-2.xml
```

```
virsh net-start lab1-2
```

```
virsh net-autostart lab1-2
```



    <network>
      <name>wan0</name>
      <forward mode='bridge'/>
      <bridge name='wan0'/>
      <virtualport type='openvswitch'/>
    </network>

```
virsh net-define wan0.xml
```

```
virsh net-start wan0
```

```
virsh net-autostart wan0
```

## VM Migration

> as root from each node

```
ssh-keygen
```

```
ssh-copy-id admin@node1.local
```

```
ssh-copy-id admin@node2.local
```

```
ssh-copy-id admin@node3.local
```

## Folder Structure

```
mkdir /mnt/bmv0/vm
```

```
mkdir /mnt/gv0/vm
```

```
mkdir /mnt/gv1/vm
```

```
mkdir /mnt/gv1/iso
```

```
mkdir /mnt/snapshots
```

```
cd /mnt
```

```
chown -R libvirt-qemu:libvirt-qemu gv0 gv1 bmv0
```

```
chmod 770 gv0 gv1 bmv0
```

```
chmod 770 /mnt/bmv0/vm /mnt/gv0/vm /mnt/gv1/vm /mnt/gv1/iso
```