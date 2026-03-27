# SIGBOVIK I Writeup

scrop (https://www.charles.systems/publications/SCROP.pdf) is a threaded interpreter.
That means it takes programs with a custom executable format that looks like:
  <8 bytes of opcode><8 bytes of immediate>
Such that the opcode is the address of the segment of code in the interpreter that interprets the instruction.
This is talked about in my SIGBOVIK paper that's linked in the challenge: https://www.charles.systems/publications/SCROP.pdf

If players strings dist/interpreter, they'll see references to flag.txt and /bin/cat.
So it should be clear that they should try to call some execve or system or something.

Looking hard enough, we find a function at 0x8008574 that loads in the strings and calls execve.
Now to write a program the interpreter will accept, you just copy a program that the scrop assembler spits out, and replace 
any instruction between the first and last (these are necessary for maintaining the stack frame) with
an instruction whose binary representation looks like
  <8008574><0000000>

The interpreter does not check if opcodes are in bounds, so this takes you to the win function, which prints out the flag.

## Solution

`cat payload | nc <ip> 1900`
