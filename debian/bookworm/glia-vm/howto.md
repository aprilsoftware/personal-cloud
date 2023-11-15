#  [glia-vm](https://github.com/aprilsoftware/glia-vm)

```
git clone https://github.com/aprilsoftware/glia-vm.git
```

```
mkdir -p ~/img
```

```
glia-vm/debian/buildvm --path ~/img \
        --name server1 \
        --release bookworm \
        --domain example.com \
        --hostname server1 \
        --ip 192.168.0.110 \
        --gateway 192.168.0.1 \
        --nameserver 192.168.0.1 \
        --size 10G \
        --ask-root-password \
        --ask-glia-password
```

```
glia-vm/debian/deployvm --path ~/img \
        --name server1 \
        --host glia@node1.local \
        --destination /mnt/gv0/vm \
        --vcpus 1 \
        --memory 2048 \
        --network br0 \
        --delete-image
```