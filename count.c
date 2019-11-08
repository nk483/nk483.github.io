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
        if (b < 128)
        {
            count++;
        }
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