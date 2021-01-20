with open("imported_i2c_data.txt") as file:
    data = file.read().splitlines()
 
found_letters = []
succ_level = 0

for line in data[1:]:

    all_data = line.split()
    data1 = all_data[-2]
    data2 = all_data[-1].strip(".Write,ACK")

    # a letter is printed, if 3 consecutive packages contain the data2="1001","1101","1001"
    if succ_level == 0 and data2 == "1001":
        succ_level = 1
    elif succ_level == 1 and data2 == "1101":
        succ_level = 2
    elif succ_level == 2 and data2 == "1001":
        # success: third package found, this is a printed letter
        found_letters.append(data1)
        succ_level = 0
    else:
        # failed: this is not a printed letter
        succ_level = 0

# put together first and second half of data bits
assert len(found_letters) % 2 == 0
found_letters_combined = []
for i in range(len(found_letters) // 2):
    k = i * 2
    data_combined = found_letters[k] + found_letters[k + 1]
    found_letters_combined.append(data_combined)
 
 
# Correspondence between Character Codes and Character Patterns (ROM Code: A00)
# from https://image.dfrobot.com/image/data/TOY0046/HD44780.pdf
letter_dict = {
    "01010000": "P",
    "01100001": "a",
    "01110011": "s",
    "01110111": "w",
    "01101111": "o",
    "01110010": "r",
    "01100100": "d",
    "01000101": "E",
    "01101110": "n",
    "01110100": "t",
    "01100101": "e",
    "00100000": " ",
    "01001000": "H",
    "00101010": "*",
    "01010100": "T",
    "01000010": "B",
    "01000001": "A",
    "01000011": "C",
    "01000111": "G",
    "01010010": "R",
    "01010011": "S",
    "01001110": "N",
    "01000100": "D",
    "01011001": "Y",
    "01111011": "{",
    "01111101": "}",
    "00110000": "0",
    "00110001": "1",
    "00110010": "2",
    "00110011": "3",
    "00110100": "4",
    "00110101": "5",
    "00110110": "6",
    "00110111": "7",
    "00111000": "8",
    "00111001": "9",
    "01011111": "_",
    "01100011": "c",
    "01101011": "k",
    "00100001": "!",
    "01000000": "@",
}


# compose password
final_letter_output = []
password = []
for i, item in enumerate(found_letters_combined):
    if item in letter_dict:
        final_letter_output.append(letter_dict[item])

    if i > 3:
        # find first letter of password
        if all([final_letter_output[-3] == "r",
                final_letter_output[-2] == "d",
                final_letter_output[-1] != "*", ]):
            password.append(final_letter_output[-1])

        # find other letters of password
        elif all([final_letter_output[-2] == "*",
                final_letter_output[-1] != "*", ]):
            password.append(final_letter_output[-1])

password = "".join(password)
print(password)
