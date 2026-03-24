#!/usr/bin/env python3
import random

# The tempering in MT19937 (as used in Python) is:
#   y = x
#   y ^= (y >> 11)
#   y ^= (y << 7)  & 0x9d2c5680
#   y ^= (y << 15) & 0xefc60000
#   y ^= (y >> 18)
#
# To recover the internal state from an output, we must “untemper” it.
# The following functions perform the reversal iteratively.

def undo_right(y, shift):
    result = y
    # Reapply the right shift correction several times.
    for _ in range(5):
        result = y ^ (result >> shift)
    return result

def undo_left(y, shift, mask):
    result = y
    # Reapply the left shift correction several times.
    for _ in range(5):
        result = y ^ ((result << shift) & mask)
    return result

def untemper(y):
    y = undo_right(y, 18)
    y = undo_left(y, 15, 0xefc60000)
    y = undo_left(y, 7, 0x9d2c5680)
    y = undo_right(y, 11)
    return y

def recover_state(dump):
    if len(dump) < 624:
        raise ValueError("Need at least 624 outputs to recover state.")

    # Untemper all 624 outputs to get the internal state
    state_vector = [untemper(y) for y in dump[:624]]

    # Append the index — this must be an int in [0, 624]
    # Use 624 so that the next call to random() will generate new values
    state_vector.append(624)

    # Wrap in the full state tuple as expected by Python's random module
    mt_state = (3, tuple(state_vector), None)
    return mt_state


def main():
    # Read the bit dump from the file provided in the challenge.
    with open("dump.txt", "r") as f:
        lines = f.readlines()
    dump = [int(line.strip()) for line in lines]
    if len(dump) < 624:
        print("Error: Not enough outputs in dump.txt to recover state.")
        return

    # Recover the internal state from the first 624 tempered outputs.
    state = recover_state(dump[:624])
    
    # Create a new random instance and set its state.
    r = random.Random()
    r.setstate(state)
    
    # The challenge provided 1000 outputs (bit dumps) in total.
    # We used the first 624 to recover state.
    # Advance the generator by (1000 - 624) outputs to catch up with the challenge.
    for _ in range(1000 - 624):
        r.getrandbits(32)
    
    # Now predict the next 200 challenge numbers.
    predicted = []
    for _ in range(1000):
        raw = r.getrandbits(32)
        num = (raw % 20) + 1
        predicted.append(num)
    
    # Output the predicted secret sequence.
    print("Predicted secret sequence (200 numbers):")
    for num in predicted:
        print(num)

if __name__ == "__main__":
    main()
