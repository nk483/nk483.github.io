# include <cs50.h>
# include <stdio.h>
# include <string.h>
# include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Please input one command line argument\n");
        return 1;
    }
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }
    // Nested for loops to check every character of the CLA against every other one to make sure there are no duplicates
    for (int i = 0; i < 26; i++)
    {
        for (int k = i + 1; k < 26; k++)
        {
            if (argv[1][i] == argv[1][k])
            {
                printf("Please enter a key with no duplicate characters!\n");
                return 1;
            }
        }
    }
    for (int i = 0; i < 26; i++)
    {
        // Checks that all characters are either lowercase or uppercase letters
        if (!((argv[1][i] >= 65 && argv[1][i] <= 90) || (argv[1][i] >= 97 && argv[1][i] <= 122)))
        {
            printf("Please enter a key that is entirely comprised of letters!\n");
            return 1;
        }
    }
    string plaintext = get_string("Plaintext: ");
    int lettervalue = 0;
    int n = strlen(plaintext);
    // Went with an array of characters here because a string was giving some weird errors with DEADLYSIGNAL
    char array[n];
    char letter = 'a';
    // Turns the key into lowercase so the plaintext case isn't messed up
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        argv[1][i] = tolower(argv[1][i]);
    }
    for (int i = 0; i < n; i++)
    {
        lettervalue = plaintext[i];
        //Shifts by 97 to get to the corresponding letter of the key
        if (lettervalue >= 97 && lettervalue <= 122)
        {
            letter = argv[1][lettervalue - 97];
        }
        else if (lettervalue >= 65 && lettervalue <= 90)
        {
            letter = argv[1][lettervalue - 65];
            //To get back to uppercase
            letter -= 32;
        }
        else
        {
            letter = lettervalue;
        }
        //Populating the array of characters
        array[i] = letter;
    }
    //Going back to a string that can be printed
    string cipher = array;
    //Making sure the null character shows up after n characters
    cipher[n] = 0;
    printf("ciphertext: %s", cipher);
    printf("\n");
    return 0;
}