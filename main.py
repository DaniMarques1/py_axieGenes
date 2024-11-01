import json
from parser import json_structure

hex_string = '0x90000000000001000200e0b0400000000001001408a045020001000c2861430a0003000c180104080003000c2061830c0003001418a0c5060003001428a1450a'

info_str = json_structure(hex_string)
info = json.loads(info_str)

print(info)
print(info_str)

