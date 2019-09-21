#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
// Declaring my functions here, but the implementation is under main
int countLetters(string text);
int countWords(string text);
int countSentences(string text);
int main(void)
{
    string text = get_string("Text: ");
    // These three variables store the letters, words, and sentences of the text as gotten from the functions under main
    int lettercount = countLetters(text);
    int wordcount = countWords(text);
    int sentencecount = countSentences(text);
    // using casting so the remainder of the division isn't discarded
    double L = (lettercount / (double) wordcount) * 100;
    double S = (sentencecount / (double) wordcount) * 100;
    // The Coleman-Liau Equation
    int index = round(.0588 * L - 0.296 * S - 15.8);
    //There are three logical scenarios, either the index is less than one, greater than 15, or between 1 and 15. The print statements differ based on which scenario.
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 15)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }

}
int countLetters(string text)
{
    int counter = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // Makes sure counter augments when the character stored is an upper or lowercase letter but that's it
        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
        {
            counter++;
        }
    }
    return counter;
}
int countWords(string text)
{
    int n = strlen(text);
    int counter = 0;
    // The following if statement is because if the block of text doesn't start with a space the first word won't be counted by my loop
    if (text[0] != 32)
    {
        counter++;
    }
    for (int i = 0; i < n; i++)
    {
        // Checks that the current character is a space and the next one is not a space so that double spaces are not counted as two words
        if (text[i] == 32 && text[i + 1] != 32)
        {
            counter++;
        }

    }
    if (text[n - 1] == 32)
    {
        counter--;
    }
    return counter;
}
int countSentences(string text)
{
    int counter = 0;
    int n = strlen(text);
    for (int i = 0; i < n; i++)
    {
        // Checks that the character stored is a period, question mark, or exclamation point. Only then does counter augment.
        if (text[i] == 46 || text[i] == 33 || text[i] == 63)
        {
            counter++;
        }
    }
    return counter;
}