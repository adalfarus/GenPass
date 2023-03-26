import string
import random
import pyperclip
import unicodedata
import time
import sys

def get_spe_characters():
    print(" ")
    categories = {'L': {'Ll': 'Lowercase', 'Lm': 'Modifier', 'Lt': 'Titlecase', 'Lu': 'Uppercase', 'Lo': 'Other'},
                  'M': {'Mc': 'Spacing Combining', 'Me': 'Enclosing', 'Mn': 'Non-Spacing'},
                  'N': {'Nd': 'Decimal Digit', 'Nl': 'Letter', 'No': 'Other'},
                  'P': {'Pc': 'Connector', 'Pd': 'Dash', 'Pi': 'Initial Quote', 'Pf': 'Final Quote',
                        'Ps': 'Open', 'Pe': 'Close', 'Po': 'Other'},
                  'S': {'Sc': 'Currency', 'Sk': 'Modifier', 'Sm': 'Math', 'So': 'Other'},
                  'Z': {'Zl': 'Line', 'Zp': 'Paragraph', 'Zs': 'Space'},
                  'C': {'Cc': 'Control', 'Cf': 'Format', 'Cn': 'Not Assigned', 'Co': 'Private Use', 'Cs': 'Surrogate'}}

    unicode_version = unicodedata.unidata_version
    print(f"Unicode {unicode_version} has {len(categories)} character categories, and each category has subcategories:")
    for category, subcategories in categories.items():
        subcategories_str = ", ".join([f"{subcat} ({name})" for subcat, name in subcategories.items()])
        print(f"\t{category}: {subcategories_str}")
    print("\nThere are 3 ranges reserved for private use (Co subcategory): U+E000—U+F8FF (6,400 code points), "
          "U+F0000—U+FFFFD (65,534) and U+100000—U+10FFFD (65,534).")
    print("Surrogates (Cs subcategory) use the range U+D800—U+DFFF (2,048 code points).")
    print(" ")
    # Define categories of "good" Unicode characters
    good_categories = input("Type in the Unicode Characters you want to see, use space as a seperator: ")
    good_categories = good_categories.split(" ")
    # Create a list of all Unicode characters
    all_characters = [chr(i) for i in range(0x110000)]
    # Filter out unwanted characters by category
    good_characters = [c for c in all_characters if unicodedata.category(c) in good_categories]
    unicode_str = ' '.join(good_characters)
    print(" ")
    print(unicode_str)
    print(" ")
    specharacters = input("Type in your extra Characters, spaces are counted as Characters too: ")
    return specharacters

def get_exclu_symbols():
    password_chars = []
    for i in range(48, 58):
        password_chars.append(chr(i)) # digits 0-9
    for i in range(65, 91):
        password_chars.append(chr(i)) # uppercase letters A-Z
    for i in range(97, 123):
        password_chars.append(chr(i)) # lowercase letters a-z
    for i in range(33, 48):
        password_chars.append(chr(i)) # special characters ! to /
    for i in range(58, 65):
        password_chars.append(chr(i)) # special characters : to @
    for i in range(91, 97):
        password_chars.append(chr(i)) # special characters [ to `
    for i in range(123, 127):
        password_chars.append(chr(i)) # special characters { to ~
    password_str = ' '.join(password_chars)
    print(" ")
    print(password_str)
    print(" ")
    exclude_symbols = input("Exclude Symbol(s), separate with a space: ")
    if len(exclude_symbols) > 1:
        exclude_symbols = exclude_symbols.split(" ")
    else:
        exclude_symbols = []
    return exclude_symbols

def get_pass_length():
    while True:
        try:
            string_length = int(input("Length of Password: "))
            if string_length <= 0:
                print("Length should be a positive integer. Try again.")
            else:
                break
        except ValueError:
            print("Entered Value should be an integer only. Try again.")
    return string_length

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

def generate_password(length, letters, digits, specialchar, specharacters):
    characters = letters + digits + specialchar + specharacters

    password = ''.join(random.choice(characters) for i in range(length))
    return password

def finish_up_password(password, exclude_symbols):
    password_l = list(password)
    #print (password_l) #use for debug
    random.shuffle(password_l)
    password = "".join(password_l)
    string = ""
    for i in range(len(password)):
        if password[i] not in exclude_symbols:
            string += password[i]
    return string

def configure():
    pass_type = input("0:Choose own Characters\n1:Without a Type/s of Characters\n2:With all Characters\n3:With a sentence\n->")
    if pass_type == "0":
        specharacters = get_spe_characters()
        exclude_symbols = []
        letters = ""
        digits = ""
        specialchar = ""
    elif pass_type == "1":
        pass_type_list = input("ALPHABET\nDIGITS\nSPECIAL CHARACTERS\nType which Character Types you DON'T want to use, separate with dots: ").split(".")
        if "ALPHABET" in pass_type_list:
            letters = ""
        else:
            letters = string.ascii_letters
        if "DIGITS" in pass_type_list:
            digits = ""
        else:
            digits = string.digits
        if "SPECIAL CHARACTERS" in pass_type_list:
            specialchar = ""
        else:
            specialchar = string.punctuation
        specharacters = get_spe_characters()
        exclude_symbols = get_exclu_symbols()
    elif pass_type == "2":
        letters = string.ascii_letters
        digits = string.digits
        specialchar = string.punctuation
        specharacters = get_spe_characters()
        exclude_symbols = get_exclu_symbols()
    elif pass_type == "3":
        password = sentence_pass_gen()
        sys.exit()
    else:
        print("Please choose one of the Options!")
        sys.exit()
    return letters, digits, specialchar, specharacters, exclude_symbols

def pg_main():
    letters, digits, specialchar, specharacters, exclude_symbols = configure()
    
    password_length = get_pass_length()

    while True:
        password = generate_password(password_length, letters, digits, specialchar, specharacters)
        password = finish_up_password(password, exclude_symbols)

        if len(password) == password_length:
            print("Your password: ", password)
            pyperclip.copy(password)
            print("Your password is copied to your clipboard.")
            break

if __name__ == "__main__":
    pg_main()
