import os
import csv
import json
import unicodedata

# === CONFIGURATION ===
TSV_FILE = "../../global/excel/magicprefix.txt"          # Your TSV file with "Name" column
JSON_DIR = "./strings/"           # Folder with multiple .json files
# =====================

def normalize(text):
    """Normalize and lowercase text to avoid invisible mismatches."""
    return unicodedata.normalize("NFKC", text.strip().lower())

def collect_all_keys(json_dir):
    keys = set()
    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            path = os.path.join(json_dir, filename)
            try:
                with open(path, 'r', encoding='utf-8-sig') as f:
                    data = json.load(f)
                    for entry in data:
                        key = entry.get("Key")
                        if key:
                            keys.add(normalize(key))
            except Exception as e:
                print(f"Warning: Couldn't load {filename}: {e}")
    return keys

def find_missing_names(tsv_file, known_keys):
    missing = []
    seen = set()
    with open(tsv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        if "Name" not in reader.fieldnames:
            raise Exception("Missing 'Name' column in TSV file.")
        for row in reader:
            raw_name = row.get("Name", "")
            clean_name = raw_name.strip()
            norm_name = normalize(clean_name)

            # Brute force comparison to avoid ANY mismatch edge cases
            found = any(norm_name == k for k in known_keys)

            if clean_name and not found and clean_name not in seen:
                missing.append(clean_name)
                seen.add(clean_name)
    return missing

def main():
    print("🔍 Collecting all 'Key' entries from JSON files...")
    json_keys = collect_all_keys(JSON_DIR)
    print(f"✅ Loaded {len(json_keys)} normalized keys.\n")

    print("📄 Comparing against TSV 'Name' values...")
    missing_names = find_missing_names(TSV_FILE, json_keys)

    print("\n🚫 MISSING KEYS:")
    if missing_names:
        for name in missing_names:
            print(f"- {name}")
    else:
        print("✅ All TSV names were found in at least one JSON.")

if __name__ == "__main__":
    main()
