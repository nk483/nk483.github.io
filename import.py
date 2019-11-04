from sys import argv
import csv
import cs50
def main():
    # Checking that the correct number of cmd line args were entered
    if len(argv) != 2:
        print("Usage: Name of CSV file")
    # Setting database equal to our student database
    db = cs50.SQL("sqlite:///students.db")
    # Making sure students starts afresh every time this program is run, to not end up with a bunch of duplicates
    db.execute("DELETE FROM students")
    with open(argv[1],"r") as characters:
        reader = csv.DictReader(characters)
        for row in reader:
            name = row["name"]
            # I separate the logic flow here based on spaces in name, basically to separate based on whether or not there is a middle name
            if name.count(' ') == 1:
                firstName, lastName = name.split()
                db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?,?,?,?,?)", firstName, None, lastName, row["house"], row["birth"])
            else:
                firstName, middleName, lastName = name.split()
                db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?,?,?,?,?)", firstName, middleName, lastName, row["house"], row["birth"])
main()
