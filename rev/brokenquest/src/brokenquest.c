#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

void reset(int flags[]) {
	memset(flags, 0, sizeof(char) * 8);
}

void rotate(int flags[]) {
	int temp = flags[7];
	for(int i=6; i>=0; i--) {
		flags[i+1] = flags[i];
	}
	flags[0] = temp;
}

void increment(int flags[]) {
	flags[0]++;
	flags[4]++;
}

void add_sub(int flags[]) {
	flags[0] += 3;
	flags[3] -= 2;
}

void modulo(int flags[]) {
	flags[0] /= 5;
	flags[6] %= 5;
}

void swap(int flags[]) {
	int temp = flags[0];
	flags[0] = flags[5];
	flags[5] = temp;
}

void bitshift(int flags[]) {
	flags[1] <<= 1;
	flags[7] >>= 1;
}

void flip_sign(int flags[]) {
	flags[0] *= -1;
	flags[2] *= -1;
}

char char_clamp(int val) {
	return (char)(val%256);
}

char op0(char v1, int v2) {
	return char_clamp(v1+v2+'0');
}

char op1(char v1, int v2) {
	if(v1 && v2) {
		return char_clamp(v1*v2);
	} else if(v2) {
		return char_clamp(v2*v2);
	} else if(v1) {
		return char_clamp(v1*v2);
	}

	return '\x00';
}

char op2(char v1, int v2) {
	return char_clamp(v1+1);
}

char op3(char v1, int v2) {
	return char_clamp(v1+v2);
}

char op4(char v1, int v2) {
	if(v2) {
		return char_clamp(v1%v2);
	} else {
		return v1;
	}
}

char op5(char v1, int v2) {
	return char_clamp(v1-v2);	
}

char op6(char v1, int v2) {
	if(v2 < 0) {
		v2 *= -1;
	}
	return char_clamp(v1<<v2);
}

char op7(char v1, int v2) {
	return char_clamp(v1+(v2*-1));
}

char calc_val(int pos_arr[], int val_arr[], int start) {
	char val = (char)val_arr[start];
	for(int i=0; i<7; i++) {
		int idx = (start + i) % 8;
		
		switch(pos_arr[idx]) {
			case 0:
				val = op0(val, val_arr[(idx+1)%8]);
				break;
			case 1:
				val = op1(val, val_arr[(idx+1)%8]);
				break;
			case 2:
				val = op2(val, val_arr[(idx+1)%8]);
				break;
			case 3:
				val = op3(val, val_arr[(idx+1)%8]);
				break;
			case 4:
				val = op4(val, val_arr[(idx+1)%8]);
				break;
			case 5:
				val = op5(val, val_arr[(idx+1)%8]);
				break;
			case 6:
				val = op6(val, val_arr[(idx+1)%8]);
				break;
			case 7:
				val = op7(val, val_arr[(idx+1)%8]);
				break;
			default:
				puts("Something went wrong! This shouldn't happen.");
		}
	}
	return val;	
}

void transform(char buf[], int pos_arr[], int val_arr[], const char* bytes, int in_start, int out_start, int len) {
	for(int i=0; i<len; i++) {
		char val = calc_val(pos_arr, val_arr, pos_arr[i%8]);
		char sbyte = bytes[in_start+i];
		buf[out_start+i] = val ^ sbyte;
	}
}

void handle_flag(int flags[]) {
	const char* bytes = "\xa4\x76\x30\x58\x6b\xfd\x60\x67\x06\x7d\x31\x21\x32\x68\x20\x24\x69\x2c\x87\x5d\x80\x0e\x3d\x30\x26\x78\xbd\x9c\x9e\x89\x77\xa4\x3f\x6a\x83\xca\x8d\x51\x65\x7b\xe7\x65\xff\x57\xcd\x51";
	int positions[8][8] = {{5, 3, 0, 7, 1, 6, 4, 2},
						   {3, 6, 2, 0, 1, 4, 5, 7},
						   {4, 5, 1, 3, 6, 0, 2, 7},
						   {3, 2, 5, 1, 4, 0, 6, 7},
						   {7, 4, 6, 1, 0, 3, 2, 5},
						   {4, 3, 0, 5, 6, 7, 1, 2},
						   {6, 0, 3, 2, 1, 7, 4, 5},
						   {5, 4, 2, 7, 3, 0, 6, 1}};
	int values[8][8];
	for(int i=0; i<8; i++) {
		for(int j=0; j<8; j++) {
			values[i][j] = flags[positions[i][j]];
		}
	}

	// yes I know this is ugly but I swear there's a point
	char output[47] = {0};
	transform(output, positions[0], values[0], bytes, 37, 0, 9);
	transform(output, positions[1], values[1], bytes, 32, 9, 5);
	transform(output, positions[2], values[2], bytes, 26, 14, 6);
	transform(output, positions[3], values[3], bytes, 21, 20, 5);
	transform(output, positions[4], values[4], bytes, 16, 25, 5);
	transform(output, positions[5], values[5], bytes, 13, 30, 3);
	transform(output, positions[6], values[6], bytes, 6, 33, 7);
	transform(output, positions[7], values[7], bytes, 0, 40, 6);	

	printf("Here's your reward: %s\n", output);
}

int turn_in(int flags[], int target[]) {
	if(memcmp(flags, target, 8)) {
		puts("Objectives not met - can't turn in quest yet!\n");
		return 1;
	} else {
		puts("You turned in the quest!\n");
		handle_flag(flags);
		return 0;
	}
}

void print_menu() {
	puts("Choose an action [0-8] to (probably) advance your quest:");
	puts("0: Turn in Quest");
	puts("1: Reset");
	puts("2: Rotate Pillars");
	puts("3: Increase Heat");
	puts("4: Move Gold Coins");
	puts("5: Swing Sword");
	puts("6: Swap Gems");
	puts("7: Shift Sand Piles");
	puts("8: Reverse Polarity\n");
}

int main(int argc, char** argv) {
	int flags[8] = {0};
	int target[] = {2, 6, -4, 6, 0, 4, -3, 1};
	int status = 1;

	puts("Interact with objects to advance your quest. Set all quest objective flags and turn in the quest to get the real flag.");

	char buf[8];
	uint8_t input;
	while(status) {
		printf("Current Values: [ ");
		for(int i=0; i<8; i++) {
			printf("%d\t", flags[i]);
		}
		puts("]");

		print_menu();

		memset(buf, 0, sizeof(char) * 8);
		fgets(buf, 8, stdin);
		sscanf(buf, "%c", &input);
		input -= '0';
		if(input < 0 || input > 8) {
			puts("That's not a valid action.\n");
			continue;
		}

		switch(input) {
			case 0:
				status = turn_in(flags, target);
				break;
			case 1:
				reset(flags);
				break;
			case 2:
				rotate(flags);
				break;
			case 3:
				increment(flags);
				break;
			case 4:
				add_sub(flags);
				break;
			case 5:
				modulo(flags);
				break;
			case 6:
				swap(flags);
				break;
			case 7:
				bitshift(flags);
				break;
			case 8:
				flip_sign(flags);
				break;
			default:
				puts("That's not a valid action.\n");
		}
	}

	return 0;
}
