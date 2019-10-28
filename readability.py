from cs50 import get_string
def main():
    wordCount = 1
    sentenceCount = 0
    letterCount = 0
    score = 0
    L = 0
    S = 0
    text = get_string("Text: ")
    for char in text:
        # ord gets the ascii code of a char
        if ord(char) == 32:
            wordCount += 1
    for char in text:
        if (ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 97 and ord(char) <= 122):
            letterCount += 1
    for char in text:
        if (ord(char) == 33 or ord(char) == 46 or ord(char) == 63):
            sentenceCount += 1
    L = (letterCount/wordCount) * 100
    S = (sentenceCount/wordCount) * 100
    score = 0.0588 * L - 0.296 * S - 15.8
    #To get an integer grade level
    score = round(score)
    if score < 1:
        print("Before Grade 1")
    elif score >= 16:
        print("Grade 16+")
    else:
        # printf is print formatted since we have a variable inside what we're printing
        print(f"Grade {score}")


main()
