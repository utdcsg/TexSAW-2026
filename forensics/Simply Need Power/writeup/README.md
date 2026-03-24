## You Simply Need Power

## Description
You are an agent for the NSA and have gained physical access to a secure hardware device that performs cryptographic operations.

## Solution
1. Plot the trace and you will notice that there are 256 repeating blocks each with 1 or 2 spikes
2. Recognize that 1 spike = 0 and 2 spikes = 1
3. Extract the bits using 1.3 as a threshold (guessy but pretty easy to guess)
4. Convert to int and decrypt using AES-CBC

## Author Name
ag3nt
