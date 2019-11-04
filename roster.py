import cs50
from sys import argv
def main():
    if len(argv) != 2:
        print("Usage: House")
        return
    db = cs50.SQL("sqlite:///students.db")
    output = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", argv[1])
    for line in output:
        if line["middle"] != None:
         print(line["first"] + " " + line["middle"] + " " + line["last"] + ", " + "born " + str(line["birth"]))
        else:
            print(line["first"] + " " + line["last"] + ", " + "born " + str(line["birth"]))
main()
