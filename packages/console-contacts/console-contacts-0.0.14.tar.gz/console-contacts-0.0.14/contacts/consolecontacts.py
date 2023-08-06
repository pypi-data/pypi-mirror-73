import pickle, colorama, argparse
from colorama import Fore
colorama.init(autoreset=True)

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--search", help="What you'd like to search comes after")
parser.add_argument("-l", "--list", action="store_true", help="Lists all contact names")
parser.add_argument("-a", "--add", nargs="+", help="Add a contact: name email [phone]")
parser.add_argument("-r", "--remove", nargs="+", help="Remove a contact: name email [phone]")

args = parser.parse_args()

def main():
    helpInfo = ""
    if args.search:
        print(f"{Fore.YELLOW}Searching for {args.search}...")
        try:
            pickleIn = open("contacts.pickle", "rb")
            users = pickle.load(pickleIn)
            pickleIn.close()
            for i in users:
                if i[0].lower() == args.search.lower():
                    user = i
                    return print(f"{Fore.GREEN}Name: {user[0]}\nEmail: {user[1]}\nPhone: {user[2]}")
            return print(f"{Fore.RED}No results for {args.search}")
        except: return print(f"{Fore.YELLOW}No contacts. Add some.")
    elif args.add:
        try:
            userName, userEmail = args.add[0], args.add[1]
            try:
                userPhone = args.add[2]
            except: userPhone = "No phone number"
        except: return print("Must provide at least first 2 arguments: name email [phone]")
        # if the file is empty/non-exisistent, or there is any error, we will set users to an empty list.
        try:
            pickleIn = open("contacts.pickle", "rb")
            users = pickle.load(pickleIn)
            pickleIn.close()
        except: users = []
        pickleOut = open("contacts.pickle", "wb")
        users.append((userName, userEmail, userPhone))
        pickle.dump(users, pickleOut)
        return pickleOut.close()
    elif args.remove:
        try:
            userName, userEmail = args.remove[0], args.remove[1]
            try:
                userPhone = args.remove[2]
            except: pass
        except: return print("Must provide at least first 2 arguments: name email [phone]")
        
        try:
            pickleIn = open("contacts.pickle", "rb")
            users = pickle.load(pickleIn)
            pickleIn.close()
        except: return print("No users to remove from db.")
        for i in users:
            if i[0] == args.remove[0] and i[1] == args.remove[1]:
                users.remove(i)
        pickleOut = open("contacts.pickle", "wb")
        pickle.dump(users, pickleOut)
        pickleOut.close()
    elif args.list:
        try:
            pickleIn = open("contacts.pickle", "rb")
            users = pickle.load(pickleIn)
            pickleIn.close()
        except: return print("No users in db to list")
        for i in users:
            print(f"{Fore.GREEN}{i[0]}")
    else: parser.print_help()

# if __name__ == "__main__": main()