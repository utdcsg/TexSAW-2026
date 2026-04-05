0. This is a mostly static function so i reccomend using ghidra to examine or some other diassembler
1. Understand that the string needed for the challenge is 27 characters meaning including texsaw and {} removes 8 so 19 characters needed.
2. See how it is checking ascii codes and what numbers you needed to put that postion to get a certain code.
For example 
temp2[0] = hexcheck(pass[7] - 43);
temp2[1] = hexcheck(pass[25] - 49);
you need to get  the number at pass[7] - 43 to equal the ascii for 3 and at postion 24 you need the number -49 to equal the ascii for 4
3. next is to check what file is being checked to read to get these numbers which is asking for README.txt so you understand what characters you need for the string is assembled.

4. After noticing these numbers you can build your temp string which is the result of it gettign shuffled. This string is 
0    1   2   3 4   5   6 7   8   9   10 11  12   13 14 15 16 17 18 19 20    21   22  23   24  25 26 
115 101 105 30 ? -114 51 98 127 96  38  -85  49  ?  ?  ?  ?  ?  ?  ?  ?    118  65  -82  49  101 -64
it should thsi be calculated. Now understanding that you can start going through the function actually does most of the function.
P.s. the next ones for 20 and 13 are -75 and  115

5.
Finally you need to reserve the switcheroo function which is two parts. Moving of the pieces and adding and subtracting of numbers in a order
The first switching is easy just reverse the direction of the shift  or what was similar and esier to me was instead of shifting it to the right 4  shift the numbers so it would wrap around to orginal place before 4. For example you have 
randomize(pass, 7);
 make it shift 20 to go back to the orginal place
 orginal function but modified to go back to the previous one that was modified. 
 void shift(char* pass, int num ){
    num = 27 - num
    int temp= 0;
    char copy[29];
    strcpy(copy, pass);
    copy[28]= '\0';
    for(int i = 0; i < 27; i++){
        pass[(i+ num) % 27] = copy[i];
    }
    pass[27]= '\0';
}
6. Once shift is dealt with  you have to deal with the adding and subtracting.  this is just flip the sign but keep the same position that is calculated. Also do not forget they either subtract or add and when they shift depending if the number is even or odd.

finished function should look like
void randomize(char* pass, int num){
    if(num % 2 == 0){
        shift(pass , num);
        for(int i = 0; i < num; i++){
         pass[(i*num) % 27] -= num;
            
        }
    }
    else{
        for(int i = 0; i < num; i++){
            pass[(i+num) % 27] += num;
        }
        shift(pass , num);
    }
}

7. Once you have made your reverse functions you can start checking string characters which are mostly texsaw but there is one still  unknown in the main string 
pass[14] - 20 == '>' which should be number 82 at time of check.

8. Once you have gone through all the reversal that are called to orginal function you can check your flag by entering the flag and having a README.txt file with text W4a) inside
