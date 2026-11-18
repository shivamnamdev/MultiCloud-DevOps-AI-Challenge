#!/usr/bin/env bash
echo "script=$0 first=$1 second=$2 count=$# all=$@"
today=$(date +%F); old=`date +%F`
echo "today=$today old-style=$old nested=$(echo "inner $(date +%Y)")"
read -p "Name: " nm
echo "read gave: $nm"
