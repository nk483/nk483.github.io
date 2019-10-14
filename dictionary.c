// Implements a dictionary's functionality
//Idk how to free local variables of one function from another function.

#include <stdbool.h>

#include "dictionary.h"

#include <stdlib.h>

#include <stdio.h>

#include <strings.h>

#include <ctype.h>

#include <string.h>

// Represents a node in a hash table
typedef struct node
{
    char value[LENGTH + 1];
    struct node *next;
}
node;

FILE*file;

char *unfinishedWord = "";
char *finishedWord = "";

char memoryDict[144091][50];


// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    for (int i = 0; i < 144091; i++)
    {
        if (strcasecmp(memoryDict[i], word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int ascii = word[0];
    ascii = tolower(ascii);
    ascii = ascii - 65;
    ascii = ascii % 26;
    return ascii;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //  if (fopen(dictionary, "r") == NULL)
    // {
    //     return false;
    // }
    file = fopen(dictionary, "r");
    int j = 0;
    int k = 0;
    char c[1];
    unfinishedWord = malloc(50);
    finishedWord = malloc(50);
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

    // for (int i = 0; i < 26; i++)
    // {
    //     table[i] = NULL;
    // }
    // node *append = malloc(sizeof(node)+50);
    // node *currentLink = malloc(sizeof(node)+50);
    // append->next = malloc(sizeof(node));
    // currentLink->next = malloc(sizeof(node));
    // int a = 0;
    // int b = 0;
    // int index = 0;
    // while (memoryDict[a][0] != 0)
    // {
    // index = hash(memoryDict[a]);
    // currentLink = table[index];
    // append->next = currentLink->next;
    // strcpy(append->value,memoryDict[a]);
    // currentLink->next = append;
    // a++;
    // }
    fclose(file);
    return true;
}
// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    int counter = 0;
    int i = 0;
    while (memoryDict[i][0] != 0)
    {
        counter++;
        i++;
    }
    return counter;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    free(unfinishedWord);
    free(finishedWord);
    return true;
}