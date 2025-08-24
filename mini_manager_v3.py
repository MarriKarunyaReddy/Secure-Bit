import json
import os

VAULT_FILE = "vault.json"

if os.path.exists(VAULT_FILE):
    with open(VAULT_FILE, "r") as f:
        vault = json.load(f)
else:
    vault = {}

while True:
    print("\nOptions : add / get / list / exit")
    action = input("what do you want to do? ").lower()

    if action == "add":
        website = input("Enter the website name: ")
        username = input("Enter the username: ")
        password = input("Enter the Password: ")
        vault[website] = {"username": username, "password": password}

        with open(VAULT_FILE, "w") as f:
            json.dump(vault, f, indent=3)

        print(f"Credentials for {website} added and saved!")
    
    elif action == "get":
        website = input("Enter the Website to retrive Creds: ")
        if website in vault:
            creds = vault[website]
            print(f"Website: {website}, Username: {creds['username']}, Password: {creds['password']}")
        else:
            print("No credentials found for this website")
    
    elif action == "list":
        if vault:
            print("Websites stored in vault:")
            for site in vault:
                print("-", site)

    elif action == "exit":
        print("Exiting........")
        break

    else:
        print("Invalid Option, Try again")


    