#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height = 0;
    //Gets height as input from user
    do 
    {
        height = get_int("Input an integer from 1-8 for the pyramid's height: ");
    }
    //Condition to make sure input is from 1-8, otherwise it re-asks user for height
    while (!(height > 0 && height < 9));
    int dummyheight = height;
    int length = 4;
    for (int i = 0; i < height; i++) 
    {
        //This loop is so that the hashtags have space to fan out to the left
        for (int k = 0; k < dummyheight - 1; k++) 
        {
            printf(" ") ;
        }
        for (int j = 0; j < length; j++) 
        { 
            //This if statement is to implement the gap in middle of each pyramid line
            if (j == length / 2 - 1) 
            {
                printf("  ");
                j += 2;
            }
            printf("#");
        }
        printf("\n");
        length = length + 2;
        dummyheight--;
    }
    
}
