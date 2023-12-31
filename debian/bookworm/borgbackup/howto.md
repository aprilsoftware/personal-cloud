# Install [BorgBackup](https://www.borgbackup.org/)

```
apt install borgbackup
```

# Initialize a repository

```
borg init --encryption=repokey /mnt/gv1/backup/daily
```

or

```
borg init --encryption=none /mnt/gv1/backup/daily
```

# List backups

```
borg list /mnt/gv1/backup/daily
```

# Restore a file

```
borg extract /mnt/gv1/backup/daily:DAILY_2023-04-02 mnt/snapshots/gv0/vm/net0.test.img
```

# Delete a backup

```
borg delete /mnt/gv1/backup/vm::DAILY_2023-04-02
```

# Backup script

[Daily VM images backup script](https://github.com/aprilsoftware/personal-cloud/blob/main/debian/bookworm/borgbackup/daily.backup.sh) (GlusterFS snapshot)

