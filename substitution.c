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
    string plaintext = get_string("Plaintext: ");
    int lettervalue = 0;
    int n = strlen(plaintext);
    char array[n];
  //  string cipher = " ";
    char letter = 'a';

   for (int i = 0; i < strlen(argv[1]); i++)
   {
       argv[1][i] = tolower(argv[1][i]);
   }
   for (int i = 0; i < n; i++)
    {
       lettervalue = plaintext[i];
       if (lettervalue >= 97 && lettervalue <= 122)
       {
            letter = argv[1][lettervalue-97];
       }
       else if (lettervalue >= 65 && lettervalue <= 90)
       {
           letter = argv[1][lettervalue-65];
           letter -= 32;
       }
       else
       {
            letter = lettervalue;
       }
      array[i] = letter;
   }
    string cipher = array;
    cipher[n] = 0;
    printf("ciphertext: %s",cipher);
    printf("\n");
    return 0;
}