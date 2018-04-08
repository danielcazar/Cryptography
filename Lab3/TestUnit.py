import filecmp
from Assignment1 import decrypt, encrypt

# Unit Test over mode CBC
input_file = "input.txt"
output_file = input_file + ".enc"
output_file_decrypt = input_file + ".dec"
mode = "CBC"
IV="817714415"

assert decrypt(mode, encrypt(mode, IV, input_file, output_file), output_file_decrypt)

if filecmp.cmp(input_file, output_file_decrypt) == True:
    print("Unit test successfull")

# Unit Test over mode CFB
input_file = "input.txt"
output_file = input_file + ".enc"
output_file_decrypt = input_file + ".dec"
mode = "CFB"
IV="817714415"

assert decrypt(mode, encrypt(mode, IV, input_file, output_file), output_file_decrypt)

if filecmp.cmp(input_file, output_file_decrypt) == True:
    print("Unit test successfull")

# Unit Test over mode ECB
input_file = "input.txt"
output_file = input_file + ".enc"
output_file_decrypt = input_file + ".dec"
mode = "ECB"
IV="817714415"

assert decrypt(mode, encrypt(mode, IV, input_file, output_file), output_file_decrypt)

if filecmp.cmp(input_file, output_file_decrypt) == True:
    print("Unit test successfull")
