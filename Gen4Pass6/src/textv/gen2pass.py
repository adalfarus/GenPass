# Gen2Pass.py
print("  $$$$$$\                       $$$$$$\  $$$$$$$\                               ")
print(" $$  __$$\                     $$  __$$\ $$  __$$\                              ")
print(" $$ /  \__| $$$$$$\  $$$$$$$\  \__/  $$ |$$ |  $$ |$$$$$$\   $$$$$$$\  $$$$$$$\ ")
print(" $$ |$$$$\ $$  __$$\ $$  __$$\  $$$$$$  |$$$$$$$  |\____$$\ $$  _____|$$  _____|")
print(" $$ |\_$$ |$$$$$$$$ |$$ |  $$ |$$  ____/ $$  ____/ $$$$$$$ |\$$$$$$\  \$$$$$$\  ")
print(" $$ |  $$ |$$   ____|$$ |  $$ |$$ |      $$ |     $$  __$$ | \____$$\  \____$$\ ")
print(" \$$$$$$  |\$$$$$$$\ $$ |  $$ |$$$$$$$$\ $$ |     \$$$$$$$ |$$$$$$$  |$$$$$$$  |")
print("  \______/  \_______|\__|  \__|\________|\__|      \_______|\_______/ \_______/ ")
print("Gen2Pass V2.0.0.0 Created by Adalfarus")
print()

import string
import random
import pyperclip
import unicodedata
import sys

def main():
    print("0: Choose own Characters")
    print("1: Without (a) Type/s of Characters")
    print("2: With all Characters")
    print("3: With a sentence")
    
    while True:
        try:
            pass_type = int(input("What kind of Password do you want? : "))
            if pass_type in (0, 1, 2, 3):
                break
            else:
                print("Invalid input. Please enter a valid option (0, 1, 2, or 3).")
        except ValueError:
            print("Invalid input. Please enter a valid option (0, 1, 2, or 3).")

    if pass_type == 0:
        specharacters = get_special_characters()
        deduct_symbols, exclude_symbols = [], []
        letters, digits, specialchar = "", "", ""
    elif pass_type == 1:
        pass_type_list = input("Enter character types you DON'T want to use, separate with dots (ALPHABET.DIGITS.SPECIAL CHARACTERS): ").split(".")
        letters = "" if "ALPHABET" in pass_type_list else string.ascii_letters
        digits = "" if "DIGITS" in pass_type_list else string.digits
        specialchar = "" if "SPECIAL CHARACTERS" in pass_type_list else string.punctuation
        specharacters = get_special_characters()
        deduct_symbols, exclude_symbols = get_exclu_and_dedc_symbols()
    elif pass_type == 2:
        letters, digits, specialchar = string.ascii_letters, string.digits, string.punctuation
        specharacters = get_special_characters()
        deduct_symbols, exclude_symbols = get_exclu_and_dedc_symbols()
    elif pass_type == 3:
        password = sentence_pass_gen()
        sys.exit()

    while True:
        try:
            password_length = int(input("Length of Password: "))
            if password_length <= 0:
                print("Length should be a positive integer. Try again.")
            else:
                break
        except ValueError:
            print("Entered value should be an integer only. Try again.")

    while True:
        password = generate_password(password_length, deduct_symbols, exclude_symbols, letters, digits, specialchar, specharacters)
        if password is None:
            print("Please try again with different inputs.")
            main()
        elif len(password) == password_length:
            print("Your password: ", password)
            pyperclip.copy(password)
            print("Your password is copied to your clipboard.")
            break

