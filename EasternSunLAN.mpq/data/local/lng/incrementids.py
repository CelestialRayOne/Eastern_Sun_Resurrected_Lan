import json

# Config: Input file and starting ID
INPUT_JSON_FILE = './strings/input.json'
STARTING_ID = 28126  # Hardcoded starting value

def reassign_ids_in_place():
    # Load JSON array from file
    with open(INPUT_JSON_FILE, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("Error: Input JSON must be an array.")
        return

    # Update ID fields
    for i, obj in enumerate(data):
        obj['id'] = STARTING_ID + i

    print(f"Updated {len(data)} objects with new IDs starting from {STARTING_ID}.")

    # Overwrite the same file
    with open(INPUT_JSON_FILE, 'w', encoding='utf-8-sig') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

reassign_ids_in_place()
