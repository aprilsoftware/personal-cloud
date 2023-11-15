# [rclone](https://rclone.org/)
## Install
```
apt install rclone
```

## SSH
```
ssh-keygen
```

```
ssh-copy-id user@server1.example.com
```

```
vi ~/.config/rclone/rclone.conf
```

```
[server1]
type = sftp
host = server1.example.com
user = user
key_file = /root/.ssh/id_rsa
```

On the SSH server side
```
vi /etc/ssh/sshd_config
```

```
PubkeyAuthentication yes
PubkeyAcceptedAlgorithms=+ssh-rsa
```

# AWS
```
vi ~/.config/rclone/rclone.conf
```

```
[data]
type = s3
provider = AWS
env_auth = false
access_key_id = 
secret_access_key = 
region = eu-central-1
location_constraint = eu-central-1
acl = private

[data_crypt]
type = crypt
remote = data:MY_S3_BUCKET
filename_encryption = standard
directory_name_encryption = true
password = 
password2 = 
```

## Sync
```
rclone sync -i folder1 data_crypt:folder1
```