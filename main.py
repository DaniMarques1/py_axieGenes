import json
from parser import json_structure

hex_string = '0x18000000000001006001c0e10208000000010010108143040001000c086043020001000c2040c00a0002068c1860c30a0001000c3061830c0001000c08604106'


info_str = json_structure(hex_string)
info = json.loads(info_str)

print(info)
print(info_str)

