from parser import (
    hex_to_512bit_binary,
    identify_axie_class,
    load_parts_mapping,
    identify_axie_parts,
    identify_axie_recessive_parts,
    json_structure
)

hex_string = '0x9000000000000100008000c0840800000001000410604508000100102040450a000100102081020c000100042821410600010008180040080001001018014406'

print(json_structure(hex_string))
