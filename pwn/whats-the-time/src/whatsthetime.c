#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <stdint.h>
#include <string.h>

void win() {
	const char *msg = "Executing shell";
	const char *shell = "/bin/sh";
	printf("%s %s...", msg, shell);
	system("ls");
	printf("oops wrong command");
}

void read_user_input(int key) {
	setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
	char buffer[40];
	char *temp = malloc(160);

	//Overflowing the buffer directly with read broke the loop
	int read_size = read(0, temp, 160);

	for (int byte_chunk = 0; byte_chunk < read_size; byte_chunk += 4) {
		for (int current_byte = 0; current_byte < 4; current_byte++) {
			temp[byte_chunk + current_byte] ^= (key >> (current_byte * 8)) & 0xFF;
		}
		key++;
	}

	//Had to memcpy the temp to buffer after XORing
	memcpy(buffer, temp, read_size);
	write(1, buffer, 40);
}

int main() {
	int custom_time = time(NULL);
	custom_time = (custom_time / 60) * 60;

	time_t rawtime = custom_time;
	printf("I think one of my watch hands fell off!\n");
	printf("Currently the time is: %s", ctime(&rawtime));
	read_user_input(custom_time);
}
