import random
import struct

# CONFIGURATION
FLAG = "texsaw{VVhYd_U_M4k3_mE_s0_4n6ry}"
PREFIX_LEN = 9 # use the first 9 chars to pick the target function
NUM_FUNCS = 1009 # prime number for hash distribution
MULTIPLIER = 131    # used for hashing

# ASSETS
QUOTES = [
    "Error: Layer 8 problem.",
    "Did you mean to do that?",
    "It's not a bug, it's a feature!",
    "Sir, this is a Wendy's.",
    "Task failed successfully.",
    "Error 418: I'm a teapot.",
]

FAKE_FLAGS = [
    "texsaw{n0t_th3_fl4g_lol}",
    "texsaw{fake_flag_do_not_submit}",
    "texsaw{maybe_the_real_fake_flag_was_the_friends_we_made}",
]

# make simple arithmetic operations more complicated
def mba_add(a, b):
    ops = [
        f"(({a} ^ {b}) + 2 * ({a} & {b}))",
        f"(({a} | {b}) + ({a} & {b}))",
        f"((({a} ^ ~{b}) + 1) + 2 * ({a} & ~{b}))" 
    ]
    return random.choice(ops)

def mba_xor(a, b):
    ops = [
        f"(({a} | {b}) - ({a} & {b}))",
        f"(({a} ^ {b}))",
        f"(({a} + {b}) - 2 * ({a} & {b}))"
    ]
    return random.choice(ops)

def mba_sub(a, b):
    return f"(({a} ^ ~({b})) + 1 + 2 * ({a} & ~({b})))"

# HASHING
# non-cryptoghraphic hash
def fnv1a_32(data: bytes) -> int:
    hash_val = 0x811c9dc5
    for byte in data:
        hash_val ^= byte
        hash_val = (hash_val * 0x01000193) & 0xFFFFFFFF
    return hash_val

# Calculate target index
TARGET_PREFIX = FLAG[:PREFIX_LEN]
TARGET_INDEX = fnv1a_32(TARGET_PREFIX.encode()) % NUM_FUNCS
print(f"[*] Generating Challenge Source...")
print(f"    Target Prefix: '{TARGET_PREFIX}'")
print(f"    Target Index:  {TARGET_INDEX}")

def get_dummy_func(idx):
    types = ["segfault", "loop", "recursion", "gaslight", "bash_mock", "stall", "troll", "shell"]
    choice = random.choice(types)
    
    # Pick a random string to encrypt inside the function so 'strings' can't find it.
    if choice == "gaslight":
        raw_str = random.choice(FAKE_FLAGS)
    elif choice == "bash_mock":
        raw_str = f"bash: {random.choice(['command not found', 'Permission denied', 'syntax error'])}"
    else:
        raw_str = random.choice(QUOTES)

    # XOR-encrypt the string at generation time and write the decryption logic directly into the generated C code to make it annoying to read.
    s_bytes = raw_str.encode()
    s_key = random.randint(0x01, 0xFF)
    encrypted_hex = ", ".join([hex(b ^ s_key) for b in s_bytes])
    
    code = f"void func_{idx}(char *input) {{\n"
    
    # Add a troll state to include reversing / angr complexity 
    junk_val = random.randint(0, 0xFFFF)
    code += f"    volatile uint32_t troll_state = {hex(junk_val)};\n"
    for _ in range(random.randint(2, 4)):
        op = random.choice([mba_add, mba_xor, mba_sub])
        code += f"    troll_state = {op('troll_state', str(random.randint(1, 255)))};\n"
    
    # Decryption loop for  string.
    code += f"    uint8_t s_enc[] = {{{encrypted_hex}}};\n"
    code += f"    char s_dec[{len(s_bytes) + 1}];\n"
    code += f"    for(int i = 0; i < {len(s_bytes)}; i++) {{\n"
    dec_logic = mba_xor("s_enc[i]", str(s_key))
    code += f"        s_dec[i] = (char)({dec_logic});\n"
    code += f"    }}\n"
    code += f"    s_dec[{len(s_bytes)}] = '\\0';\n"

    # gives a shell lol
    if choice == "shell":
        code += f'    char *args[] = {{"/bin/sh", NULL}};\n'
        code += f'    execve("/bin/sh", args, NULL);\n'
        code += f'    exit(0);\n'

    # The Collatz Conjecture 
    elif choice == "loop":
        code += f'    uint32_t c = (uint32_t)input[0] + {random.randint(1, 10)};\n'
        code += f'    while(c != 1) {{\n'
        code += f'        c = (c % 2 == 0) ? (c / 2) : {mba_add("3 * c", "1")};\n'
        code += f'        if (troll_state == 0) break;\n'
        code += f'    }}\n'
        code += f'    printf("%s\\n", s_dec); exit(1);\n'

    # segfaults at a random address
    elif choice == "segfault":
        code += f'    if (troll_state > 0) {{\n'
        code += f'        fprintf(stderr, "%s\\n", s_dec);\n'
        code += f'        int *p = (int*)(uintptr_t)(troll_state & 0xFFFF);\n'
        code += f'        *p = {idx};\n'
        code += f'    }}\n'
        code += f'    exit(139);\n'
    
    # infinite recursion
    elif choice == "recursion":
        code += f'    if (troll_state % 2 != 0) {{ func_{idx}(input); }}\n'
        code += f'    exit(1);\n'

    # right message type, wrong flag   
    elif choice == "gaslight":
        code += f'    printf("\\033[0;32m[SUCCESS] Flag: %s\\033[0m\\n", s_dec);\n'
        code += f'    exit(0);\n'

    # mocks a bash error message
    elif choice == "bash_mock":
        code += f'    printf("%s: %s\\n", s_dec, input);\n'
        code += f'    exit(127);\n'
    
    # Hangs the program to hurt more scripts
    elif choice == "stall":
        code += f'    for(int i=0; i < {random.randint(1000, 5000)}; i++) {{\n'
        code += f'        troll_state = {mba_xor("troll_state", "i")};\n'
        code += f'        usleep(100);\n'
        code += f'    }}\n'
        code += f'    printf("%s\\n", s_dec); exit(1);\n'

    else: # Default Troll
        code += f'    puts(s_dec);\n'
        code += f'    exit(1);\n'

    code += "}\n"
    return code

