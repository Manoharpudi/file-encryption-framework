import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet
import base64
import hashlib

BG = "#000000"
CARD = "#0d0d0d"
RED = "#dc2626"
WHITE = "#ffffff"
GRAY = "#9ca3af"
HOVER = "#1f1f1f"

def get_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def status(msg, color=WHITE):
    status_label.config(text=msg, fg=color)

#ENCRYPT
def encrypt_file():
    file_path = filedialog.askopenfilename()
    password = password_entry.get()

    if not file_path or password == "":
        status("Select file & enter password", RED)
        return

    try:
        f = Fernet(get_key(password))
        data = open(file_path, "rb").read()
        encrypted = f.encrypt(data)

        with open(file_path + ".enc", "wb") as file:
            file.write(encrypted)

        status("✔ File Encrypted")

    except:
        status("Encryption failed", RED)

#DECRYPT
def decrypt_file():
    file_path = filedialog.askopenfilename()
    password = password_entry.get()

    if not file_path or password == "":
        status("Select file & enter password", RED)
        return

    try:
        f = Fernet(get_key(password))
        data = open(file_path, "rb").read()
        decrypted = f.decrypt(data)

        new_file = file_path.replace(".enc", "_decrypted")

        with open(new_file, "wb") as file:
            file.write(decrypted)

        status("✔ File Decrypted")

    except:
        status("Wrong password or file", RED)

def toggle_password():
    if password_entry.cget('show') == "*":
        password_entry.config(show="")
        eye_btn.config(text="🙈")
    else:
        password_entry.config(show="*")
        eye_btn.config(text="👁")

def create_btn(parent, text, cmd, color):
    return tk.Button(
        parent,
        text=text,
        command=cmd,
        bg=color,
        fg=WHITE,
        font=("Segoe UI", 12, "bold"),
        width=20,
        height=2,
        bd=0,
        cursor="hand2",
        activebackground=HOVER
    )

#UI
root = tk.Tk()
root.title("Secure Encryptor Pro")
root.state("zoomed") 
root.configure(bg=BG)

frame = tk.Frame(root, bg=CARD)
frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=420)

tk.Label(
    frame,
    text="SECURE ENCRYPTOR",
    font=("Segoe UI", 20, "bold"),
    bg=CARD,
    fg=RED
).pack(pady=20)

tk.Label(
    frame,
    text="Encrypt & Decrypt using Password",
    font=("Segoe UI", 11),
    bg=CARD,
    fg=GRAY
).pack()

password_frame = tk.Frame(frame, bg=CARD)
password_frame.pack(pady=15)

password_entry = tk.Entry(
    password_frame,
    show="*",
    font=("Segoe UI", 12),
    width=22,
    bd=0,
    justify="center"
)
password_entry.pack(side="left", padx=5)

eye_btn = tk.Button(
    password_frame,
    text="👁",
    command=toggle_password,
    bg=CARD,
    fg=WHITE,
    bd=0,
    font=("Segoe UI", 12),
    cursor="hand2"
)
eye_btn.pack(side="right")

encrypt_btn = create_btn(frame, "Encrypt File", encrypt_file, RED)
encrypt_btn.pack(pady=15)

decrypt_btn = create_btn(frame, "Decrypt File", decrypt_file, "#111111")
decrypt_btn.pack(pady=10)

status_label = tk.Label(
    frame,
    text="Enter password and choose action",
    font=("Segoe UI", 10),
    bg=CARD,
    fg=GRAY
)
status_label.pack(pady=20)

root.mainloop()