from datetime import datetime
import ast
from abc import ABC, abstractmethod

class BaseBook(ABC):
    @abstractmethod
    def to_dict(self):
        pass

class Book(BaseBook):
    def __init__(self, title, author, isbn, status, borrower):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._status = status
        self._borrower = borrower

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, value):
        self._isbn = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def borrower(self):
        return self._borrower

    @borrower.setter
    def borrower(self, value):
        self._borrower = value

    def to_dict(self):
        return {"Title": self._title, "Author": self._author, "ISBN": self._isbn, "Status": self._status, "Borrower": self._borrower}


class LibrarySystem:
    def __init__(self):
        f = open("library_management_system.txt", "a+")
        f.close()

    def showrecords(self):
        f = open("library_management_system.txt")
        a = f.read()
        print(a)
        f.close()

    def addbooks(self):
        f = open("library_management_system.txt", "a+")
        while True:
            try:
                b_name = input("Enter Book name:")
                b_author = input("Enter Author Name:")
                b_isbn = int(input("Enter ISBN code:"))
                b_status = input("Is book available?(y/n)")
                if b_status == "y":
                    b_status = "Available"
                    b_borrower = "N/A"
                elif b_status == "n":
                    b_status = "Not Available"
                    b_borrower = input("Enter name of borrower:")
                else:
                    print("Only enter y or n")
                    raise ValueError
                break
            except ValueError: 
                print("Try again")
        
        book = Book(b_name, b_author, b_isbn, b_status, b_borrower)
        d = book.to_dict()
        f.write(str(d) + "\n")
        f.flush()
        f.close()

    def fetchrecord(self):
        f = open("library_management_system.txt")
        a = f.readlines()
        x = 0
        while True:
            print('''How would you like to search records?
    * Search by Title: enter 1
    *Search by isbn: enter 2
     *Search by Status: enter 3''')
            try:
                b = int(input("Enter your Choice:"))
                if str(b) not in "123":
                    raise ValueError
                break
            except ValueError:
                print("Enter 1 ,2, or 3")
        
        while True:
            try:
                if b == 1:
                    c = input("Enter to search:").strip()
                    matches = []
                    for i in a:
                        if i.strip():
                            record = ast.literal_eval(i.strip())
                            if record["Title"].lower() == c.lower():
                                matches.append(i)
                    for i in matches:
                        print(i)
                        print("In Line:", a.index(i) + 1)
                        x += 1
                elif b == 2:
                    c = input("Enter to search:")
                    c = int(c)
                    matches = [i for i in a if "'ISBN': " + str(c) in i]
                    for i in matches:
                        print(i)
                        print("Line:", a.index(i) + 1)
                        x += 1
                elif b == 3:
                    print('''a- Enter 'a' to check available books
                b- Enter b to check borrowed books''')
                    c = input()
                    if c == "a":
                        c = "Available"
                    elif c == "b":
                        c = "Not Available"
                    else:
                        print("ONLY ENTER a or b!")
                        raise ValueError
                    matches = [i for i in a if "'Status': '" + str(c) + "'" in i]
                    for i in matches:
                        print(i)
                        print("Line:", a.index(i) + 1)
                        x += 1
                break
            except ValueError:
                print("Try again") 
        if x == 0:
            print("Not found")
        f.close()

    def avbook(self):
        f = open("library_management_system.txt")
        a = f.readlines()
        matches = [i for i in a if "'Status': 'Available'" in i]
        for i in matches:
            print(i)
            print("Line:", a.index(i) + 1)
        f.close()

    def issbook(self):
        f = open("library_management_system.txt", "r")
        l = f.readlines()
        f.close()
        if len(l) == 0:
            print("No books to issue")
            return
        while True:
            try:
                n = int(input("Which line do you want to update? "))
                if n > len(l) or n <= 0:
                    print("Only enter from 1 to", len(l))
                    raise ValueError
                else:
                    d_raw = ast.literal_eval(l[n - 1].strip())
                    book = Book(d_raw["Title"], d_raw["Author"], d_raw["ISBN"], d_raw["Status"], d_raw["Borrower"])
                    book.status = "Not Available"
                    book.borrower = input("Enter name of Borrower:")
                    l[n - 1] = str(book.to_dict()) + "\n"
                    break
            except ValueError:
                print("Try again!")
                  
        f = open("library_management_system.txt", "w")
        f.writelines(l)
        f.close()
        print("Book issued successfully.")

    def returnbook(self):
        f = open("library_management_system.txt", "r")
        l = f.readlines()
        f.close()
        if len(l) == 0:
            print("No books to return")
            return
        while True:
            try:
                n = int(input("Which line do you want to update? "))
                if n > len(l) or n <= 0:
                    print("Only enter from 1 to", len(l))
                    raise ValueError
                else:
                    d_raw = ast.literal_eval(l[n - 1].strip())
                    book = Book(d_raw["Title"], d_raw["Author"], d_raw["ISBN"], d_raw["Status"], d_raw["Borrower"])
                    book.status = "Available"
                    book.borrower = "N/A"
                    l[n - 1] = str(book.to_dict()) + "\n"
                    break
            except ValueError:
                print("Try again!")
                  
        f = open("library_management_system.txt", "w")
        f.writelines(l)
        f.close()
        print("Book returned successfully.")

    def deone(self, n):
        f = open("library_management_system.txt", "r")
        l = f.readlines()
        f.close()
        f = open("library_management_system.txt", "w")
        print("Removing ", l[n])
        del l[n]
        for i in l:
            f.write(i)
        f.flush()
        f.close()

    def delone(self):
        while True:
            try:
                f = open("library_management_system.txt", "r")
                l = f.readlines()
                f.close()
                n = int(input("Enter the Line number:"))
                print(l[n - 1], "to be deleted")
                if n > len(l) or n <= 0:
                    print("Only enter from 1 to", len(l))
                    raise ValueError
                a = input("ARE YOU SURE YOU WANT TO DELETE DATA?(y/n)")
                if a == "n":
                    print("NOT DELETED")
                    break
                elif a == "y":
                    print("DATA DELETED")
                    self.deone(n - 1)
                    break
                else:
                    raise ValueError
            except ValueError:
                print("Try again!")

    def deleteall(self):
        while True:
            try:
                a = input("ARE YOU SURE YOU WANT TO DELETE ALL DATAS?(y/n)")
                if a == "n":
                    print("NOT DELETED")
                elif a == "y":
                    print("ALL DATAS DELETED")
                    f = open("library_management_system.txt", "w")
                    f.close()
                else:
                    raise ValueError
                break
            except ValueError:
                print("Try again")  


if __name__ == "__main__":
    lms = LibrarySystem()
    while True:
        print('''\nLibrary
Management System
* 1 to see records
* 2 to add books
* 3 to search books
* 4 to search available books
* 5 to issue books
* 6 to return books
* 7 to remove a book 
* 8 to remove all books
* 9 to exit program''')
        
        try:
            choice = int(input("Enter your option (1-9): "))
            if choice == 1:
                lms.showrecords()
            elif choice == 2:
                lms.addbooks()
            elif choice == 3:
                lms.fetchrecord()
            elif choice == 4:
                lms.avbook()
            elif choice == 5:
                lms.issbook()
            elif choice == 6:
                lms.returnbook()
            elif choice == 7:
                lms.delone()
            elif choice == 8:
                lms.deleteall()
            elif choice == 9:
                print("Thank you for using the system. Goodbye!")
                break
            else:
                print("Invalid option. Please choose between 1 and 9.")
        except ValueError:
            print("Please enter a valid number selection.")
        finally:
            print('''*****************************************************************************************************************************
''')
