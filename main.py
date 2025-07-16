import json
from parser import json_structure

hex_string = input("Input your hex string: ").strip()
if not hex_string:
    hex_string = "0x200000000000030001c120e0830c00000002060c1020400200010010084044040001000010a0c0020002060c18a040020002009008a044060002061010a04206"

info_str = json_structure(hex_string)
info = json.loads(info_str)

print(info)
print(info_str)
