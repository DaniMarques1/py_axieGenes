import json
from parser import json_structure


hex_string = input("Input your hex string: ").strip()
if not hex_string:
    hex_string = "0x18000000000002018101c040c40c00000003000c0800450200020608108045020001000c186044040002060410a084040002060c186082040003000418a0c102"

info_str = json_structure(hex_string)
info = json.loads(info_str)

print(info)
print(info_str)
