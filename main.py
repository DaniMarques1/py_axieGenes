from parser import (
    hex_to_512bit_binary,
    identify_axie_class,
    load_parts_mapping,
    identify_axie_parts,
    identify_axie_recessive_parts,
    json_structure
)

hex_string = '0x200000000000030003408041001000000001000808a0400400010000100040020000009008208506000100101860420400000094082082020001001010404304'
parts_mapping_file = 'parts_mapping.json'
print(json_structure(hex_string, parts_mapping_file))
