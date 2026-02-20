This is an intro pwn challenge that requires a 1 (or 2) step ROP chain.
The solution script is "solve.py", but the general steps are below:
- Decompile/disassemble/GDB the target binary to find the win function "drive" that calls system("/bin/sh") and opens a shell
- Note the address of "drive"
- Analyze the logic of "drive" and note that it requires a key as an argument before calling system()
- Note that the value of the key is 0x48435344
- Note that "gets" is an input function vulnerable to buffer overflow and its associated buffer is size 32
- Note that the return address on the stack is 40 bytes from the start of the vuln buffer
- Create a pwntools script (or equivalent):
    - Concept: craft a payload to "gets" that replaces the return address on the stack with a ROP chain sequence that executes a "pop rdi" gadget to put 0x48435344 in rdi, aligns the stack, and returns to "drive"
    - Find "pop rdi" and "ret" gadgets
    - Payload: 40 bytes padding, pop rdi addr, 0x48435344, pop ret addr, "drive" addr
- Execute the script against the target and cat out the flag