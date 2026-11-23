#!/bin/bash
# The fix from the script: refuse an empty or missing DIR twice (once for the argument, once at the rm).
DIR="${1:?usage: DIR}"
echo rm -rf "${DIR:?}"/*      # "echo" keeps this demo harmless; remove it only on a throwaway folder
