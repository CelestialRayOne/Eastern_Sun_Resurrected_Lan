import pandas as pd

# File paths
FILE_A = '../../global/excel/monstats.txt'  # must contain "MonSound" and "UMonSound"
FILE_B = '../../global/excel/monsounds.txt'  # must contain "Id"

def validate_monster_sounds():
    # Load tab-separated files
    df_a = pd.read_csv(FILE_A, sep='\t', dtype=str).fillna('')
    df_b = pd.read_csv(FILE_B, sep='\t', dtype=str).fillna('')

    # Check required columns
    if not {'MonSound', 'UMonSound'}.issubset(df_a.columns) or 'Id' not in df_b.columns:
        print("Error: Required columns are missing.")
        return

    # Extract and clean sound references
    sound_refs = set(df_a['MonSound'].str.strip()) | set(df_a['UMonSound'].str.strip())
    sound_refs.discard('')

    valid_ids = set(df_b['Id'].str.strip())

    # Find missing sound references
    missing = sorted(sound_refs - valid_ids)

    # Output
    if missing:
        print("❌ The following MonSound/UMonSound values are missing in the 'Id' column of File B:")
        for val in missing:
            print(f"  - {val}")
    else:
        print("✅ All MonSound and UMonSound values are valid.")

validate_monster_sounds()
