#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height = 0;
    int maxheight = 8;
    do {
       height = get_int("Input an integer from 1-8 for the pyramid's height: ");
    }
    while(!(height>0 && height<9));
    int length = 4;
    for(int i = 0;i<height;i++) {
        for(int k = 0; k<maxheight;k++) {
           printf(" ") ;
        }
            for(int j=0; j<length; j++) { 
                if (j == length/2-1) {
                    printf("  ");
                    j+=2;
                }
                printf("#");
            }
        printf("\n");
        length = length+2;
        maxheight--;
    }
    
}
