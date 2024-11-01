import json
import os

def hex_to_512bit_binary(hex_string):
    if hex_string.startswith(('0x', '0X')):
        hex_string = hex_string[2:]
    hex_int = int(hex_string, 16)
    binary_str = bin(hex_int)[2:].zfill(512)
    return binary_str[-512:]

def identify_axie_class(binary_str):
    class_mapping = {
        "00100": "aquatic",
        "00000": "beast",
        "00010": "bird",
        "00001": "bug",
        "00101": "reptile",
        "00011": "plant",
        "10010": "dusk",
        "10001": "dawn",
        "10000": "mech",
    }
    binary_slice = binary_str[0:5]
    axie_class = class_mapping.get(binary_slice, "Unknown Class")
    return binary_slice, axie_class

def get_axie_color(binary_512):
    color_slice = (95, 98)
    color_bits = binary_512[color_slice[0]:color_slice[1]]

    color_mapping = {
        "000": "00",
        "001": "01",
        "010": "02",
        "011": "03",
        "100": "04"
    }

    return color_mapping.get(color_bits, "Unknown")

def load_parts_mapping(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file '{filepath}' does not exist.")
    with open(filepath, 'r') as file:
        parts_data = json.load(file)
    return parts_data

def normalize_binary(binary_str, length):
    return binary_str.zfill(length)

def identify_special_genes(binary_str, specialGenes_slice, specialGenes_mapping, part):
    start, end = specialGenes_slice.get(part, (None, None))
    if start is None or end is None:
        return None
    gene_bits = binary_str[start:end]
    gene_key = gene_bits
    for gene_name, gene_value in specialGenes_mapping.items():
        if isinstance(gene_value, list):
            if gene_key in gene_value:
                return gene_name
        else:
            if gene_key == gene_value:
                return gene_name
    return None

import json


def identify_axie_parts(binary_str, parts_data, dominant_mapping, stage_mapping, specialGenes_slice,
                        specialGenes_mapping):
    identified_parts = {}
    for part, (start, end) in dominant_mapping.items():
        part_binary = binary_str[start:end]
        part_type = part.capitalize()
        stage_bit_position = stage_mapping[part]
        stage_bit = binary_str[stage_bit_position]
        stage = 1 if stage_bit == '0' else 2
        special_genes = identify_special_genes(binary_str, specialGenes_slice, specialGenes_mapping, part)

        expected_length = None
        for p in parts_data:
            if (p.get('type') == part_type and
                    p.get('stage') == stage and
                    ((special_genes is not None and p.get('specialGenes') == special_genes) or
                     (special_genes is None and p.get('specialGenes') is None))):
                expected_length = len(p.get('binary'))
                break

        if expected_length:
            normalized_part_binary = normalize_binary(part_binary, expected_length)
        else:
            normalized_part_binary = part_binary

        if special_genes is not None:
            potential_matches = [
                p for p in parts_data
                if (p.get('type') == part_type and
                    p.get('stage') == stage and
                    p.get('specialGenes') == special_genes)
            ]
            matching_part = next(
                (
                    p for p in potential_matches
                    if p.get('binary') == normalized_part_binary
                ),
                None
            )
        else:
            potential_matches = [
                p for p in parts_data
                if (p.get('type') == part_type and
                    p.get('stage') == stage and
                    p.get('specialGenes') is None)
            ]
            matching_part = next(
                (
                    p for p in potential_matches
                    if p.get('binary') == normalized_part_binary
                ),
                None
            )

        if not matching_part and special_genes is not None:
            fallback_matches = [
                p for p in parts_data
                if (p.get('type') == part_type and
                    p.get('stage') == stage and
                    p.get('specialGenes') is None)
            ]
            matching_part = next(
                (
                    p for p in fallback_matches
                    if p.get('binary') == normalized_part_binary
                ),
                None
            )

        if matching_part:
            identified_parts[part] = {
                "id": matching_part.get("id"),
                "name": matching_part.get("name"),
                "specialGenes": special_genes,
                "stage": matching_part.get("stage"),
                "type": matching_part.get("type").lower(),
                "class": matching_part.get("class")
            }
        else:
            identified_parts[part] = "Unknown Part"

    return identified_parts


def identify_axie_recessive_parts(binary_str, parts_data, recessive_mapping):
    identified_recessive_parts = {}
    for part, aliases in recessive_mapping.items():
        for alias, (start, end) in aliases.items():
            recessive_binary = binary_str[start:end]
            part_type = part.capitalize()
            expected_length = None
            for p in parts_data:
                if p.get('type') == part_type and p.get('binary') and p.get('specialGenes') is None:
                    expected_length = len(p.get('binary'))
                    break
            if expected_length:
                normalized_recessive_binary = normalize_binary(recessive_binary, expected_length)
            else:
                normalized_recessive_binary = recessive_binary
            potential_matches = [
                p for p in parts_data
                if p.get('type') == part_type and
                   p.get('specialGenes') is None
            ]
            matching_recessive_part = next(
                (
                    p for p in potential_matches
                    if p.get('binary') == normalized_recessive_binary
                ),
                None
            )
            key = f"{part}_{alias}"
            if matching_recessive_part:
                identified_recessive_parts[key] = {
                    "id": matching_recessive_part.get("id"),
                    "class": matching_recessive_part.get("class"),
                }
            else:
                identified_recessive_parts[key] = "Unknown Recessive Part"
    return identified_recessive_parts

def json_structure(hex_string):
    parts_mapping_file = 'parts_mapping.json'
    binary_512 = hex_to_512bit_binary(hex_string)
    binary_slice, axie_class = identify_axie_class(binary_512)
    axie_color = get_axie_color(binary_512)

    stage_mapping = {
        "eyes": 142,
        "mouth": 206,
        "ears": 270,
        "horn": 334,
        "back": 398,
        "tail": 462,
    }

    dominant_mapping = {
        "eyes": (155, 165),
        "mouth": (219, 229),
        "ears": (283, 293),
        "horn": (347, 357),
        "back": (411, 421),
        "tail": (475, 485),
    }

    recessive_mapping = {
        "eyes": {"r1": (168, 178), "r2": (181, 191)},
        "mouth": {"r1": (232, 242), "r2": (245, 255)},
        "ears": {"r1": (296, 306), "r2": (309, 319)},
        "horn": {"r1": (360, 370), "r2": (373, 383)},
        "back": {"r1": (424, 434), "r2": (437, 447)},
        "tail": {"r1": (488, 498), "r2": (501, 511)},
    }

    specialGenes_slice = {
        "eyes": (149, 153),
        "mouth": (213, 217),
        "ears": (277, 281),
        "horn": (341, 345),
        "back": (405, 409),
        "tail": (469, 473),
    }

    specialGenes_mapping = {
        None: "0000",
        "Japan": "0011",
        "Xmas2018": "0100",
        "Xmas2019": "0101",
        "Bionic": "0010",
        "Mystic": "0001",
        "Summer2022": ["0110", "1001"]
    }

    try:
        parts_data = load_parts_mapping(parts_mapping_file)
    except (FileNotFoundError, ValueError):
        parts_data = []

    output_data = {}

    if parts_data:
        output_data['class'] = axie_class
        output_data['color'] = axie_color

        identified_parts = identify_axie_parts(
            binary_512, parts_data, dominant_mapping, stage_mapping,
            specialGenes_slice, specialGenes_mapping
        )

        identified_recessive_parts = identify_axie_recessive_parts(
            binary_512, parts_data, recessive_mapping
        )

        parts_list = ['eyes', 'mouth', 'ears', 'horn', 'back', 'tail']

        for part in parts_list:
            output_data[part] = {}
            dominant_part = identified_parts.get(part)
            output_data[part]['d'] = dominant_part if dominant_part else None

            r1_key = f"{part}_r1"
            r2_key = f"{part}_r2"
            output_data[part]['r1'] = identified_recessive_parts.get(r1_key, None)
            output_data[part]['r2'] = identified_recessive_parts.get(r2_key, None)

        return json.dumps(output_data, indent=2)
    else:
        return "No parts data available."

