from sys import argv
import csv
import cs50
def main():
    if len(argv) != 2:
        print("Usage: Name of CSV file")
    db = cs50.SQL("sqlite:///students.db")
    db.execute("DELETE FROM students")
    with open(argv[1],"r") as characters:
        reader = csv.DictReader(characters)
        for row in reader:
            name = row["name"]
            if name.count(' ') == 1:
                firstName, lastName = name.split()
                db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?,?,?,?,?)", firstName, None, lastName, row["house"], row["birth"])
            else:
                firstName, middleName, lastName = name.split()
                db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?,?,?,?,?)", firstName, middleName, lastName, row["house"], row["birth"])
main()
