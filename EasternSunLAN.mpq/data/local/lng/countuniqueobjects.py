import os
import json

# Directory containing your JSON files
DIRECTORY = './strings'  # Change this to your actual folder path

def count_objects_in_all_json_files():
    for filename in os.listdir(DIRECTORY):
        if filename.endswith('.json'):
            path = os.path.join(DIRECTORY, filename)
            try:
                with open(path, 'r', encoding='utf-8-sig') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        print(f"{filename}: {len(data)} objects")
                    else:
                        print(f"{filename}: Root is not a JSON array")
            except Exception as e:
                print(f"{filename}: Failed to read ({e})")

count_objects_in_all_json_files()
