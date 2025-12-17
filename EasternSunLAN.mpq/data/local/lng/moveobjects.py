import json
import pandas as pd

# File paths
TSV_FILE = '../../../data/global/excel/magicprefix.txt'
SOURCE_JSON = './strings/item-names.json'
TARGET_JSON = './strings/item-nameaffixes.json'

def move_objects_by_key_anywhere_in_tsv():
    # Step 1: Read the tab-separated file as plain text (all values)
    df = pd.read_csv(TSV_FILE, sep='\t', dtype=str)
    all_values = set(str(cell) for col in df.columns for cell in df[col].dropna())

    # Step 2: Load source and target JSON files
    with open(SOURCE_JSON, 'r', encoding='utf-8-sig') as f:
        source_data = json.load(f)

    with open(TARGET_JSON, 'r', encoding='utf-8-sig') as f:
        target_data = json.load(f)

    if not isinstance(source_data, list) or not isinstance(target_data, list):
        print("Both JSON files must contain top-level arrays.")
        return

    # Step 3: Move objects where Key is found anywhere in the TSV
    to_move = [obj for obj in source_data if str(obj.get("Key")) in all_values]
    remaining = [obj for obj in source_data if str(obj.get("Key")) not in all_values]

    print(f"Moving {len(to_move)} objects from {SOURCE_JSON} to {TARGET_JSON} based on Key matches found anywhere in {TSV_FILE}")

    # Step 4: Save results
    with open(SOURCE_JSON, 'w', encoding='utf-8-sig') as f:
        json.dump(remaining, f, indent=2, ensure_ascii=False)

    with open(TARGET_JSON, 'w', encoding='utf-8-sig') as f:
        json.dump(target_data + to_move, f, indent=2, ensure_ascii=False)

move_objects_by_key_anywhere_in_tsv()
