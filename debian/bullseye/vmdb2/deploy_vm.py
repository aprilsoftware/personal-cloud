#!/usr/bin/python3
# This program is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, 
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. 
# If not, see <https://www.gnu.org/licenses/>.

import argparse
import os
import sys
import time
import subprocess

# Parameters

parser = argparse.ArgumentParser()

parser.add_argument("--build_name")
parser.add_argument("--build_root_path")
parser.add_argument("--qemu_host")
parser.add_argument("--destination")
parser.add_argument("--vcpus")
parser.add_argument("--memory")
parser.add_argument("--network")
parser.add_argument("--host")

args = parser.parse_args()

build_name = args.build_name
build_root_path = args.build_root_path
qemu_host = args.qemu_host
destination = args.destination
vcpus = args.vcpus
memory = args.memory
network = args.network
host = args.host

if build_name is None:
    print("Missing build name")
    sys.exit(1)

if build_root_path is None:
    print("Missing build root path")
    sys.exit(1)

if qemu_host is None:
    print("Missing qemu host")
    sys.exit(1)

if destination is None:
    print("Missing destination")
    sys.exit(1)

if vcpus is None:
    print("Missing vcpus")
    sys.exit(1)

if memory is None:
    print("Missing memory")
    sys.exit(1)

if network is None:
    print("Missing network")
    sys.exit(1)

if host is None:
    print("Missing host")
    sys.exit(1)

build_name = build_name.strip()
build_root_path = build_root_path.strip()
qemu_host = qemu_host.strip()
destination = destination.strip()
vcpus = vcpus.strip()
memory = memory.strip()
network = network.strip()
host = host.strip()

if len(build_name) == 0:
    print("Invalid build name")
    sys.exit(1)

if len(build_root_path) == 0:
    print("Invalid build root path")
    sys.exit(1)

if len(qemu_host) == 0:
    print("Invalid qemu host")
    sys.exit(1)

if len(destination) == 0:
    print("Invalid destination")
    sys.exit(1)

if len(vcpus) == 0:
    print("Invalid vcpus")
    sys.exit(1)

if len(memory) == 0:
    print("Invalid memory")
    sys.exit(1)

if len(network) == 0:
    print("Invalid network")
    sys.exit(1)

if len(host) == 0:
    print("Invalid host")
    sys.exit(1)

# Copy image

if subprocess.run(["scp", 
        build_root_path + "/" + build_name + ".img", 
        qemu_host + ":" + destination]).returncode != 0:
    sys.exit(1)

# Install VM

if subprocess.run(["virt-install", 
        "--connect=qemu+ssh://" + qemu_host + "/system",
        "--name",
        build_name,
        "--vcpus",
        vcpus,
        "--memory",
        memory,
        "--disk",
        "path=" + destination + "/" + build_name + ".img,format=qcow2,bus=virtio",
        "--import",
        "--os-variant",
        "debian10",
        "--network",
        "network=" + network + ",model=virtio",
        "--graphics",
        "spice",
        "--noautoconsole",
        "--console",
        "pty,target_type=serial"]).returncode != 0:
    sys.exit(1)