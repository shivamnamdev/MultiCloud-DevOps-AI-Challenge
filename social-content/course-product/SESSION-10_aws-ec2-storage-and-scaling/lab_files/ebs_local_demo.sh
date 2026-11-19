#!/bin/bash
# The Linux half of the volume lab, with a file standing in for the EBS volume. Run as root inside the
# practice container (Session 5B). It makes a 200 MB "disk", formats it, mounts it, adds an fstab line with
# nofail, then copies the disk image and mounts the copy to prove a restore works.
set -e
truncate -s 200M /disk.img
L=$(losetup -f --show /disk.img); echo "device $L"
echo "blkid on the empty disk: [$(blkid $L)]  (empty means safe to format)" || true
mkfs -t ext4 -q $L
mkdir -p /data /restore
mount $L /data; df -h /data | tail -1
echo important > /data/note.txt
U=$(blkid -s UUID -o value $L)
echo "UUID=$U /data ext4 defaults,nofail 0 2" >> /etc/fstab
umount /data; mount -a; echo "after umount + mount -a: $(cat /data/note.txt)"
sync; cp --sparse=always /disk.img /disk-copy.img          # stands in for "snapshot, then new volume"
L2=$(losetup -f --show /disk-copy.img)
mount $L2 /restore; echo "restore test: $(cat /restore/note.txt)"
umount /restore /data; losetup -d $L $L2
sed -i "/UUID=$U/d" /etc/fstab; rm -f /disk.img /disk-copy.img; rmdir /data /restore
echo "loop devices left: $(losetup -a | wc -l)"
