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

- 3 regular PC with 3 network interfaces
- 3 network switches
- a connection to internet


## Network



## VLAN

## Components

- KVM
- Open Virtual Switch
- GlusterFS
- Backup using Borg Backup and its data deduplication technique.
...

## GlusterFS Volume vs Barre Metal Volume

bmv0
gv0 and gv1

[Install Nodes](debian/bookworm/node-install.md)


