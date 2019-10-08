#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>



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
    char *jpegName = malloc(20*sizeof(char));
    FILE *jpeg = NULL;
    int jpegCounter = 0;
    bool firstJpeg = false;

    while (fread(blockSize, 1, 512, file) != -1)
    {
        if (blockSize[0] == 255 && blockSize[1] == 216 && blockSize[2] == 255 && (blockSize[3] < 240 && blockSize[3] >= 224))
        {
            if (firstJpeg)
            {
                fclose(jpeg);
            }
            sprintf(jpegName,"%i.jpg",jpegCounter);
            jpeg = fopen(jpegName,"a");
            firstJpeg = true;
            jpegCounter++;

        }
        if (firstJpeg)
        {
        fwrite(blockSize, 1, 512, jpeg);
        }
    }
    free(jpegName);
    fclose(jpeg);

}