def get_real_func(idx, full_flag):
    # Pre-calculate the correct 4 hash states for the flag
    targets = [0, 0, 0, 0]
    for i, c in enumerate(full_flag):
        b = ord(c)
        stream = i % 4
        targets[stream] = (targets[stream] * MULTIPLIER + b) & 0xFFFFFFFFFFFFFFFF
    
    code = f"void func_{idx}(char *input) {{\n"
    code += "    uint64_t s[4] = {0, 0, 0, 0};\n"
    code += "    size_t len = strlen(input);\n"
    code += "    for(size_t i = 0; i < len; i++) {\n"
    code += "        uint64_t b = (uint64_t)input[i];\n"
    
    # Generate C code to perform: s[i%4] = s[i%4] * 131 + b
    # We implement (x * 131) as ((x << 7) + (x << 1) + x) to hide the constant
    # We do not use MBA to make this solvable with angr
    
    # Step A: calc (x << 7) + (x << 1)
    code += f"        uint64_t v = s[i%4];\n"
    code += f"        uint64_t term1 = (v << 7);\n"
    code += f"        uint64_t term2 = (v << 1);\n"
    code += f"        uint64_t step1 = term1 + term2;\n" # 128x + 2x
    
    # Step B: calc (130x) + x  -> 131x
    code += f"        uint64_t mult = step1 + v;\n"

    # Step C: add char b
    code += f"        s[i%4] = mult + b;\n"
    code += "    }\n"
    
    # 3. Verification Check
    code += f"    if (s[0] == {targets[0]}ULL && s[1] == {targets[1]}ULL && "
    code += f"s[2] == {targets[2]}ULL && s[3] == {targets[3]}ULL) {{\n"
    code += "        printf(\"\\033[0;32m[SUCCESS] Flag: %s\\033[0m\\n\", input);\n"
    code += "    } else { exit(1); }\n"
    code += "}\n"
    return code

def generate_file():
    # creates the .c file
    filename = "ragebait.c"
    with open(filename, "w") as f:
        # Standard headers and a fake flag string to bait strings
        f.write("#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n#include <stdint.h>\n#include <unistd.h>\n\nchar* dummy_string = \"texsaw{nope_not_here}\";\n\n")
        
        f.write("uint32_t fnv1a_32(const void *buf, size_t size) {\n")
        f.write("    const uint8_t *p = buf; uint32_t h = 0x811c9dc5;\n")
        f.write("    while (size--) { h ^= *p++; h *= 0x01000193; }\n")
        f.write("    return h;\n}\n\n")

        # Generate 1009 functions, inserting the real one at the correct index.
        for i in range(NUM_FUNCS):
            if i == TARGET_INDEX:
                f.write(get_real_func(i, FLAG))
            else:
                f.write(get_dummy_func(i))
        
        # Create a massive function pointer table
        f.write("\nvoid (*funcs[])(char*) = {\n")
        for i in range(NUM_FUNCS):
            f.write(f"    func_{i},\n")
        f.write("};\n\n")
        
        # The entry point checks input length and uses the hash to pick which function in the table to execute.
        f.write(f"""int main(int argc, char **argv) {{
    if (argc < 2 || strlen(argv[1]) != {len(FLAG)}) return 1;
    uint32_t idx = fnv1a_32(argv[1], {PREFIX_LEN}) % {NUM_FUNCS};
    funcs[idx](argv[1]);
    return 0;
}}""")

    print(f"Created {filename}. Target Index: {TARGET_INDEX}")
    print(f"Compile command: gcc {filename} -o ragebait -s -no-pie")

if __name__ == "__main__":
    generate_file()