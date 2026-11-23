#!/bin/bash
# SAFE twin of the risky script: "echo" prints what rm WOULD receive. Nothing is deleted.
DIR=$1
echo rm -rf $DIR/*
