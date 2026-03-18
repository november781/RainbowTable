# written to help test rainbowtable.py
# picks a random password out of the password list
# salts the password in a random location with the supplied salt
# hashes the password

import os
import hashlib
from random import randint

filename = input("Enter the password list file name: ")
if os.path.exists(filename):
    lines = list()
    with open(filename, "r") as f:
        try:
            for line in f:
                lines.append(line.rstrip("\n"))  # strip off newline characters
        except UnicodeDecodeError:
            #print("UTF-8 non-complaint character detected, ignoring this password")
            pass # ignore lines with non-complaint characters

else:
    print("File not found")
    exit()

password = lines[randint(0, len(lines) - 1)]

salt = input("Enter the salt to use in hashing this password: ")

i = randint(0, len(password) - 1)
salted = password[:i] + salt + password[i:]

print("The md5 hash of this password with the salt is: " + hashlib.md5(salted.encode()).hexdigest()
      +"\nThe Sha-1 hash of this password with the salt is: " + hashlib.sha1(salted.encode()).hexdigest() )