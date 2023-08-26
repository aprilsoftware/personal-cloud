# [vmdb2](https://vmdb2.liw.fi/)
## Install
```
apt install vmdb2
```

```
wget -O build_vm.py https://aprilsoftware.github.io/personal-cloud/debian/bullseye/vmdb2/build_vm.py
```

```
wget -O deploy_vm.py https://aprilsoftware.github.io/personal-cloud/debian/bullseye/vmdb2/deploy_vm.py

```

## Build an image
```
TEMPLATE_ROOT_PATH=templates
BUILD_ROOT_PATH=PATH_TO_IMG

python3 build_vm.py --build_name example.server1 \
        --build_root_path ${BUILD_ROOT_PATH} \
        --template_name bookworm_base_1 \
        --template_root_path ${TEMPLATE_ROOT_PATH} \
        --domain example.com \
        --hostname example \
        --ip 192.168.0.100 \
        --gateway 192.168.0.1 \
        --vm_size 10G \
        -o

```

[Templates](https://github.com/aprilsoftware/personal-cloud/tree/main/debian/bullseye/vmdb2/templates)

## Deploy an image
```
BUILD_ROOT_PATH=PATH_TO_IMG

python3 deploy_vm.py --build_name example.server1 \
        --build_root_path ${BUILD_ROOT_PATH} \
        --qemu_host admin@node1 \
        --destination /mnt/gv0/vm \
        --vcpus 1 \
        --memory 2048 \
        --network br0 \
        --host admin@server1.example.com

sudo rm ${BUILD_ROOT_PATH}/example.server1.img

```