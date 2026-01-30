#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void avenue() {
// address avenue
	puts("Package delivered to 0 Address Avenue.\n");
}

void boulevard() {
// buffer boulevard
	puts("Package delivered to 1 Buffer Boulevard.\n");
}

void court() {
// canary court
	puts("Package delivered to 2 Canary Court.\n");
}

void drive(long key) {
// dangerous drive
	puts("Attempting secret delivery to 3 Dangerous Drive...\n");
	if(key == 0x48435344) {
		puts("Success! Secret package delivered.\n");
		system("/bin/sh");
	} else {
		puts("Need the secret key to deliver this package.\n");
	}
}

void deliver() {
	char buf[32];
	puts("Where would you like to send your package?\n");
	puts("Some Options:\n0 Address Avenue\n1 Buffer Boulevard\n2 Canary Court\n");

	gets(buf);	
	if(!strcmp(buf, "0 Address Avenue")) {
		puts("Delivering to 0 Address Avenue...\n");
		avenue();	
	} else if(!strcmp(buf, "1 Buffer Boulevard")) {
		puts("Delivering to 1 Buffer Boulevard...\n");
		boulevard();
	} else if(!strcmp(buf, "2 Canary Court")) {
		puts("Delivering to 2 Canary Court...\n");
		court();
	} else {
		puts("Sorry, we couldn't deliver your package. Returning to sender...\n");
	}
}

int main(int argc, char** argv) {
	setbuf(stdout, NULL);
	setbuf(stdin, NULL);
	setbuf(stderr, NULL);

	puts("Our modern and highly secure postal service never fails to deliver your package.\n");
	deliver();
	return 0;
}
