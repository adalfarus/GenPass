#ccipher_6
def cipher(intext, index): #Function to apply Cipher, that takes in the position of the Key letter in the alphabet and the text to cipher.
    outtext = ""
    for i in range(len(intext)):
        temp = ord(intext[i]) + index
        if temp > 122:
            temp_diff = temp - 122
            temp = 96 + temp_diff
        elif temp < 97:
            temp_diff = 97 - temp
            temp = 123 - temp_diff
        outtext += chr(temp)
    return outtext
chars=[]
for i in range(97, 123): #Create list with all lowercase letters
    chars.append(chr(i))
setting=int(input("0:Encode\n1:Decode\n2:Bruteforce\nInput:"))
intext=input("Phrase:").lower()
if not setting==2:
    key_letter=input("Key Letter: a->").lower()
else:
    key_letter="a"
if not intext.isalpha() or not key_letter.isalpha():
    print("Error: Input must be alphabetic.")
else:
    if setting==0:
        index=chars.index(key_letter) #find Position of Key Letter in list with all lowercase letters
        outtext=cipher(intext, index)
        print("Phrase:", outtext)
    elif setting==1:
        index=26-chars.index(key_letter) #26-keypos is for deciphering, so that it doesn't go below 97, but it also functions by making the keypos minus
        outtext=cipher(intext, index)
        print("Phrase:", outtext)
    elif setting==2:
        for key in range(ord('a'), ord('z')+1): #Try all possible key letters
            key_letter=chr(key)
            index=26-chars.index(key_letter)
            outtext=cipher(intext, index)
            print("Key:", key_letter, "Decoded text:", outtext)
    else:
        print("Error: Invalid option selected.")
