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
- 3 network switches (L2)
- a connection to internet

This procedure can be easily adapted to run a cluster of [Raspberry Pi](https://www.raspberrypi.org/). We managed to run a cluster on 3 Raspberry Pi with limited network capabilities (for instance no routing / no firewall capabilites).

## Components
We selected the following components to fulfill our requirements:

| Component | Feature |
| --- | --- |
| [KVM](https://www.linux-kvm.org/page/Main_Page) / [libvirt](https://libvirt.org/) / [virt-manager](https://virt-manager.org/) | Hypervisor
| [GlusterFS](https://www.gluster.org/) | Software-defined storage & Scale out storage
| [clevis](https://github.com/latchset/clevis) / [luks](https://gitlab.com/cryptsetup/cryptsetup) / [tang](https://github.com/latchset/tang) | Disk Encryption
| [Open vSwitch](https://www.openvswitch.org/) / [OPNsense](https://opnsense.org/) | Software-defined networking
| [BorgBackup](https://www.borgbackup.org/) | Data deduplication backup
| [Prometeus](https://prometheus.io/) | Telemetry


## Network




## VLAN


## Storage

4 drives, 3 encrypted, os not encrypted

tang for

--GlusterFS Volume vs Barre Metal Volume

barre metal volume help full to run ceph on top of Kubernetes
bmv0
gv0 and gv1

## Backup


[Install Nodes](debian/bookworm/node-install.md)


