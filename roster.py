import cs50
from sys import argv
def main():
    # Checking that the correct number of cmd line args were entered
    if len(argv) != 2:
        print("Usage: House")
        return
    # Setting database equal to our student database
    db = cs50.SQL("sqlite:///students.db")
    #This creates a dictionary with corresponding values
    output = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", argv[1])
    #Need to separate logic flow based on presence of middle name
    for line in output:
        if line["middle"] != None:
         print(line["first"] + " " + line["middle"] + " " + line["last"] + ", " + "born " + str(line["birth"]))
        else:
            print(line["first"] + " " + line["last"] + ", " + "born " + str(line["birth"]))
main()
