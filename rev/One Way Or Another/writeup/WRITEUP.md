# One Way Or Another Writeup

Use Ghidra to decompile the binary. 
Find the byte array in “.rodata” and the constant XOR key “0x4B”. 
Notice the condition: if ((input[i] ^ key) != encrypted_flag[i]). Using that, we realize that flag[i] = encrypted_flag[i] ^ key. 
Write a solution program. Output will produce the flag. 