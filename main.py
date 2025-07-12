import json
from parser import json_structure

hex_string = input("Input your hex string: ").strip()
if not hex_string:
    hex_string = "0x200000000000000181c16080820800000001001008a04302000100082081430400020604188044020001001008810402000300042001040a0001001010808404"

info_str = json_structure(hex_string)
info = json.loads(info_str)

print(info)
print(info_str)
