# Whats The Time Write Up

The challenge XORs the input passed to the program.
The program also has a buffer overflow exploit that can
be taken advantage of. (via ROP).

This encryption method first takes the time from the start of execution and then
removes the seconds.

(The decription and the program give a little hint to this.)

The time is used to XOR with the input one byte at a time.
Since the hex value of time is 4 bytes, the program will work with 4 bytes of input at a time.

*FOR EXAMPLE*
In GDB the time would look like 0x697d191b which is the epoch time 1769806107
the seconds would get truncated which would turn the hex to 0x697d1900 and the epoch time 1769806080
NOTE: The hex time truncated might not always end with a 0x00 byte.

The user will input something and it would get XOR'ed using the time as the key.

The character 'a' = 0x65 would get XOR'ed with 0x697d1900 which will only XOR the lowest byte.
The time key will get bit shifted right 8 times to move on to the next byte.

The next character 'b' = 0x66 would get XOR'ed with 0x00697d19 with the lower byte

It would do this up to 4 times and then start on the next 4 bytes.
Each time it moves up to the next 4 bytes, it would increment the time value by one

So 0x697d1900 -> 0x697d1901

The encryption would loop like thing until it gets through all of the input.

Afterwards, the program will do a memcpy into a buffer made earlier which would cause an overflow.
(Its done like this because directly overflowing the buffer first would break the encryption loop)

There is a method thats also included called win() that acts a bit of a fake win condition.
The method only does system(ls) which wouldnt be useful for actually getting the flag.
However, this gives users enough tools to ROP system and /bin/sh together to get the flag.

The main problem for users is to reverse how the encryption works and encrypt a ROP payload to
get the flag.

A pwntools solution is provided.
