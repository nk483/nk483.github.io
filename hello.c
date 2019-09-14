#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Asks user for their name and stores it
    string name = get_string("What is your name?\n"); 
    //Prints hello, (name)
    printf("hello, %s\n",name);
}
