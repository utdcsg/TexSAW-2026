#include <iostream>
#include <cstring>
using namespace std;

int main() {
    unsigned char encrypted_flag[] = {
        0x3f, 0x2e, 0x33, 0x38, 0x2a, 0x3c, 0x30, 0x22, 0x6c, 
        0x26, 0x14, 0x2c, 0x24, 0x25, 0x25, 0x2a, 0x14, 0x2c, 
        0x2e, 0x3f, 0x14, 0x32, 0x2a, 0x6a, 0x36
    };

    const unsigned char key = 0x4B;

    char input[64];
    cout << "Enter the flag: ";
    cin >> input;

    if (strlen(input) != sizeof(encrypted_flag)) {
        cout << "Wrong!\n";
        return 0;
    }

    for (size_t i = 0; i < sizeof(encrypted_flag); i++) {
        if ((input[i] ^ key) != encrypted_flag[i]) {
            cout << "Wrong!\n";
            return 0;
        }
    }

    cout << "Correct!\n";
    return 0;
}
