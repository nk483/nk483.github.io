#include <stdbool.h>

#include <stdlib.h>
bool load(const char *dictionary);
int main(int argc, char *argv[])
{
    bool test = load("dictionaries/large");
}
    bool load(const char *dictionary)
{
    char **memoryDict = malloc(sizeof(char)*sizeof(dictionary)*10);
    int j = 0;
    int counter = 0;
    int k = 0;
    char* unfinishedWord = malloc(sizeof(char)*45);
    for (int i = 0; i < sizeof(dictionary); i++)
    {
        while (dictionary[i] != 32)
        {
           unfinishedWord[k] = dictionary[i];
           k++;
        }
        memoryDict[j] = unfinishedWord;
        k = 0;
        counter++;

    }
    if (counter == sizeof(dictionary))
    {
        return true;
    }
    return false;
}