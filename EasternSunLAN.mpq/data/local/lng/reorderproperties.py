import json
import os

# Folder containing JSON files
JSON_FOLDER = './strings'

# Desired property order
DESIRED_ORDER = [
    "id", "Key", "enUS", "zhTW", "deDE", "esES", "frFR", "itIT",
    "koKR", "plPL", "esMX", "jaJP", "ptBR", "ruRU", "zhCN"
]

def reorder_json_files_in_folder():
    for filename in os.listdir(JSON_FOLDER):
        if not filename.endswith('.json'):
            continue

        filepath = os.path.join(JSON_FOLDER, filename)
        print(f"Processing {filename}...")

        with open(filepath, 'r', encoding='utf-8-sig') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"  Skipping (invalid JSON): {filename}")
                continue

        if not isinstance(data, list):
            print(f"  Skipping (not an array): {filename}")
            continue

        # Reorder properties in each object
        reordered = []
        for obj in data:
            new_obj = {key: obj[key] for key in DESIRED_ORDER if key in obj}
            # Preserve any extra fields not in DESIRED_ORDER
            for key in obj:
                if key not in new_obj:
                    new_obj[key] = obj[key]
            reordered.append(new_obj)

        # Overwrite file with reordered content
        with open(filepath, 'w', encoding='utf-8-sig') as f:
            json.dump(reordered, f, indent=2, ensure_ascii=False)

        print(f"  ✓ Reordered {len(reordered)} entries")

reorder_json_files_in_folder()
