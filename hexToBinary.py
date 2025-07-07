import json
import pyperclip

hex_string = '0x18000000000001006001c0e10208000000010010108143040001000c086043020001000c2040c00a0002068c1860c30a0001000c3061830c0001000c08604106'

def hex_to_512bit_binary(hex_string):
    if hex_string.startswith(('0x', '0X')):
        hex_string = hex_string[2:]
    hex_int = int(hex_string, 16)
    binary_str = bin(hex_int)[2:].zfill(512)
    return binary_str[-512:]

# Convert and format the binary string with commas
binary_output = hex_to_512bit_binary(hex_string)
binary_with_commas = ",".join(binary_output)

# Copy to clipboard
pyperclip.copy(binary_with_commas)
print("[INFO] Binary string copied to clipboard.")
