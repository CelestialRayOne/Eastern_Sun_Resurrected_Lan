# Config: Set file paths
SKILLDESC_FILE = "../../global/excel/skilldesc.txt"  # Path to skilldesc file
REFERENCE_FILE = "../../global/excel/skills.txt"  # Path to reference file

# Function to extract the skilldesc column from skilldesc.txt
def extract_skilldesc_column(file_path):
    values = set()
    with open(file_path, "r", encoding="utf-8-sig") as file:
        for line in file:
            parts = line.strip().split("\t")  # Assume tab-separated
            if len(parts) > 1:  # Ensure there are multiple columns
                values.add(parts[0].strip())  # Use only first column (skilldesc), keep case-sensitive
    return values

# Function to check if skilldesc values exist anywhere in skills.txt
def check_references(file_path, skilldesc_values):
    found_values = set()
    with open(file_path, "r", encoding="utf-8-sig") as file:
        file_content = file.read()  # Read entire file without lowercasing

        for skill in skilldesc_values:
            if skill in file_content:  # Search for exact match (case-sensitive)
                found_values.add(skill)  # If found, store it

    return found_values

# Extract skilldesc values
skilldesc_values = extract_skilldesc_column(SKILLDESC_FILE)

# Check if they exist in skills.txt
found_values = check_references(REFERENCE_FILE, skilldesc_values)

# Find missing entries
missing_entries = sorted(skilldesc_values - found_values)

# Print results
if missing_entries:
    print("\n🔹 Missing Entries (Not Found in skills.txt):")
    for entry in missing_entries:
        print(entry)
else:
    print("\n✅ No missing entries found!")
