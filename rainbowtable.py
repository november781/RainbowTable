import hashlib
import os
import pickle
import gzip


def make_table(lines: set, *, salt = None, passwords:dict = None):
    if passwords is None:
        passwords = dict()
    if salt is None:
        for password in lines:
            passwords[hashlib.md5(password.encode()).hexdigest()] = (password, "md5")
            passwords[hashlib.sha1(password.encode()).hexdigest()] = (password, "Sha-1")
    else:
        for password in lines:
            for i in range(len(password)):
                candidate = password[:i] + salt + password[i:]
                passwords[hashlib.md5(candidate.encode()).hexdigest()] = (password, "md5")
                passwords[hashlib.sha1(candidate.encode()).hexdigest()] = (password, "Sha-1")

    return passwords

def set_from_file(file, *, lines: set=None):
    if lines is None:
        lines = set()
    with open(file, "r") as file:
        try:
            for line in file:
                lines.add(line.rstrip("\n"))  # strip off newline characters
        except UnicodeDecodeError:
            #print("UTF-8 non-complaint character detected, ignoring this password")
            pass # ignore lines with non-complaint characters
        except FileNotFoundError:
            print("File disappeared between last check and now, exiting")
            exit()
    return lines

def check_file(filename):
    if os.path.isfile(filename):
        return True
    else:
        return False

def check_password(passwords:dict):
    candidate = input("Enter a password hash to crack: ")
    while True:
        if candidate in passwords:
            print("The password is: \"" + passwords[candidate][0] + "\" and the hash used to make it is: " +
                  passwords[candidate][1])
        else:
            print("The password is not in the table")
        candidate = input("If you want to crack another password enter the hash, or press 0 to exit: ")
        if candidate == "0":
            break

def main():
    salt = input("Enter the salt used to encode these passwords (press enter if no salt was used): ").strip()
    if salt == '':
        salt = None
    passwords_file = input("Enter the password list file: ")
    while not check_file(passwords_file):
        passwords_file = input("no such file exists, please enter a password list file or press 0 to exit: ")
        if passwords_file == "0":
            exit()

    if check_file("passwordDict.pkl.gz"):
        print("Password hash table found would you like to:\n"
              "\t1. replace this hash table with a new one?\n"
              "\t2. append new password hashes to this table?\n"
              "\t3. use the existing table as is?")
        selection = input("Enter the number corresponding to your choice: ")
        while selection != "1" and selection != "2" and selection != "3":
            selection = input("invalid selection. Please enter either 1, 2, or 3: ")
    else:
        selection = "1"
    pw_set = set_from_file(passwords_file)

    match selection:
        case "1":
            print("Prepping password hash table, this may take a while...", end="")
            passwords = make_table(pw_set, salt=salt)
            print(" done")
        case "2":
            print("Loading found hash table...", end="")
            with gzip.open("passwordDict.pkl.gz", "rb") as file:
                passwords = pickle.load(file)
            print(" hashing new passwords...", end="")
            passwords = make_table(pw_set, salt=salt, passwords=passwords)
            print(" done")
        case "3":
            print("Loading the password hash table...", end="")
            with gzip.open("passwordDict.pkl.gz", "rb") as file:
                passwords = pickle.load(file)
            print(" done")

    check_password(passwords)

    match selection:
        case "1":
            selection = input("Do you want to save the hash table for future use? (y/n): ").strip().lower()
        case "2":
            selection = input("Do you want to update the hash table on disk? (y/n): ").strip().lower()
        case _:
            exit()

    match selection:
        case "y":
            print("Saving hash table...", end="")
            with gzip.open("passwordDict.pkl.gz", "wb") as file:
                pickle.dump(passwords, file)
            print(" done")
            exit()
        case "n":
            exit()


if __name__ == '__main__':
    main()
