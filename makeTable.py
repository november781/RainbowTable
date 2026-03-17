import hashlib
import pickle
import hashcompare

def main():
    passdict = dict()

    while True:
        filename = input("Enter the name of a password list file: ")
        try:
            with open(filename,"r") as file:
                lines = file.readlines()
                break
        except FileNotFoundError:
            print("No password list found, please provide a password list.")

    salt = input("Enter the password salt: ")
    for password in lines:
        newpass = password.rstrip("\n")
        for i in range(len(newpass)):
            candidate = newpass[:i] + salt + newpass[i:]
            passdict[hashlib.md5(candidate.encode()).hexdigest()] = (newpass, "md5")
            passdict[hashlib.sha1(candidate.encode()).hexdigest()] = (newpass, "Sha-1")

    with open("passwordDict.pkl","wb") as file:
        pickle.dump(passdict, file)
    print("Password hash table written to file 'passwordDict.pkl'.\n"
          "Now running 'hashcompare.py'...........................\n"
          ".......................................................")

    hashcompare.main()


if __name__ == "__main__":
    main()