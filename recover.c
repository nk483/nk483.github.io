#include <stdio.h>
#include <stdlib.h>



int main(int argc, char *argv[])
{
    // Handles an incorrect number of command line arguments
    if (argc != 2)
    {
        printf("Correct Usage: image file name");
        return 1;
    }
    // Handles an input file that cannot be read
    if (fopen(argv[1], "r") == NULL)
    {
        printf("File could not be read");
        return 2;
    }

    FILE *file = fopen(argv[1], "r");
    // To read the input in blocks of 512 bytes
    unsigned char blockSize[512];

}

