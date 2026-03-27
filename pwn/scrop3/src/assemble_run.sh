#!/bin/bash

set -euo pipefail

python3 ./assembler/main.py > /tmp/asm
./interpreter/interpreter
