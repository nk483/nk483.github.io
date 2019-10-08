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
    char *jpegName = malloc(8 * sizeof(char));
    //This will store each jpeg, I'm giving it the memory of the entire file just in case there is one huge jpeg
    FILE *jpeg = malloc(sizeof(file));
    int jpegCounter = 0;
    //To make sure fclose does not execute the first time the jpeg Marker is found
    bool firstJpeg = false;
    // While not at end of file
    while (!feof(file))
    {
        //Reading blocks of 512 bytes of card.raw
        fread(blockSize, 1, 512, file);
        // jpeg Marker condition
        if (blockSize[0] == 255 && blockSize[1] == 216 && blockSize[2] == 255 && (blockSize[3] < 240 && blockSize[3] >= 224))
        {
            if (firstJpeg)
            {
                fclose(jpeg);
            }
            // So that the name of each jpeg file increments with each new jpeg, "000.jpg", "001.jpg" etc.
            sprintf(jpegName, "%03i.jpg", jpegCounter);
            jpeg = fopen(jpegName, "a");
            // Now after the loop has run once there is nothing to worry about with fclose and fwrite
            firstJpeg = true;
            jpegCounter++;

        }
        if (firstJpeg)
        {
            fwrite(blockSize, 1, 512, jpeg);
        }
    }
    //Freeing the two malloc file pointers as well as closing jpeg for the final time
    free(jpegName);
    fclose(jpeg);
    free(jpeg);
    return 0;

}

