# Model Heist - CTF Challenge

A machine learning forensics challenge where participants must extract a flag hidden in neural network weights.

## Challenge Structure

```
ModelHeist/
├── challenge.yml        # Challenge metadata and configuration
├── Makefile             # Build and test automation
├── README.md            # This file
├── dist/                # Files distributed to participants
│   ├── model.h5         # The neural network model with hidden flag
│   └── challenge.txt    # Hint text
├── src/                 # Source code for generating the challenge
│   ├── create_model.py  # Script that creates the model with hidden flag
│   └── requirements.txt # Dependencies for building
└── writeup/             # Detailed writeup
    ├── WRITEUP.md       # Step-by-step solution guide
    ├── solve.py         # Solution script
    └── solution_requirements.txt
```

## Building the Challenge

```bash
make build
```

This will:
1. Install required dependencies
2. Generate the model with the hidden flag
3. Copy files to the `dist/` directory

## Testing the Solution

```bash
make test
```

This runs the solution script to verify the flag can be extracted correctly.

## Clean Build Artifacts

```bash
make clean
```

## Flag

`texsaw{w3ight5_t3ll_t4l3s}`

## Difficulty

**Medium (200 points)**

Requires knowledge of:
- Loading and inspecting Keras/TensorFlow models
- Understanding neural network weight structures
- Basic data encoding/decoding

## Author

brig
