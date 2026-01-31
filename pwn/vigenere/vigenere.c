#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

bool isWhitespace(char test){
    if(test >= '0' && test <= '9') return true;
    switch(test){
        case ' ':
            return true;
        case '\t':
            return true;
        case '\n':  
            return true;
        case '\r':
            return true;
        case '\0':
            return true;
        default:
            return false;
    }
}

void encrypt(char* plain, char* key, char* cipher){
    int keyLen = strlen(key);
    int plnLen = strlen(plain);
    for(int i = 0, j = 0; (i + j) <= plnLen; i++){
        if(isWhitespace(plain[i + j])){
            cipher[i + j] = plain[i + j];
            j++; i--;
        }
        else if(key[i % keyLen] == 'A'){
            cipher[i + j] = plain[i + j];
        }
        else{
            char temp = plain[i + j];
            temp -= 'A';
            temp += key[i % keyLen] - 'A';
            temp %= 26;
            temp += 'A';
            cipher[i+j] = temp;
        }
    }
}

void getPlaintext(char* buffer){
    void* tempPtr = malloc(1024);
    char* tempBuf = (char*)tempPtr;
    printf("Enter Text:\n");
    gets(tempBuf);
    int len = strlen(tempBuf);
    for(int i = 0; i < len; i++){
        if(tempBuf[i] >= 'a' && tempBuf[i] <= 'z') tempBuf[i] -= 32;
        buffer[i] = tempBuf[i];
        }
    free(tempPtr);    
}

void getKey(char* buffer){
    void* tempPtr = malloc(1024);
    char* tempBuf = (char*)tempPtr;
    printf("Enter Text:\n");
    gets(tempBuf);
    int len = strlen(tempBuf);
    int i = 0;
    for(int j = 0; (i + j) < len; i++){
        if(tempBuf[i + j] >= 'A' && tempBuf[i + j] <= 'Z') buffer[i] = tempBuf[i + j];
        else if(tempBuf[i + j] >= 'a' && tempBuf[i + j] <= 'z') buffer[i] = tempBuf[i + j] - 32;
        else{j++; i--;}
        }
    buffer[i] = '\0';
    free(tempPtr);    
}

void print_flag(){
    char flag[64];
    FILE *f = fopen("flag.txt", "r");
    if (f == NULL) {
        printf("Flag file missing!\n");
        exit(1);
    }
    fgets(flag, 64, f);
    printf("\n%s\n", flag);
    fclose(f);
}

int main() {
    bool running = true;
    char result[1024];
    char* bufTxt;
    char* bufKey;
    char *res = &result[0];
    
    bufTxt = (char*)malloc(1024);
    bufKey = (char*)malloc(1024);
    if(bufTxt == 0 || bufKey == 0) return 1;
    
    while(running){
        printf("0: Input Plaintext\n1: Input Key\n2: Encrypt Message\n3: Quit\nSelect Option: ");
        fflush(stdout);
        int option;
        scanf("%d", &option);
        getchar();
        switch(option) {
            case 0:
                getPlaintext(bufTxt);
                break;
            case 1:
                getKey(bufKey);
                break;
            case 2:
                encrypt(bufTxt, bufKey, res);
                printf("%s\n", res);
                break;
            case 3:
                running = false;
                break;
        }
    }
    return 0;
}