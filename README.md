# Texsaw 2026

## Deadline - Valentines Day \<3

## Flag format 
texsaw{flag}

## Instructions
* Make a directory for your challenge in the relevant category
* Include your challenge in your directory
* Include a flag
* Include Make files
* Include solution scripts if applicable

## Format
For each challenge follow the following directory structure:

```
challenge/
├── challenge.yml       
├── docker-compose.yml   (optional) -- optional if challenge isn't hosted / dynamic
├── Dockerfile          (optional) -- ^^
├── dist/               (optional) -- any files directly uploaded / distributed to the ctf participant
│   └── distributed.exe
├── src/                (optional) -- anything running on the server
│   ├── requirements.txt
│   ├── serve.sh
│   └── server.py
└── writeup/            -- detailed, step-by-step writeup
    └── WRITEUP.md
```

The challenge.yml should be structured like the following:
```
name: <challenge name>
author: <challenge author>
category: <category>
description: |
    Challenge description.

  Flag format: texsaw{flag}
  ex: texsaw{orthogonal}

attribution: Written by <author>
value: <any value> (100 easy, 500 crazy hard)
type: standard
flags:
  - {
      type: static,
      content: "texsaw{flag_here}",
      data: case_insensitive,
  }
files:
  - chal.png
state: hidden
```
