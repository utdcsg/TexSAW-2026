#!/bin/bash

set -euo pipefail

echo 1
python3 ./assembler/main.py > /tmp/asm
echo 2
./interpreter/interpreter < /tmp/asm
echo 3
