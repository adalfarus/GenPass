import math
from itertools import product, permutations
import string
import Levenshtein
import unicodedata

def calc_multiplier(string):
    multiplier = 2
    for i in range(0, len(string)):
        multiplier = math.pow(multiplier, ord(string[i]) / 80)

    for i in range(0, len(string)):
        if i % 2 == 0:
            multiplier -= ord(string[i])
        else:
            multiplier += ord(string[i])

    return abs(multiplier)

def decode_message(encoded_data, code_word):
    multiplier = calc_multiplier(code_word)
    encoded_chars = encoded_data.split('-')
    decoded_chars = []

    for char in encoded_chars:
        decoded_ord = int(float(char) / multiplier)
        decoded_char = chr(decoded_ord + 126)
        decoded_chars.append(decoded_char)

    return ''.join(decoded_chars)

encoded_data = "7393.1104464871705-1188.1784646140095-2112.317270424906-2508.3767586295758-1320.1982940155663-2772.416417432689-1980.2974410233494-2112.317270424906-2772.416417432689-3300.4957350389154-1584.2379528186793-1320.1982940155663-12409.863963746322-3432.515564440472-3828.575052645142-1452.2181234171228-12409.863963746322-3828.575052645142-1188.1784646140095-3564.535393842029-2904.4362468342456-12409.863963746322-1584.2379528186793-2772.416417432689-3564.535393842029-2904.4362468342456-1320.1982940155663-2772.416417432689-3036.4560762358024-10825.626010927643-12409.863963746322-1188.1784646140095-2112.317270424906-3432.515564440472-12409.863963746322-2772.416417432689-1452.2181234171228-1320.1982940155663-12409.863963746322-3300.4957350389154-1452.2181234171228-12409.863963746322-1452.2181234171228-2772.416417432689-3564.535393842029-2904.4362468342456-3300.4957350389154-1584.2379528186793-8317.249252298066-8317.249252298066-8317.249252298066"

def is_similar(message1, message2, threshold):
    distance = Levenshtein.distance(message1, message2)
    similarity = 1 - distance / max(len(message1), len(message2))
    return similarity >= threshold

def is_surrogate(char):
    return 0xD800 <= ord(char) <= 0xDFFF

def remove_surrogates(input_string):
    return ''.join(c for c in input_string if not is_surrogate(c))

expected_message = "Funktioniert das, und ist das auch sicher???"

length = 20
letters_ratio = 0.6
numbers_ratio = 0.2
punctuations_ratio = 0.2
exclude_chars = 'l1i!?'

def generate_passwords(length, letters_ratio, numbers_ratio, punctuations_ratio, exclude_chars):
    num_letters = int(length * letters_ratio)
    num_numbers = int(length * numbers_ratio)
    num_punctuations = int(length * punctuations_ratio)

    letters = string.ascii_letters.translate(str.maketrans('', '', exclude_chars))
    numbers = string.digits.translate(str.maketrans('', '', exclude_chars))
    punctuations = string.punctuation.translate(str.maketrans('', '', exclude_chars))

    for letter_combination in product(letters, repeat=num_letters):
        for number_combination in product(numbers, repeat=num_numbers):
            for punctuation_combination in product(punctuations, repeat=num_punctuations):
                possible_password = ''.join(letter_combination) + ''.join(number_combination) + ''.join(punctuation_combination)
                for shuffled_password in permutations(possible_password, length):
                    yield ''.join(shuffled_password)

possible_passwords = generate_passwords(length, letters_ratio, numbers_ratio, punctuations_ratio, exclude_chars)

for password in possible_passwords:
    print("possible_password", password)
    decoded_message = decode_message(encoded_data, password)
    print("decoded_message", remove_surrogates(decoded_message))

    if is_similar(decoded_message, expected_message, 0.9):  # 0.9 is the similarity threshold
        print(f"Found similar password: {password}")
        break
    # All Possibilities 7.228819 x 10^56/7.228819 � 1056/7.228819e56/722.8819 � 1054/7.228819 � 1056/56/722881900000000000000000000000000000000000000000000000000
    # If there are 2 Billion trys per second it would take 1.1058047369718607e+40 years to Brute Force it.
    #  90^12 * 10^4 * 32^4, which is approximately 4.4 x 10^29 would be the number without shuffleing