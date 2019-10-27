from cs50 import get_string
def main():
    number = get_string("Number: ")
    sum = 0
    twoDigit = int(number[:2])
    for i in range(len(number) - 2, -1, -2):
        digit = int(number[i])
        digit = 2 * digit
        sum += digit // 10
        sum += digit % 10
    for i in range(len(number) - 1, -1, -2):
        digit = int(number[i])
        sum += digit
    if sum % 10 != 0:
        print("INVALID")
        return
    if (twoDigit == 34 or twoDigit == 37) and len(number) == 15:
        print("AMEX")
        return
    elif len(number) == 16 and (twoDigit <= 55 and twoDigit >= 51):
        print("MASTERCARD")
        return
    elif (len(number) == 16 or len(number) == 13) and int(number[0]) == 4:
        print("VISA")
        return
    else:
        print("INVALID")
        return
main()






