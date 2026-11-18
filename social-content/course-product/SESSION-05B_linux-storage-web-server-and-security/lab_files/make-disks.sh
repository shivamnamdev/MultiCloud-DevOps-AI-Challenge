#!/bin/bash
# Practice only, inside the privileged Rocky container.
# Makes two "disks" (5 GB and 10 GB, sparse files) as loop devices, standing in for /dev/sdb and /dev/sdc.
#   make-disks.sh create   : create both and print their device names
#   make-disks.sh nodes    : (re)create the /dev entries for partitions, run after fdisk or partprobe
#   make-disks.sh remove   : detach both and delete the files
case "$1" in
  create)
    truncate -s 5G /disk-b.img; truncate -s 10G /disk-c.img
    echo "5 GB disk : $(losetup -fP --show /disk-b.img)"
    echo "10 GB disk: $(losetup -fP --show /disk-c.img)" ;;
  nodes)
    # A container has no udev, so the kernel's partition devices do not appear in /dev by themselves.
    for d in /sys/class/block/loop*p*; do
      [ -e "$d" ] || continue
      n=$(basename "$d"); [ -e "/dev/$n" ] || mknod -m 660 "/dev/$n" b $(tr ':' ' ' < "$d/dev")
    done
    ls /dev/loop*p* 2>/dev/null ;;
  remove)
    for f in /disk-b.img /disk-c.img; do
      for l in $(losetup -j "$f" -O NAME -n); do losetup -d "$l"; done; rm -f "$f"
    done
    rm -f /dev/loop*p*; losetup -a ;;
  *) echo "usage: $0 create|nodes|remove"; exit 1 ;;
esac
