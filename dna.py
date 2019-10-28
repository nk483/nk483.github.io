from sys import argv
from csv import reader
def main():
    #Throws error if wrong number of command line args
    if len(argv) != 3:
        print("Usage: Database, DNA Sequence")
        return 1
    #reader object
    database = reader(open(argv[1]), delimiter = ',')
    #first line of csv file, all of the column names
    codes = next(database)
    codes.remove("name")
    longCode = max(codes, key=len)
    codeCount = [0]*(len(codes))
    tmpCodeCount = [0]*(len(codes))
    stringCounts = {}
    k = 0
    n = 0
    noMatch = True
    #Person's name is the key, pattern frequencies are the corresponding key values
    for row in database:
        stringCounts[row[0]] = row[1:len(row)]
    text = open(argv[2],"r")
    pattern = ""
    char = ''
    while True:
        #If pattern has gotten bigger than the longest code, we make it blank and go to the index it started at plus 1
        if len(pattern) > len(longCode):
            pattern = ""
            k += 1
            text.seek(k)
            n = k
            for j in range(0, len(tmpCodeCount)):
                tmpCodeCount[j] = 0
        #Reads txt file character by character
        char = text.read(1)
        n += 1
        if char == "":
            break
        pattern = pattern + char
        for i in range(0, len(codes)):
            if pattern == codes[i]:
                for j in range(0, len(tmpCodeCount)):
                    if j == i:
                        continue
                    tmpCodeCount[j] = 0
                tmpCodeCount[i] += 1
                codeCount[i] = max(codeCount[i], tmpCodeCount[i])
                pattern = ""
                text.seek(n)
                k = n
    for i in range(0, len(codeCount)):
        codeCount[i] = str(codeCount[i])
    print(codeCount)
    print(stringCounts)
    for key in stringCounts:
        if stringCounts[key] == codeCount:
            print(key)
            noMatch = False
    if noMatch:
        print("No match")


main()




