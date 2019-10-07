#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Correct Usage: image file name");
        return 1;
    }
    if (fopen(argv[1], "r") == NULL)
    {
        printf("File could not be read");
        return 2;
    }
    unsigned char blockSize[512];
    int jpegNumber = 0;
    bool jpegMarker = true;
    char name[20];
    bool foundOneJpeg = false;

    FILE *jpeg = NULL;

    FILE *file = fopen(argv[1], "r");


    while (fread(blockSize, 512, 1, file) == 1)
    {

        if (blockSize[0] == 255 && blockSize[1] == 216 && blockSize[2] == 255)
        {
            if (foundOneJpeg)
            {
            fclose(jpeg);
            }
            foundOneJpeg = true;
            sprintf(name, "%i.jpg", jpegNumber);
            jpeg = fopen(name, "a");
            jpegNumber++;
        }
        if (foundOneJpeg)
        {
        fwrite(blockSize, 512, 1, jpeg);
        }


    }

    return 0;
}
