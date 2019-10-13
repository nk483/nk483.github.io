#include "stdio.h"
#include "stdlib.h"
#include "string.h"
int main(int argc, char* argv[])
{
    char *dictionary = "dictionaries/large";
    FILE *file = fopen(dictionary, "r");
    char memoryDict[144091][50];
    int j = 0;
    int k = 0;
    char* unfinishedWord = malloc(sizeof(char)*45);
    char* finishedWord = malloc(45);
    char c[1];
    while(!feof(file))
    {
        fread(c, 1, 1, file);
        while (c[0] != 32 && c[0] != 0 && c[0] != 10)
        {
           unfinishedWord[k] = c[0];
           k++;
           fread(c,1,1,file);
        }
        for (int i = 0; i < 46; i++)
        {
            finishedWord[i] = unfinishedWord[i];
        }
        for (int i = 0; i < 46; i++)
        {
        memoryDict[j][i] = finishedWord[i];
        }
        for (int i = 0; i < 46; i++)
        {
            unfinishedWord[i] = 0;
        }
        for (int i = 0; i < 46; i++)
        {
            finishedWord[i] = 0;
        }
        k = 0;
        j++;

    }
    int v = 0;
    printf("His \n");
    for (int i = 0; i < 10; i++)
    {
        while(memoryDict[i][v] != 0)
        {
        printf("%c", memoryDict[i][v]);
        v++;
        }
        printf("\n");
        v = 0;
    }
}