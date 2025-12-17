import json
import re
import time
import requests
import os
from pathlib import Path

# Folder containing input .json files
INPUT_DIR = Path(".")   # change this if needed
OUTPUT_DIR = Path("./translated")
OUTPUT_DIR.mkdir(exist_ok=True)

# Language codes for translation
languages = {
    "deDE": "de",
    "esES": "es",
    "esMX": "es",
    "itIT": "it",
    "frFR": "fr",
    "jaJP": "ja",
    "koKR": "ko",
    "plPL": "pl",
    "ptBR": "pt",
    "ruRU": "ru",
    "zhCN": "zh-CN",
    "zhTW": "zh-TW"
}

# Regular expressions to match special codes and characters to escape
special_code_pattern = re.compile(r"(ÿc[0-9A-Z=@;<]|\n)")
special_char_pattern = re.compile(r"([+%])")  # Characters to preserve

# Escape/unescape helpers
def escape_special_chars(text):
    return special_char_pattern.sub(lambda m: f"[[{ord(m.group(0))}]]", text)

def unescape_special_chars(text):
    return re.sub(r"\[\[(\d+)\]\]", lambda m: chr(int(m.group(1))), text)

# Helper function to perform translation with retry logic
def translate_with_retries(text, lang, max_retries=3):
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={lang}&dt=t&q={text}"
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                translated_text = response.json()[0][0][0]
                return translated_text
            else:
                print(f"Warning: Translation failed (status {response.status_code}) attempt {attempt+1} for {lang}")
        except (requests.exceptions.RequestException, IndexError, TypeError) as e:
            print(f"Error on attempt {attempt+1} for {lang}: {e}")
        time.sleep(1)
    return text

# Function to translate text while preserving codes/characters
def translate_text_with_codes(text, lang, max_retries=3):
    chunks = re.split(special_code_pattern, text)
    translated_text = ""
    for chunk in chunks:
        if special_code_pattern.match(chunk):
            translated_text += chunk
        elif chunk.strip():
            escaped_chunk = escape_special_chars(chunk.strip())
            translated_chunk = translate_with_retries(escaped_chunk, lang, max_retries)
            translated_text += unescape_special_chars(translated_chunk)
    return translated_text

# Process a single JSON file
def process_json_file(file_path: Path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading {file_path.name}: {e}")
        return

    if not isinstance(data, list):
        print(f"⚠️ Skipping {file_path.name}: not a list of objects")
        return

    for index, item in enumerate(data):
        english_text = item.get("enUS", "")
        if not english_text:
            continue
        print(f"Translating {file_path.name} item {index+1}/{len(data)}")

        for key, lang in languages.items():
            if not item.get(key):  # only translate if empty
                item[key] = translate_text_with_codes(english_text, lang)

    # Save translated JSON in output folder
    output_file = OUTPUT_DIR / f"{file_path.stem}-translated.json"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved: {output_file.name}")
    except Exception as e:
        print(f"❌ Error writing {output_file.name}: {e}")

if __name__ == "__main__":
    if not INPUT_DIR.exists() or not INPUT_DIR.is_dir():
        print(f"❌ Input directory does not exist: {INPUT_DIR}")
    else:
        for file_path in INPUT_DIR.glob("*.json"):
            process_json_file(file_path)
