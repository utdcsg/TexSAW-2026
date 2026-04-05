#!/usr/bin/env bash

make clean

cp main_template.cpp main.cpp
python text_to_vertices.py "$(< flag.txt)" --patch main.cpp
mv main.cpp source/main.cpp

make
