# ============================================================
#  CipherLab — CLI v1.0
#  A terminal-based cryptography toolkit
#  Concepts: functions, loops, conditionals, string methods
# ============================================================


# ── COMMON PASSWORDS LIST ──────────────────────────────────
# A list is a collection of items stored in one variable.
# We'll check the user's password against this list.

# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
#  CipherLab — CLI v1.0

COMMON_PASSWORDS = [
    "password", "123456", "password123", "admin", "letmein",
    "qwerty", "abc123", "monkey", "master", "dragon",
    "iloveyou", "sunshine", "princess", "welcome", "shadow",
    "superman", "michael", "football", "batman", "trustno1",
    "123456789", "000000", "1234567", "password1", "12345678",
    "12345", "1234567890", "pass", "test", "guest", "hello"
]


# ============================================================
#  CAESAR CIPHER
# ============================================================

# A function is a reusable block of code.
# def means "define a function"
# text, shift, mode are the inputs (called parameters)

def caesar_cipher(text, shift, mode):
    """Encrypts or decrypts text using the Caesar cipher."""

    # When decrypting, we reverse the shift direction
    if mode == "decrypt":
        shift = 26 - shift

    result = ""  # Start with an empty string, build it up letter by letter

    # Loop through every character in the text
    # 'for' means "do this for each item in a collection"
    for char in text:

        # Check if the character is an uppercase letter
        # .isupper() returns True or False
        if char.isupper():
            base = 65  # ASCII number where uppercase letters start (A = 65)
            # ord() converts a character to its ASCII number
            # chr() converts an ASCII number back to a character
            # % 26 wraps the alphabet — after Z comes A again
            shifted = (ord(char) - base + shift) % 26 + base
            result += chr(shifted)  # += adds to the end of the string

        # Check if the character is a lowercase letter
        elif char.islower():
            base = 97  # ASCII number where lowercase letters start (a = 97)
            shifted = (ord(char) - base + shift) % 26 + base
            result += chr(shifted)

        # If it's not a letter (space, number, punctuation), leave it unchanged
        else:
            result += char

    return result  # Send the result back to whoever called this function


def brute_force(text):
    """Tries all 25 possible shifts and prints every result."""

    print("\n  ⚠  BRUTE FORCE — All 25 Possible Decryptions")
    print("  " + "─" * 50)

    # A for loop with range() — runs the code 25 times
    # range(1, 26) generates numbers 1, 2, 3 ... 25
    for i in range(1, 26):
        decrypted = caesar_cipher(text, i, "decrypt")
        # f-strings let you embed variables inside strings using {}
        # They start with the letter f before the quote
        print(f"  Shift +{i:>2} │ {decrypted}")

    print()


def run_cipher():
    """Handles the Caesar cipher menu."""

    print("\n  ── CAESAR CIPHER ──────────────────────────────")

    # input() pauses the program and waits for the user to type something
    # The string inside is the prompt shown to the user
    text = input("  Enter your message: ")

    if not text:  # Check if the user typed nothing
        print("  ✖  No message entered.")
        return  # Exit the function early

    print("  [1] Encrypt  [2] Decrypt  [3] Brute Force")
    choice = input("  Choose: ").strip()  # .strip() removes extra spaces

    if choice == "1":
        # int() converts a string to a whole number
        shift = int(input("  Shift (1-25): "))
        result = caesar_cipher(text, shift, "encrypt")
        print(f"\n  ✔  Encrypted: {result}")

    elif choice == "2":
        shift = int(input("  Shift (1-25): "))
        result = caesar_cipher(text, shift, "decrypt")
        print(f"\n  ✔  Decrypted: {result}")

    elif choice == "3":
        brute_force(text)

    else:
        print("  ✖  Invalid choice.")


# ============================================================
#  PASSWORD STRENGTH CHECKER
# ============================================================

def check_password(password):
    """Analyzes a password and returns a score and feedback."""

    # A dictionary stores key-value pairs — like a labeled checklist
    # Each key is a criterion name, each value is True or False
    criteria = {
        "12+ characters":       len(password) >= 12,
        "Uppercase letter":     any(c.isupper() for c in password),
        "Lowercase letter":     any(c.islower() for c in password),
        "Number":               any(c.isdigit() for c in password),
        "Special character":    any(not c.isalnum() for c in password),
        "Not a common password": password.lower() not in COMMON_PASSWORDS,
    }

    # Count how many criteria passed
    # sum() adds up numbers — True counts as 1, False as 0
    score = sum(criteria.values())

    return criteria, score  # Return both the checklist and the score


def run_password_checker():
    """Handles the password strength checker menu."""

    print("\n  ── PASSWORD STRENGTH CHECKER ───────────────────")
    password = input("  Enter a password to analyze: ")

    if not password:
        print("  ✖  No password entered.")
        return

    criteria, score = check_password(password)

    print("\n  Criteria:")
    print("  " + "─" * 40)

    # Loop through the dictionary — .items() gives you key and value together
    for criterion, passed in criteria.items():
        # Ternary expression — one-line if/else
        icon = "✔" if passed else "✖"
        status = "Pass" if passed else "Fail"
        print(f"  {icon}  {criterion:<25} {status}")

    print("  " + "─" * 40)

    # Determine rating based on score
    if score == 6:
        rating = "EXCELLENT"
    elif score == 5:
        rating = "STRONG"
    elif score == 4:
        rating = "GOOD"
    elif score == 3:
        rating = "FAIR"
    elif score == 2:
        rating = "WEAK"
    else:
        rating = "VERY WEAK"

    print(f"\n  Score:  {score}/6")
    print(f"  Rating: {rating}\n")


# ============================================================
#  MAIN MENU
# ============================================================

def main():
    """The main loop — keeps the program running until the user exits."""

    # A while loop runs forever until told to stop
    # while True means "keep going indefinitely"
    while True:
        print("\n" + "=" * 50)
        print("         CIPHERLAB — CLI v1.0")
        print("         Cryptography Toolkit")
        print("=" * 50)
        print("  [1]  Caesar Cipher")
        print("  [2]  Password Strength Checker")
        print("  [3]  Exit")
        print("─" * 50)

        choice = input("  Choose an option: ").strip()

        if choice == "1":
            run_cipher()

        elif choice == "2":
            run_password_checker()

        elif choice == "3":
            print("\n  Goodbye.\n")
            break  # break exits the while loop — program ends here

        else:
            print("\n  ✖  Invalid option. Enter 1, 2, or 3.")


# ============================================================
#  ENTRY POINT
# ============================================================

# This is a Python convention — it means:
# "Only run main() if this file is being run directly"
# (not if it's being imported by another file)

if __name__ == "__main__":
    main()