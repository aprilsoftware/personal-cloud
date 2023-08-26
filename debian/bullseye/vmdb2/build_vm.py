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
import shutil
import subprocess

# Parameters

parser = argparse.ArgumentParser()

parser.add_argument("--build_name")
parser.add_argument("--build_root_path")
parser.add_argument("--template_name")
parser.add_argument("--template_root_path")
parser.add_argument("--domain")
parser.add_argument("--hostname")
parser.add_argument("--ip")
parser.add_argument("--gateway")
parser.add_argument("--vm_size")
parser.add_argument("-o", "--override", help="Override build if already existing", action="store_true")

args = parser.parse_args()

build_name = args.build_name
build_root_path = args.build_root_path
template_name = args.template_name
template_root_path = args.template_root_path
domain = args.domain
hostname = args.hostname
ip = args.ip
gateway = args.gateway
vm_size = args.vm_size

if build_name is None:
    print("Missing build name")
    sys.exit(1)

if build_root_path is None:
    print("Missing build root path")
    sys.exit(1)

if template_name is None:
    print("Missing template name")
    sys.exit(1)

if template_root_path is None:
    print("Missing template root path")
    sys.exit(1)

if domain is None:
    print("Missing domain")
    sys.exit(1)

if hostname is None:
    print("Missing hostname")
    sys.exit(1)

if ip is None:
    print("Missing ip")
    sys.exit(1)

if gateway is None:
    print("Missing gateway")
    sys.exit(1)

if vm_size is None:
    print("Missing vm size")
    sys.exit(1)

build_name = build_name.strip()
build_root_path = build_root_path.strip()
template_name = template_name.strip()
template_root_path = template_root_path.strip()
domain = domain.strip()
hostname = hostname.strip()
ip = ip.strip()
gateway = gateway.strip()
vm_size = vm_size.strip()

if len(build_name) == 0:
    print("Invalid build name")
    sys.exit(1)

if len(build_root_path) == 0:
    print("Invalid build root path")
    sys.exit(1)

if len(template_name) == 0:
    print("Invalid template name")
    sys.exit(1)

if len(template_root_path) == 0:
    print("Invalid template root path")
    sys.exit(1)

if len(domain) == 0:
    print("Invalid domain")
    sys.exit(1)

if len(hostname) == 0:
    print("Invalid hostname")
    sys.exit(1)

if len(ip) == 0:
    print("Invalid ip")
    sys.exit(1)

if len(gateway) == 0:
    print("Invalid gateway")
    sys.exit(1)

if len(vm_size) == 0:
    print("Invalid vm size")
    sys.exit(1)

build_path = build_root_path + "/" + template_name

if os.path.exists(build_path) == False:
    os.mkdir(build_path)
elif os.path.isdir(build_path) == False:
    print("Invalid build path")
    print("Path: ", build_path)
    sys.exit(1)
elif args.override == False: 
    print("Build path already exists")
    print("Path: ", build_path)
    sys.exit(1)

# Initalize template

shutil.copy(template_root_path  + "/" + template_name + ".vmdb", \
    build_path + "/" + template_name + ".vmdb")

vmdb_file_path = build_path + "/" + template_name + ".vmdb"

with open(vmdb_file_path, 'r') as in_file:
    file_content = in_file.read()

file_content = file_content.replace("{{ domain }}", domain)
file_content = file_content.replace("{{ hostname }}", hostname)
file_content = file_content.replace("{{ ip }}", ip)
file_content = file_content.replace("{{ gateway }}", gateway)
file_content = file_content.replace("{{ vm_size }}", vm_size)

with open(vmdb_file_path, 'w') as out_file:
    out_file.write(file_content)

# Create image

if subprocess.run(["sudo", 
        "qemu-img", 
        "create",
        "-f",
        "qcow2",
#        "-o",
#        "preallocation=full",
         build_root_path + "/" + build_name + ".img",
         vm_size]).returncode != 0:
    sys.exit(1)

if subprocess.run(["sudo", 
        "modprobe", 
        "nbd",
        "max_part=8"]).returncode != 0:
    sys.exit(1)

if subprocess.run(["sudo", 
        "qemu-nbd", 
        "--connect=/dev/nbd0",
        "--format=qcow2",
        "--cache=none",
        "--detect-zeroes=on",
        "--aio=native",
        build_root_path + "/" + build_name + ".img"]).returncode != 0:
    sys.exit(1)

process = subprocess.run(["sudo", 
        "vmdb2", 
        "--image",
        "/dev/nbd0",
        "--rootfs-tarball",
        build_path + "/" + template_name + ".tar.gz",
        "--log",
        build_path + "/" + template_name + ".log",
        vmdb_file_path])

if subprocess.run(["sudo", 
        "qemu-nbd", 
        "--disconnect",
        "/dev/nbd0"]).returncode != 0:
    sys.exit(1)

if process.returncode != 0:
    sys.exit(1)