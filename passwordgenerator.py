import random
import string

def generatePassword(length=12, useUppercase=True, useLowercase=True, useDigits=True, useSymbols=True):
    if not (useUppercase or useLowercase or useDigits or useSymbols):
        return "Error: At least one character type must be selected!"

    characterSets = []
    if useUppercase:
        characterSets.append(string.ascii_uppercase)  # A-Z
    if useLowercase:
        characterSets.append(string.ascii_lowercase)  # a-z
    if useDigits:
        characterSets.append(string.digits)  # 0-9
    if useSymbols:
        characterSets.append(string.punctuation)  # Special characters

    # Ensure at least one character from each selected type
    password = [random.choice(chars) for chars in characterSets]

    # Fill the rest of the password with random characters from all selected sets
    allCharacters = ''.join(characterSets)
    password += [random.choice(allCharacters) for _ in range(length - len(password))]

    # Shuffle to avoid predictable patterns
    random.shuffle(password)

    return ''.join(password)

# User Input
try:
    length = int(input("Enter the desired password length (min 4): "))
    if length < 4:
        print("Password length must be at least 4 characters.")
    else:
        useUppercase = input("Include uppercase letters? (y/n): ").strip().lower() == 'y'
        useLowercase = input("Include lowercase letters? (y/n): ").strip().lower() == 'y'
        useDigits = input("Include numbers? (y/n): ").strip().lower() == 'y'
        useSymbols = input("Include special characters? (y/n): ").strip().lower() == 'y'

        password = generatePassword(length, useUppercase, useLowercase, useDigits, useSymbols)
        print("\nGenerated Password:", password)

except ValueError:
    print("Invalid input! Please enter a valid number for password length.")
