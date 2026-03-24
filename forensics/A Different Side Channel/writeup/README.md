## A Different Side Channel P2

## Description
You've captured 500 power traces from a hardware AES encryption device while it processed known plaintexts with an unknown secret key.

## Solution
1. Load the traces.npy and plaintexts.npy
2. Attack each byte:
   - Try all 256 possible key values
   - For each guess, compute hypothetical hamming weight
   - Correlate those values with actual power consumption
   - Highest correlation = correct key byte
3. Recover the full AES key
4. Decrypt with AES-CBC

## Author Name
ag3nt

