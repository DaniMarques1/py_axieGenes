import json
from parser import json_structure

hex_string = '0x200000000000010001c0e070400000000001001008a1020200010008084044040001001020618404000206841021440400030008182085020001001018818504'


info_str = json_structure(hex_string)
info = json.loads(info_str)

print(info)
print(info_str)

