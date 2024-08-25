import tkinter as tk                    # Import the tkinter module for GUI
from tkinter import ttk, messagebox     # Import ttk for themed widgets and messagebox for alerts
from cryptography.fernet import Fernet  # Import Fernet from cryptography for encryption/decryption
from PIL import Image, ImageTk          # Import Image and ImageTk from PIL for handling images
import pyperclip                        # Import pyperclip for clipboard operations


class CryptographyApp:
#____________________________________________________*Encryption*______________________________________________________________________________________
    def __init__(self, master):
        self.master = master                # Store reference to the main window
        master.title("Encryption Window")   # Set the title of the main window
        master.geometry("800x600")          # Set the size of the main window
#----------------------------------------------------------------------------------------------------------------------
        # Set background image with error handling
        try:
            image = Image.open(r"D:\Downloads\1702839047405.jpg")  # Attempt to open the background image file
            photo = ImageTk.PhotoImage(image)                      # Convert the image to a format tkinter can display
            background_label = tk.Label(master, image=photo)       # Create a label to display the image
            background_label.image = photo                         # Keep a reference to avoid garbage collection
            background_label.place(relwidth=1, relheight=1)        # Make the image cover the whole window
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {e}")  # Show an error message if image loading fails
#-----------------------------------------------------------------------------------------------------------------------
        # Fernet key for encryption and decryption
        self.key = Fernet.generate_key()                           # Generate a new Fernet encryption key
        self.cipher = Fernet(self.key)                             # Create a Fernet object with the generated key
#-----------------------------------------------------------------------------------------------------------------------
        # Entry Style
        style = ttk.Style()                                        # Create a style object for ttk widgets
        style.configure("TEntry", foreground="black", background="#333333", font=("Helvetica", 12))  # Configure the style for entry widgets

        # UI Elements for User 1 (Encryption)
        self.label = tk.Label(master, text="Enter message to encrypt:", fg="red", background="yellow", font=("Helvetica", 12))  # Label prompting for encryption input
        self.label.pack(pady=10)                                   # Add padding around the label

        self.message_entry = ttk.Entry(master, style="TEntry", font=("Helvetica", 14))  # Entry widget for the message to be encrypted
        self.message_entry.pack(pady=10)                            # Add padding around the entry widget

        self.encrypt_button = tk.Button(master, text="Encrypt and Copy", command=self.encrypt_and_copy, bg="#007ACC", fg="black", font=("Helvetica", 12))  # Button to trigger encryption
        self.encrypt_button.pack(pady=5)                            # Add padding around the button

        self.encrypted_label = tk.Label(master, text="", fg="black", bg="#CCCCCC", font=("Helvetica", 10))  # Label to display the encrypted message
        self.encrypted_label.pack(pady=10)                          # Add padding around the label

        # Button to open the decryption window
        self.open_decrypt_window_button = tk.Button(master, text="Open Decrypt Window", command=self.open_decrypt_window, bg="#007ACC", fg="black", font=("Helvetica", 12))  # Button to open the decryption window
        self.open_decrypt_window_button.pack(pady=5)                # Add padding around the button

        # Create Decryption Window
        self.decrypt_window = None                                  # Initialize variable to track the decryption window
#--------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------~Auto Copy Text~----------------------------------------------------------------------
    def encrypt_and_copy(self):
        message = self.message_entry.get()                          # Get the message from the entry widget
        if not message:
            messagebox.showwarning("Warning", "Please enter a message to encrypt.")  # Show a warning if no message is entered
            return                                                  # Exit the method if no message is provided

        # Encrypt the message
        encrypted_message = self.cipher.encrypt(message.encode()).decode()  # Encrypt the message and convert it to a string

        # Display encrypted message
        self.encrypted_label.config(text=f"Encrypted Message: {encrypted_message}")  # Update the label with the encrypted message

        # Copy the encrypted message to the clipboard
        pyperclip.copy(encrypted_message)                           # Copy the encrypted message to the clipboard

        # Clear the entry field
        self.message_entry.delete(0, tk.END)                        # Clear the input field
#----------------------------------------------------------------------------------------------------------------------------
#_______________________________________________________*Decryption*___________________________________________________________________________________________
    def open_decrypt_window(self):
        if self.decrypt_window is None or not self.decrypt_window.winfo_exists():  # Check if the decryption window is not open
            # Create a new top-level window for decryption
            self.decrypt_window = tk.Toplevel(self.master)          # Create a new top-level window
            self.decrypt_window.title("Decryption Window")          # Set the title of the decryption window
            self.decrypt_window.geometry(self.master.geometry())    # Set size to match the main window
#-----------------------------------------------------------------------------------------------------------------------------
            # Set background image for the decryption window
            try:
                image = Image.open(r"D:\Downloads\hack.png")                   # Attempt to open the background image file for the decryption window
                photo = ImageTk.PhotoImage(image)                              # Convert the image to a format tkinter can display
                background_label = tk.Label(self.decrypt_window, image=photo)  # Create a label to display the image
                background_label.image = photo                                 # Keep a reference to avoid garbage collection
                background_label.place(relwidth=1, relheight=1)                # Make the image cover the whole window
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {e}")    # Show an error message if image loading fails
#------------------------------------------------------------------------------------------------------------------------------
            # Decryption tab UI elements
            decrypt_label = tk.Label(self.decrypt_window, text="Paste encrypted message:", fg="white", bg="#333333", font=("Helvetica", 16))  # Label prompting for the encrypted message
            decrypt_label.pack(pady=10)                                        # Add padding around the label

            self.encrypted_entry = ttk.Entry(self.decrypt_window, width=50, font=("Helvetica", 14))  # Entry widget for pasting the encrypted message
            self.encrypted_entry.pack(pady=5)                                  # Add padding around the entry widget

            decrypt_button = tk.Button(self.decrypt_window, text="Decrypt", command=self.decrypt, bg="#007ACC", fg="white", font=("Helvetica", 14))  # Button to trigger decryption
            decrypt_button.pack(pady=5)                                        # Add padding around the button

            self.decrypted_label = tk.Label(self.decrypt_window, text="", fg="white", bg="#333333", font=("Helvetica", 14))  # Label to display the decrypted message
            self.decrypted_label.pack(pady=10)                                 # Add padding around the label
        else:
            self.decrypt_window.lift()                                         # Bring the window to the front if it is already open
#------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------
    def decrypt(self):
        encrypted_message_str = self.encrypted_entry.get()                     # Get the encrypted message from the entry widget
        if not encrypted_message_str:
            messagebox.showwarning("Warning", "Please paste the encrypted message.")  # Show a warning if no message is pasted
            return                                                                    # Exit the method if no message is provided

        try:
            # Decrypt the message
            decrypted_message = self.cipher.decrypt(encrypted_message_str.encode()).decode()  # Decrypt the message and convert it to a string

            # Display decrypted message
            self.decrypted_label.config(text=f"Decrypted Message: {decrypted_message}")       # Update the label with the decrypted message

            # Clear the entry field
            self.encrypted_entry.delete(0, tk.END)                    # Clear the input field
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {e}")  # Show an error message if decryption fails
#______________________________________________________________________________________________________________________________________________________________

if __name__ == "__main__":
    root = tk.Tk()               # Create the main application window
    app = CryptographyApp(root)  # Initialize the CryptographyApp with the main window
    root.mainloop()              # Start the tkinter event loop
