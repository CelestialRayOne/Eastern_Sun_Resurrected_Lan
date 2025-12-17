import json
from pathlib import Path

# 🔧 Path to your input .json file
INPUT_FILE = Path("./strings/item-names.json")  # Change this to your file path

def process_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {file_path.name}: {e}")
        return

    if not isinstance(data, list):
        print(f"Skipping {file_path.name}: Not a list of objects")
        return

    for entry in data:
        if 'enUS' in entry:
            entry['ruRU'] = entry['enUS']
        else:
            print(f"Missing 'enUS' in: {entry}")

    output_path = file_path.with_name(f"{file_path.stem}-copied.json")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Copied: {file_path.name} -> {output_path.name}")
    except Exception as e:
        print(f"Error writing {output_path.name}: {e}")

if __name__ == "__main__":
    if not INPUT_FILE.exists():
        print(f"Input file does not exist: {INPUT_FILE}")
    else:
        process_json_file(INPUT_FILE)
