import tkinter as tk
from tkinter import messagebox
import json
import os

VAULT_FILE = "vault.json"

# Load or create vault
if os.path.exists(VAULT_FILE):
    with open(VAULT_FILE, "r") as f:
        vault = json.load(f)
else:
    vault = {}

# Save vault
def save_vault():
    with open(VAULT_FILE, "w") as f:
        json.dump(vault, f, indent=3)

# Custom input dialog
def ask_input(title, prompt, width=40):
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("400x150")
    win.config(bg="#1e1e2f")

    lbl = tk.Label(win, text=prompt, font=("Arial", 12), bg="#1e1e2f", fg="white")
    lbl.pack(pady=10)

    entry = tk.Entry(win, width=width, font=("Arial", 12))
    entry.pack(pady=5)
    entry.focus()

    value = {"text": None}

    def on_ok():
        value["text"] = entry.get()
        win.destroy()

    btn = tk.Button(win, text="OK", font=("Arial", 11, "bold"), bg="#4caf50", fg="white", command=on_ok)
    btn.pack(pady=10)

    win.grab_set()
    root.wait_window(win)
    return value["text"]

# Custom message box
def show_info(title, message):
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("400x200")
    win.config(bg="#1e1e2f")

    lbl = tk.Label(win, text=message, font=("Arial", 12), wraplength=380, justify="left", bg="#1e1e2f", fg="white")
    lbl.pack(padx=20, pady=20)

    btn = tk.Button(win, text="OK", font=("Arial", 11, "bold"), bg="#4caf50", fg="white", command=win.destroy)
    btn.pack(pady=10)

    win.grab_set()
    root.wait_window(win)

# Add credentials
def add_credentials():
    website = ask_input("Website", "Enter website name:")
    if not website: return
    username = ask_input("Username", "Enter your username:")
    if not username: return
    password = ask_input("Password", "Enter your password:")
    if not password: return

    vault[website] = {"username": username, "password": password}
    save_vault()
    show_info("Success", f"Credentials for {website} added!")

# Get credentials
def get_credentials():
    website = ask_input("Find Credentials", "Enter website name:")
    if not website: return

    if website in vault:
        creds = vault[website]
        show_info("Credentials Found", f"Website: {website}\nUsername: {creds['username']}\nPassword: {creds['password']}")
    else:
        show_info("Not Found", f"No credentials stored for {website}.")

# List websites (with view + delete)
def list_websites():
    if not vault:
        show_info("Vault", "No websites stored yet.")
        return

    win = tk.Toplevel(root)
    win.title("Stored Websites")
    win.geometry("450x450")
    win.config(bg="#1e1e2f")

    lbl = tk.Label(win, text="Stored Websites", font=("Arial", 14, "bold"), bg="#1e1e2f", fg="white")
    lbl.pack(pady=10)

    frame = tk.Frame(win, bg="#1e1e2f")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(frame, bg="#1e1e2f", highlightthickness=0)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#1e1e2f")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for site in vault.keys():
        row = tk.Frame(scrollable_frame, bg="#2a2a40", pady=5)
        row.pack(fill="x", pady=5, padx=5)

        lbl = tk.Label(row, text=site, font=("Arial", 12, "bold"), bg="#2a2a40", fg="white", anchor="w", width=18)
        lbl.pack(side="left", padx=5)

        def make_view(site_name):
            def view_site():
                creds = vault[site_name]
                show_info("Credentials", f"Website: {site_name}\nUsername: {creds['username']}\nPassword: {creds['password']}")
            return view_site

        def make_delete(site_name):
            def delete_site():
                confirm = messagebox.askyesno("Confirm Delete", f"Delete {site_name}?")
                if confirm:
                    del vault[site_name]
                    save_vault()
                    win.destroy()
                    list_websites()
            return delete_site

        btn_view = tk.Button(row, text="View", font=("Arial", 10, "bold"), bg="#2196f3", fg="white", command=make_view(site))
        btn_view.pack(side="right", padx=5)

        btn_del = tk.Button(row, text="Delete", font=("Arial", 10, "bold"), bg="#f44336", fg="white", command=make_delete(site))
        btn_del.pack(side="right", padx=5)

# ---------------- MAIN GUI ----------------
root = tk.Tk()
root.title("Password Manager")
root.geometry("450x500")
root.config(bg="#1e1e2f")

lbl = tk.Label(root, text="🔐 Password Manager", font=("Arial", 18, "bold"), bg="#1e1e2f", fg="white")
lbl.pack(pady=20)

btn_add = tk.Button(root, text="➕ Add Credentials", font=("Arial", 13, "bold"), command=add_credentials, width=20, height=2, bg="#4caf50", fg="white")
btn_add.pack(pady=10)

btn_get = tk.Button(root, text="🔎 Get Credentials", font=("Arial", 13, "bold"), command=get_credentials, width=20, height=2, bg="#2196f3", fg="white")
btn_get.pack(pady=10)

btn_list = tk.Button(root, text="📜 List Websites", font=("Arial", 13, "bold"), command=list_websites, width=20, height=2, bg="#ff9800", fg="white")
btn_list.pack(pady=10)

btn_exit = tk.Button(root, text="❌ Exit", font=("Arial", 13, "bold"), command=root.destroy, width=20, height=2, bg="#9c27b0", fg="white")
btn_exit.pack(pady=10)

root.mainloop()