def get_special_characters():
    categories = {'L': {'Ll': 'Lowercase', 'Lm': 'Modifier', 'Lt': 'Titlecase', 'Lu': 'Uppercase', 'Lo': 'Other'},
                  'M': {'Mc': 'Spacing Combining', 'Me': 'Enclosing', 'Mn': 'Non-Spacing'},
                  'N': {'Nd': 'Decimal Digit', 'Nl': 'Letter', 'No': 'Other'},
                  'P': {'Pc': 'Connector', 'Pd': 'Dash', 'Pi': 'Initial Quote', 'Pf': 'Final Quote',
                        'Ps': 'Open', 'Pe': 'Close', 'Po': 'Other'},
                  'S': {'Sc': 'Currency', 'Sk': 'Modifier', 'Sm': 'Math', 'So': 'Other'},
                  'Z': {'Zl': 'Line', 'Zp': 'Paragraph', 'Zs': 'Space'},
                  'C': {'Cc': 'Control', 'Cf': 'Format', 'Cn': 'Not Assigned', 'Co': 'Private Use', 'Cs': 'Surrogate'}}

    unicode_version = unicodedata.unidata_version
    print(f"\nUnicode {unicode_version} has {len(categories)} character categories, and each category has subcategories:")
    for category, subcategories in categories.items():
        subcategories_str = ", ".join([f"{subcat} ({name})" for subcat, name in subcategories.items()])
        print(f"\t{category}: {subcategories_str}")
    print("There are 3 ranges reserved for private use (Co subcategory): U+E000-U+F8FF (6,400 code points), "
          "U+F0000-U+FFFFD (65,534) and U+100000-U+10FFFD (65,534).")
    print("Surrogates (Cs subcategory) use the range U+D800-U+DFFF (2,048 code points).\n")

    selected_categories = input("Type in the Unicode category/ies or subcategory/ies you want to see, use space as a separator: ").strip()

    selected_categories = selected_categories.split()
    for cat in selected_categories:
        if cat not in categories and not any(cat in subcats for subcats in categories.values()) or cat==[]:
            print("Invalid category/ies or subcategory/ies:", cat)
        else:
            all_characters = [chr(i) for i in range(0x110000)]
            selected_characters = [c for c in all_characters
                           if unicodedata.category(c)[0] in selected_categories
                           or unicodedata.category(c) in selected_categories]
            unicode_str = ' '.join(selected_characters)
            print(f"Characters in {selected_categories}: {unicode_str}")
    specharacters = input("Type in your extra Character/s, spaces are counted as Character/s too: ")
    return specharacters

def get_exclu_and_dedc_symbols():
    character_groups = [
        range(97, 123), # lowercase letters a-z
        range(65, 91),  # uppercase letters A-Z
        range(48, 58),  # digits 0-9
        range(33, 48),  # special characters ! to /
        range(58, 65),  # special characters : to @
        range(91, 97),  # special characters [ to `
        range(123, 127) # special characters { to ~
    ]

    password_chars = []
    for group in character_groups:
        for i in group:
            password_chars.append(chr(i))
    password_str = ''.join(password_chars)
    print(password_str)
    
    deduct_symbols_input = input("Deduct Symbol(s): ")
    exclude_symbols_input = input("Exclude Symbol(s): ")
    
    deduct_symbols = list(deduct_symbols_input) if deduct_symbols_input else []
    exclude_symbols = list(exclude_symbols_input) if exclude_symbols_input else []

    return deduct_symbols, exclude_symbols

def sentence_pass_gen():
    print(" ")
    print("Write a sentence, of all the things you want in your password.")
    print("Each word will become a connected section in the password")
    print("All words get shuffled before use")
    print("Words wont be used multiple times in the password")
    print("The order of the words will get shuffled too")
    print(" ")
    sentence = input("Sentence: ")
    sentence_1 = sentence.split(' ')

    if len(sentence_1) < 2:
        print("Error: Input must have more than one word.")
    else:
        password = ""
        while len(password) != len(sentence):
            if not sentence_1:
                break  # exit the loop if Satz_1 is empty
            word = random.choice(sentence_1)  # select a random word from Satz
            sentence_1.remove(word)  # remove the selected word from Satz
            word = list(word)  # convert the word to a list of letters
            random.shuffle(word)
            password = password + "".join(word)  # add shuffled word to password
            print(" ")
            print(password)
            print(" ")
    return password

def generate_password(length, deduct_symbols, exclude_symbols, letters, digits, specialchar, specharacters):
    characters = letters + digits + specialchar + specharacters
    characters = list(characters)
    deduct_symbols_set = set(deduct_symbols)

    for char in deduct_symbols_set:
        if char in characters:
            characters.remove(char)
    characters = ''.join(characters)
    filtered_characters = [char for char in characters if char not in exclude_symbols]

    if not filtered_characters:
        print("Error: Filtered characters list is empty. Please adjust your inputs.")
        return None

    password = ''.join(random.choice(filtered_characters) for i in range(length))
    password_l = list(password)
    random.shuffle(password_l)
    password = "".join(password_l)
    return password

if __name__ == "__main__":
    main()
