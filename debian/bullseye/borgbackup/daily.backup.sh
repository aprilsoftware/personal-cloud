#!/bin/bash
export BORG_REPO=/mnt/gv1/backup/daily
# Provide the passphare here if the repository is encrypted
#export BORG_PASSPHRASE=...

ARCHIVE=DAILY_$(date +%F)

echo "$(date): Backup ${ARCHIVE} started"

gluster --mode=script snapshot create gv0_backup gv0 no-timestamp
gluster --mode=script snapshot activate gv0_backup

mount -t glusterfs hal4-1.local:/snaps/gv0_backup/gv0 /mnt/snapshots/gv0

if [ -d "/mnt/snapshots/gv0/vm" ]
then
        echo gv0 snapshot successfully mounted
else
        echo gv0 snapshot not mounted

        echo "$(date): Backup ${ARCHIVE} failed"

        exit 1
fi

echo borg create

borg create --list --stats --show-rc ::${ARCHIVE} /mnt/snapshots/gv0/vm/*.img

backup_exit=$?

echo borg prune

borg prune --list --prefix 'DAILY_' --show-rc --keep-daily=7 --keep-weekly=4 --keep-monthly=12

prune_exit=$?

umount /mnt/snapshots/gv0

if [ -d "/mnt/snapshots/gv0/vm" ]
then
        echo gv0 snapshot unmounted failed
else
        echo gv0 snapshot unmounted successfully
fi

gluster --mode=script snapshot delete gv0_backup

global_exit=$(( backup_exit > prune_exit ? backup_exit : prune_exit ))

if [ ${global_exit} -eq 0 ]; then
    echo "Backup and Prune finished successfully"
elif [ ${global_exit} -eq 1 ]; then
    echo "Backup and/or Prune finished with warnings"
else
    echo "Backup and/or Prune finished with errors"
fi

# Clone the repo on different media
#echo cloning repo
#/usr/bin/rclone sync -v /mnt/gv1/backup/daily destination:/path

echo "$(date): Backup ${ARCHIVE} completed"