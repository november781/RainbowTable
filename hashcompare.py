import pickle

RAINBOWTABLE = dict()

def main():
    try:
        with open("passwordDict.pkl","rb") as file:
            RAINBOWTABLE = pickle.load(file)
    except FileNotFoundError:
        print("No password hash table found.\n"
              "Please run makeTable.py first to create one.")
        exit()

    while True:
        candidate = input("Please enter a password hash or 0 to exit: ")
        if candidate == "0":
            exit()
        else:
            if candidate in RAINBOWTABLE:
                print("The password is: \"" + RAINBOWTABLE[candidate][0] + "\" and the hash used to make it is: " +
                      RAINBOWTABLE[candidate][1])
            else:
                print("The password is not in the table")


if __name__ == "__main__":
    main()