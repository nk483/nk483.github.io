#include <cs50.h>
#include <stdio.h>
int main(void) 
{
    // Prompts user for card number
    long number = get_long("Number: ");
    // Setting variables to the value of the number so I can make changes without changing the original value
    long copy = number;
    long secondcopy = number;
    long thirdcopy = number;
    long fourthcopy = number;
    int sum = 0;
    int digit = 0;
    int length = 0;
    bool checksum = false;
    //This loop does the first part of the checksum computation
    while (copy > 0) 
    {
        copy = copy / 10;       
        digit = 2 * (copy % 10);
        sum += digit % 10;
        sum += digit / 10;    
        copy = copy / 10;        
    }
    //This loop does the second part of the checksum computation
    while (secondcopy > 0)
    {
        digit = secondcopy % 10;
        sum += digit % 10;
        sum += digit / 10;    
        secondcopy = secondcopy / 100;
    } 
    // This loop does the final part of the checksum computation
    if (sum % 10 == 0) 
    {
        checksum = true;
    }
    while (thirdcopy >= 100) 
    {
        thirdcopy = thirdcopy / 10;
    }
    //Counts the number of digits the number has
    while (fourthcopy > 0) 
    {
        fourthcopy = fourthcopy / 10;
        length++;
    }
    //This condition says if the card starts with 34 or 37, passes the checksum, and has 15 digits, then it is an American Express card
    if ((thirdcopy == 34 || thirdcopy == 37) && checksum && length == 15) 
    {
        printf("AMEX\n");
    }
    else if ((thirdcopy == 51 || thirdcopy == 52 || thirdcopy == 53 || thirdcopy == 54 || thirdcopy == 55) && checksum && length == 16) 
    {
        printf("MASTERCARD\n");
    }
    else if (thirdcopy / 10 == 4 && checksum && (length == 13 || length == 16)) 
    {
        printf("VISA\n");
    }
    else 
    {
        printf("INVALID\n");
    }
}
