import hashlib
import pickle

def main():
    passdict = dict()
    lines = set() #intermediate storage for unhashed passwords.

    while True: # collect the password list and store it as a set of unique passwords for later manipulation
        filename = input("Enter the name of a password list file: ")
        try:
            with open(filename,"r") as file:
                # ignore lines that contain utf-8 non-complaint characters
                try:
                    for line in file:
                        lines.add(line.rstrip("\n")) # strip off newline characters
                except UnicodeDecodeError:
                    print("UTF-8 non-complaint character detected, ignoring password")
                break
        except FileNotFoundError: # handle a missing password list file and return to the top of the loop
            print("No password list found, please provide a password list.")

    salt = input("Enter the password salt: ") # ask the user if there is a known salt that was used to hash the passwords
    if salt != "": # if there is a salt, build our lookup table using every possible salt position
        for password in lines:
            for i in range(len(password)):
                candidate = password[:i] + salt + password[i:]
                passdict[hashlib.md5(candidate.encode()).hexdigest()] = (password, "md5")
                passdict[hashlib.sha1(candidate.encode()).hexdigest()] = (password, "Sha-1")
    else: # if there is no salt, simply hash the password list
        for password in lines:
            passdict[hashlib.md5(password.encode()).hexdigest()] = (password, "md5")
            passdict[hashlib.sha1(password.encode()).hexdigest()] = (password, "Sha-1")

    with open("passwordDict.pkl","wb") as file: # store the dictionary in a file as binary.
        pickle.dump(passdict, file)
    print("Password hash table written to file 'passwordDict.pkl'.\n")


if __name__ == "__main__":
    main()