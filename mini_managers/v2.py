vault = {}

while True:
    print("\nOptions: add / get / list / exit")
    action = input("what do you want to do?").lower()

    if action == "add":
        website = input("Enter the website name: ")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        vault[website] = {"username": username, "password": password}
        print(f"credentials for {website} added!")
    
    elif action == "get":
        website = input("Enter the website to retrieve: ")
        if website in vault:
            creds = vault[website]
            print(f"Username: {creds['username']}, Password: {creds['password']}")
        else:
            print(f"No credentials foound for {website}")

    elif action == "list":
        if vault:
            print("Websites Stored in Vault:")
            for site in vault:
                print("-", site)
        else:
            print("Vault is Empty")

    elif action == "exit":
        print("Exiting......")
        break

    else:
        print("Invalid Option Try Again")