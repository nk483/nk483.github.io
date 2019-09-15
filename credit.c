#include <cs50.h>
#include <stdio.h>
int main(void) 
{
    long number = get_long("Number: ");
    long copy = number;
    long secondcopy = number;
    long thirdcopy = number;
    int sum = 0;
    int digit = 0;
    bool checksum = false;
    while (copy > 0) 
    {
        copy = copy / 10;       
        digit = 2*(copy % 10);
        sum += digit % 10;
        sum += digit / 10;    
        copy = copy/10;        
    }
    
    while (secondcopy > 0)
    {
        digit = secondcopy % 10;
        sum += digit % 10;
        sum += digit / 10;    
        secondcopy = secondcopy/100;
    } 
    if (sum % 10 == 0) 
    {
        checksum = true;
    }
    while (thirdcopy >= 100) 
    {
        thirdcopy = thirdcopy / 10;
    }
    if ((thirdcopy == 34 || thirdcopy == 37) && checksum) 
    {
        printf("AMEX\n");
    }
    else if ((thirdcopy == 51 || thirdcopy == 52 || thirdcopy == 53 || thirdcopy == 54 || thirdcopy == 55)&& checksum) 
    {
        printf("MASTERCARD\n");
    }
    else if (thirdcopy / 10 == 4 && checksum) 
    {
        printf("VISA\n");
    }
    else 
    {
        printf("INVALID\n");
    }
}
