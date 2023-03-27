import string
import random
import unicodedata

def generate_password(length=16, debug=False, letters_ratio=0.5, numbers_ratio=0.3, punctuations_ratio=0.2, unicode_ratio=0, extra_chars='', exclude_chars=''):
    def debug_print(*args):
        if debug:
            print(*args)
    ratios = [letters_ratio, numbers_ratio, punctuations_ratio, unicode_ratio]
    if sum(ratios) != 1:
        raise ValueError("The sum of the ratios must be 1.")
    char_types = [string.ascii_letters, string.digits, string.punctuation, [chr(i) for i in range(0x110000) if unicodedata.category(chr(i)).startswith('P')]]
    char_lengths = [int(length * ratio) for ratio in ratios]
    debug_print("Character lengths before adjustment:", char_lengths)
    difference = length - sum(char_lengths)
    for i in range(difference):
        char_lengths[i % len(char_lengths)] += 1
    debug_print("Character lengths after adjustment:", char_lengths)
    all_chars = ''
    for i in range(len(char_types)):
        debug_print(f"Processing character type {i}: {char_types[i][:50]}...")
        if isinstance(char_types[i], str):
            char_type = char_types[i].translate(str.maketrans('', '', exclude_chars))
        else:
            char_type = ''.join([c for c in char_types[i] if c not in exclude_chars])
        debug_print(f"Character type {i} after excluding characters: {char_type[:50]}...")
        if char_lengths[i] > 0:
            generated_chars = ''.join(random.choices(char_type, k=char_lengths[i]))
            debug_print(f"Generated characters for character type {i}: {generated_chars}")
            all_chars += generated_chars
    debug_print("All characters before adding extra characters:", all_chars)
    all_chars += extra_chars
    all_chars = list(all_chars)
    random.shuffle(all_chars)
    debug_print("All characters after processing:", all_chars)
    if length > len(all_chars):
        raise ValueError("Password length is greater than the number of available characters.")
    password = ''.join(all_chars[:length])
    return password

def sentence_pass_gen(sentence, debug=False, shuffle_words=True, shuffle_characters=True, repeat_words=False):
    def debug_print(*args):
        if debug:
            print(*args)
    words = sentence.split(' ')
    if len(words) < 2:
        print("Error: Input must have more than one word.")
        return None
    password = ""
    if shuffle_words:
        debug_print("Words before shuffeling", words)
        random.shuffle(words)
        debug_print("Words after shuffeling", words)
    used_words = set()
    for word in words:
        if not repeat_words and word in used_words:
            debug_print("Ignoring repeated word")
            continue
        if shuffle_characters:
            debug_print("Word before shuffeling", list(word))
            word_chars = list(word)
            random.shuffle(word_chars)
            word = "".join(word_chars)
            debug_print("Word after shuffeling", word)
        password += word
        used_words.add(word)
        debug_print("Used Words", used_words)
        debug_print("Words", words)
    return password

def custom_password_generator(sentence, char_position='random', random_case=False, extra_char='', num_length=0, special_chars_length=0):
    words = sentence.split(' ')
    word_chars = []
    for word in words:
        if char_position == 'random':
            index = random.randint(0, len(word) - 1)
        else:
            index = min(char_position, len(word) - 1)
        char = word[index]
        if random_case:
            char = char.lower() if random.random() < 0.5 else char.upper()
        word_chars.append(char)
    num_string = ''.join(random.choices(string.digits, k=num_length))
    special_chars_string = ''.join(random.choices(string.punctuation, k=special_chars_length))
    password = ''.join(word_chars) + extra_char + num_string + special_chars_string
    return password

# Generate a 20-character password with 60% letters, 20% numbers, and 20% punctuation, but exclude the characters 'l', '1', 'i', '!', and '?'
password1 = generate_password(length=20, letters_ratio=0.6, numbers_ratio=0.2, punctuations_ratio=0.2, exclude_chars='l1i!?')
print(password1)

# Generate a 12-character password with 80% letters and 20% numbers
password2 = generate_password(length=12, letters_ratio=0.8, numbers_ratio=0.2, punctuations_ratio=0)
print(password2)

# Generate a 24-character password with 50% letters, 30% numbers, 10% punctuation, and 10% Unicode
password3 = generate_password(length=24, letters_ratio=0.5, numbers_ratio=0.3, punctuations_ratio=0.1, unicode_ratio=0.1)
print(password3)

password4 = generate_password(48, False, 0, 0, 0, 1)
print("UNI", password4)

sentence = "I love Python programming"
config = {'debug': False}

password5 = sentence_pass_gen(sentence, config.get('debug'), shuffle_words=True, shuffle_characters=True, repeat_words=True)
print("Generated password:", password5)

sentence = "Ich bin müde bitte gib mir energie..."
password6 = custom_password_generator(sentence, char_position=0, random_case=True, extra_char='_', num_length=5, special_chars_length=2)
print(password6)
