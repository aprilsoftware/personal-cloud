# Personal Cluster

We tried many options such as using Ceph when we designed our clusters and we end up with the following design. One key element in our selection was to remain independent of any commercial products. We strongly believe in free software and we had limited resources at the begining.

We wanted to have several features available from day one:
- [Hypervisor](https://en.wikipedia.org/wiki/Hypervisor)
- [Software-defined storage](https://fr.wikipedia.org/wiki/Software-defined_storage) & Scale out storage
- Disk Encryption
- [Software-defined networking](https://en.wikipedia.org/wiki/Software-defined_networking)
- [Data deduplication](https://en.wikipedia.org/wiki/Data_deduplication) backup
- Telemetry

## Hardware requirements

We identified a typical hardware requirements which could be tune on demand.

- 3 regular PC with at least 4 hard drives / SSD and 3 network interfaces
- 3 network switches
- a connection to internet

## Components
We selected the following components to fulfill our requirements:
- [KVM](https://www.linux-kvm.org/page/Main_Page) / [libvirt](https://libvirt.org/) / [virt-manager](https://virt-manager.org/)
- [GlusterFS](https://www.gluster.org/)
- [clevis](https://github.com/latchset/clevis)[luks](https://gitlab.com/cryptsetup/cryptsetup)
- [Open vSwitch](https://www.openvswitch.org/)
- [BorgBackup](https://www.borgbackup.org/)
- [Prometeus](https://prometheus.io/)


## Network



## VLAN


## Storage


--GlusterFS Volume vs Barre Metal Volume

barre metal volume help full to run ceph on top of Kubernetes
bmv0
gv0 and gv1


[Install Nodes](debian/bookworm/node-install.md)


