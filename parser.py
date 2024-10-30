import json
import os

def hex_to_512bit_binary(hex_string):
    if hex_string.startswith(('0x', '0X')):
        hex_string = hex_string[2:]
    try:
        hex_int = int(hex_string, 16)
    except ValueError:
        raise ValueError("Invalid hexadecimal string provided.")
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

def load_parts_mapping(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file '{filepath}' does not exist.")
    try:
        with open(filepath, 'r') as file:
            parts_data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError(f"The file '{filepath}' contains invalid JSON.")
    return parts_data

def normalize_binary(binary_str, length):
    return binary_str.zfill(length)

def identify_axie_parts(binary_str, parts_data, dominant_mapping_mapping):
    identified_parts = {}
    for part, (start, end) in dominant_mapping_mapping.items():
        part_binary = binary_str[start:end]
        part_type = part.capitalize()
        expected_length = None
        for p in parts_data:
            if p.get('type') == part_type:
                expected_length = len(p.get('binary'))
                break
        if expected_length:
            normalized_part_binary = normalize_binary(part_binary, expected_length)
        else:
            normalized_part_binary = part_binary
        potential_matches = [
            p for p in parts_data
            if p.get('type') == part_type
        ]
        matching_part = next(
            (
                p for p in potential_matches
                if p.get('binary') == normalized_part_binary
            ),
            None
        )
        if matching_part:
            identified_parts[part] = {
                "id": matching_part.get("id"),
                "name": matching_part.get("name"),
                "specialGenes": matching_part.get("specialGenes"),
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
                if p.get('type') == part_type and p.get('r'):
                    expected_length = len(p.get('r'))
                    break
            if expected_length:
                normalized_recessive_binary = normalize_binary(recessive_binary, expected_length)
            else:
                normalized_recessive_binary = recessive_binary
            potential_matches = [
                p for p in parts_data
                if p.get('type') == part_type
            ]
            matching_recessive_part = next(
                (
                    p for p in potential_matches
                    if p.get('r') == normalized_recessive_binary
                ),
                None
            )
            if matching_recessive_part:
                identified_recessive_parts[f"{part}_{alias}"] = {
                    "id": matching_recessive_part.get("id"),
                }
            else:
                identified_recessive_parts[f"{part}_{alias}"] = "Unknown Recessive Part"
    return identified_recessive_parts


def json_structure(hex_string):
    parts_mapping_file = 'parts_mapping.json'
    try:
        binary_512 = hex_to_512bit_binary(hex_string)

        binary_slice, axie_class = identify_axie_class(binary_512)

        dominant_mapping = {
            "eyes": (142, 165),
            "mouth": (206, 229),
            "ears": (270, 293),
            "horn": (334, 357),
            "back": (398, 421),
            "tail": (462, 485),
        }

        recessive_mapping = {
            "eyes": {"r1": (168, 178), "r2": (181, 191)},
            "mouth": {"r1": (232, 242), "r2": (245, 255)},
            "ears": {"r1": (296, 306), "r2": (309, 319)},
            "horn": {"r1": (360, 370), "r2": (373, 383)},
            "back": {"r1": (424, 434), "r2": (437, 447)},
            "tail": {"r1": (488, 498), "r2": (501, 511)},
        }

        try:
            parts_data = load_parts_mapping(parts_mapping_file)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading parts mapping: {e}")
            parts_data = []

        output_data = {}

        if parts_data:
            output_data['class'] = axie_class

            identified_parts = identify_axie_parts(binary_512, parts_data, dominant_mapping)

            identified_recessive_parts = identify_axie_recessive_parts(binary_512, parts_data, recessive_mapping)

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

    except Exception as e:
        return f"An error occurred: {e}"
