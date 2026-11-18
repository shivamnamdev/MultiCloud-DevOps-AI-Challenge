#!/usr/bin/env bash
echo "PATH=$PATH SHELL=$SHELL PWD=$PWD HOME=$HOME"
which python3 >/dev/null 2>&1 && echo "python3 found" || echo "python3 NOT found"
which shellcheck >/dev/null 2>&1 && echo "shellcheck found" || echo "shellcheck NOT found"
