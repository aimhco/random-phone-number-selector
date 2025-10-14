#!/usr/bin/env python3
"""
Phone Number Manager with GUI
Handles phone number collection, message input, and macOS integration
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import subprocess
import sys
import os


class PhoneNumberManager:
    def __init__(self):
        self.phone_numbers = []
        self.message_text = ""
        self.root = tk.Tk()
        self.setup_main_window()

    def setup_main_window(self):
        """Setup the main phone number input window"""
        self.root.title("Phone Number Manager")
        self.root.geometry("450x400")
        self.root.configure(bg='#f0f0f0')

        # Center the window
        self.center_window(450, 400)

        # Title label
        title_label = tk.Label(
            self.root,
            text="Phone Number Manager",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0'
        )
        title_label.pack(pady=10)

        # Phone number input frame
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Phone Number:", bg='#f0f0f0').pack(anchor='w')
        self.phone_entry = tk.Entry(input_frame, width=30, font=('Arial', 12))
        self.phone_entry.pack(pady=5)
        self.phone_entry.focus()

        # Phone numbers list
        list_frame = tk.Frame(self.root, bg='#f0f0f0')
        list_frame.pack(pady=10, fill='both', expand=True)

        tk.Label(list_frame, text="Added Phone Numbers:", bg='#f0f0f0').pack(anchor='w')

        # Listbox with scrollbar
        listbox_frame = tk.Frame(list_frame)
        listbox_frame.pack(fill='both', expand=True, padx=10)

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')

        self.phone_listbox = tk.Listbox(
            listbox_frame,
            yscrollcommand=scrollbar.set,
            font=('Arial', 10)
        )
        self.phone_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.phone_listbox.yview)

        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=20)

        # Buttons
        add_btn = tk.Button(
            button_frame,
            text="Add Another Phone Number",
            command=self.add_phone_number,
            bg='#4CAF50',
            fg='black',
            font=('Arial', 10, 'bold'),
            padx=10,
            relief='raised',
            bd=2
        )
        add_btn.pack(side='left', padx=5)

        ok_btn = tk.Button(
            button_frame,
            text="OK",
            command=self.proceed_to_message,
            bg='#4CAF50',
            fg='black',
            font=('Arial', 10, 'bold'),
            padx=20,
            relief='raised',
            bd=2
        )
        ok_btn.pack(side='left', padx=5)

        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel_operation,
            bg='#4CAF50',
            fg='black',
            font=('Arial', 10, 'bold'),
            padx=15,
            relief='raised',
            bd=2
        )
        cancel_btn.pack(side='left', padx=5)

        # Bind Enter key to add phone number
        self.phone_entry.bind('<Return>', lambda e: self.add_phone_number())

    def center_window(self, width, height):
        """Center window on screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def add_phone_number(self):
        """Add phone number to the list"""
        phone = self.phone_entry.get().strip()
        if phone:
            if phone not in self.phone_numbers:
                self.phone_numbers.append(phone)
                self.phone_listbox.insert(tk.END, phone)
                self.phone_entry.delete(0, tk.END)
                print(f"Added phone number: {phone}")
            else:
                messagebox.showwarning("Duplicate", "This phone number is already in the list!")
        else:
            messagebox.showwarning("Empty Field", "Please enter a phone number!")

    def proceed_to_message(self):
        """Proceed to message input if we have phone numbers"""
        if not self.phone_numbers:
            messagebox.showwarning("No Phone Numbers", "Please add at least one phone number!")
            return

        # Add current entry if it exists
        current_phone = self.phone_entry.get().strip()
        if current_phone and current_phone not in self.phone_numbers:
            self.phone_numbers.append(current_phone)

        print(f"Proceeding with {len(self.phone_numbers)} phone numbers: {self.phone_numbers}")
        self.show_message_window()

    def cancel_operation(self):
        """Cancel and exit"""
        self.root.destroy()

    def show_message_window(self):
        """Show the message input window"""
        self.root.withdraw()  # Hide main window

        # Create message window
        self.message_window = tk.Toplevel()
        self.message_window.title("Enter Message")
        self.message_window.geometry("450x300")
        self.message_window.configure(bg='#f0f0f0')
        self.center_message_window(450, 300)

        # Title
        title_label = tk.Label(
            self.message_window,
            text="Enter Your Message",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0'
        )
        title_label.pack(pady=10)

        # Message input
        tk.Label(self.message_window, text="Message:", bg='#f0f0f0').pack(anchor='w', padx=20)

        # Text area with scrollbar
        text_frame = tk.Frame(self.message_window)
        text_frame.pack(pady=10, padx=20, fill='both', expand=True)

        text_scrollbar = tk.Scrollbar(text_frame)
        text_scrollbar.pack(side='right', fill='y')

        self.message_text_widget = tk.Text(
            text_frame,
            height=8,
            font=('Arial', 12),
            yscrollcommand=text_scrollbar.set,
            wrap='word'
        )
        self.message_text_widget.pack(side='left', fill='both', expand=True)
        text_scrollbar.config(command=self.message_text_widget.yview)

        self.message_text_widget.focus()

        # Buttons
        button_frame = tk.Frame(self.message_window, bg='#f0f0f0')
        button_frame.pack(pady=20)

        ok_btn = tk.Button(
            button_frame,
            text="OK",
            command=self.send_message,
            bg='#4CAF50',
            fg='black',
            font=('Arial', 10, 'bold'),
            padx=30,
            relief='raised',
            bd=2
        )
        ok_btn.pack(side='left', padx=10)

        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel_message,
            bg='#4CAF50',
            fg='black',
            font=('Arial', 10, 'bold'),
            padx=20,
            relief='raised',
            bd=2
        )
        cancel_btn.pack(side='left', padx=10)

        # Handle window close
        self.message_window.protocol("WM_DELETE_WINDOW", self.cancel_message)

    def center_message_window(self, width, height):
        """Center message window on screen"""
        screen_width = self.message_window.winfo_screenwidth()
        screen_height = self.message_window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.message_window.geometry(f"{width}x{height}+{x}+{y}")

    def send_message(self):
        """Process the message and integrate with macOS"""
        self.message_text = self.message_text_widget.get("1.0", tk.END).strip()

        if not self.message_text:
            messagebox.showwarning("Empty Message", "Please enter a message!")
            return

        # Select random phone number (but don't show it to user)
        selected_phone = random.choice(self.phone_numbers)
        print(f"Selected phone number: {selected_phone}")
        print(f"Message: {self.message_text}")

        # Show confirmation without revealing the phone number
        result = messagebox.askyesno(
            "Send Message",
            f"Ready to send your message!\n\n"
            f"This will add a new contact and send your message.\n\n"
            f"Continue?"
        )

        if result:
            try:
                self.add_contact_to_system(selected_phone)
                self.send_imessage(selected_phone, self.message_text)
                messagebox.showinfo("Success", "Contact added and SMS sent!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        self.cleanup()

    def add_contact_to_system(self, phone_number):
        """Add contact to macOS Contacts app using AppleScript"""
        applescript = f'''
        tell application "Contacts"
            set newContact to make new person
            set first name of newContact to "Test"
            make new phone at end of phones of newContact with properties {{label:"mobile", value:"{phone_number}"}}
            save
        end tell
        '''

        try:
            subprocess.run(['osascript', '-e', applescript], check=True)
            print(f"Added contact 'Test' with phone number: {phone_number}")
        except subprocess.CalledProcessError as e:
            print(f"Error adding contact: {e}")
            raise Exception("Failed to add contact. Make sure Contacts app is accessible.")

    def send_imessage(self, phone_number, message):
        """Send SMS text message using AppleScript"""
        # Clean the phone number and message for AppleScript
        clean_phone = phone_number.replace('"', '\\"')
        clean_message = message.replace('"', '\\"').replace('\n', '\\n')

        applescript = f'''
        tell application "Messages"
            set targetService to 1st account whose service type = SMS
            set targetBuddy to participant "{clean_phone}" of targetService
            send "{clean_message}" to targetBuddy
        end tell
        '''

        try:
            subprocess.run(['osascript', '-e', applescript], check=True)
            print(f"Sent SMS to {phone_number}: {message}")
        except subprocess.CalledProcessError as e:
            print(f"Error sending SMS: {e}")
            raise Exception("Failed to send SMS. Make sure Messages app is accessible and SMS is set up.")

    def cancel_message(self):
        """Cancel message input and return to main window"""
        self.message_window.destroy()
        self.root.deiconify()  # Show main window again

    def cleanup(self):
        """Clean up and exit"""
        if hasattr(self, 'message_window'):
            self.message_window.destroy()
        self.root.destroy()

    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main function to run the application"""
    print("Starting Phone Number Manager...")
    print("Note: This app requires macOS and proper permissions for Contacts and Messages.")

    app = PhoneNumberManager()
    app.run()


if __name__ == "__main__":
    main()