import os
import json
import re

# Configuration: Set paths
JSON_FILE_PATH = "./strings/skills.json"  # Path to the main JSON file
TEXT_FILES_FOLDER = "../../global/excel"  # Folder with text files
JSON_FILES_FOLDER = "../../global/ui/layouts"  # Folder with JSON files
OUTPUT_FILE_PATH = "./strings/skills_cleaned.json"  # Output JSON file

# Regular expression to match only valid skill keys
KEY_PATTERN = re.compile(r"^(E?Skillx?|E?skillx?|E?Skill|E?skill)(ld|sd|an|name)([0-9]{1,3}|400)$")

# Load the JSON file
try:
    with open(JSON_FILE_PATH, "r", encoding="utf-8-sig") as json_file:
        data = json.load(json_file)
except Exception as e:
    print(f"Error loading JSON file: {e}")
    exit(1)

# ✅ Extract & store only valid keys from JSON
valid_skill_keys = {entry["Key"] for entry in data if "Key" in entry and KEY_PATTERN.match(entry["Key"])}

# Function to read all text files in a folder
def read_text_files(folder_path):
    content = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content += file.read()
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return content

# Function to read all JSON files in a folder, handling broken JSON
def read_json_files(folder_path):
    json_content = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    json_data = file.read()
                    try:
                        json_obj = json.loads(json_data)  # Try parsing JSON normally
                    except json.JSONDecodeError:
                        print(f"⚠ Warning: Invalid JSON detected in {filename}. Attempting to fix...")
                        json_data = re.sub(r",\s*([\]}])", r"\1", json_data)  # Remove trailing commas
                        try:
                            json_obj = json.loads(json_data)  # Try parsing again
                        except json.JSONDecodeError:
                            print(f"⚠ Error: Could not fully fix {filename}, treating as plain text.")
                            json_content += json_data  # Fallback: Read as text
                            continue
                    
                    json_content += json.dumps(json_obj)  # Convert JSON to string
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return json_content

# Read content from both folders
text_files_content = read_text_files(TEXT_FILES_FOLDER)
json_files_content = read_json_files(JSON_FILES_FOLDER)

# ✅ Only remove objects where:
#    1. The key matches the skill pattern
#    2. The key is NOT found in either text or JSON files
cleaned_data = [
    entry for entry in data 
    if entry["Key"] not in valid_skill_keys or (entry["Key"] in text_files_content or entry["Key"] in json_files_content)
]

# Save the cleaned JSON file
try:
    with open(OUTPUT_FILE_PATH, "w", encoding="utf-8-sig") as json_file:
        json.dump(cleaned_data, json_file, indent=2, ensure_ascii=False)
    print(f"\n✅ Cleaned JSON saved to {OUTPUT_FILE_PATH}")
except Exception as e:
    print(f"Error saving cleaned JSON file: {e}")
