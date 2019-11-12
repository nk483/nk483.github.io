#include <stdbool.h>
#include <stdio.h>

typedef unsigned char BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./count INPUT\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (!file)
    {
        printf("Could not open file.\n");
        return 1;
    }
    // To store skipped over bytes
    char *trashcan[3];

    int count = 0;
    while (true)
    {
        BYTE b;
        fread(&b, 1, 1, file);
        if (feof(file))
        {
            break;
        }
        //If the ascii code was less than 128 then only one byte was needed to represent using UTF-8
        if (b < 128)
        {
            count++;
        }
        //If the ascii code was between 194 and 223 then two bytes were needed so we skip over the next byte as we know it pertain to a character already counted
        else if (b >= 194 && b <= 223)
        {
            count++;
            fread(trashcan,1,1,file);
        }
        else if (b >= 224 && b <= 239)
        {
            count++;
            fread(trashcan,1,2,file);
        }
        else
        {
            count++;
            fread(trashcan,1,3,file);

        }
    }
    printf("Number of characters: %i\n", count);
}