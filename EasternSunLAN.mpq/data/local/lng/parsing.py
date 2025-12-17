import pandas as pd
import csv

# === Load data ===
cubemain    = pd.read_csv("cubemain.txt", sep="\t", dtype=str)
uniqueitems = pd.read_csv("uniqueitems.txt", sep="\t", dtype=str)
weapons     = pd.read_csv("weapons.txt", sep="\t", dtype=str)
armor       = pd.read_csv("armor.txt", sep="\t", dtype=str)
misc        = pd.read_csv("misc.txt", sep="\t", dtype=str)
treasure    = pd.read_csv("treasureclassex.txt", sep="\t", dtype=str)

# === Codes to look up (your big list) ===
codes_of_interest = [
    "05f","06f","07f","08f","03f","02c","02f","01f","01c",
    "13f","05c","01j","06c","09f","10f","04c","03c","04f",
    "09c","08c","07c","14f","15f","16f","17f","11f","12f",
    "22f","23f","10c","21f","20f","11c","19f","01i","18f",
    "19c","15c","25f","27f","14c","13c","26f","12c","16c",
    "16c","30f","29f","28f","18c","17c","02j","02i","20c",
    "34f","35f","32f","33f","24c","31f","23c","22c","21c",
    "27c","26c","29c","28c","25c","36f","37f","38f","39f",
    "32c","31c","34c","42f","30c","43f","44f","40f","41f",
    "47f","38c","39c","37c","36c","35c","46f","45f","33c",
    "53f","54f","55f","42c","41c","40c","56f","49f","48f",
    "60f","61f","43c","59f","58f","57f","51f","50f","52f",
    "46c","65f","64f","63f","62f","03i","45c","44c","66f",
    "01d","02d","03d","02g","71f","70f","69f","68f","67f",
    "10d","09d","08d","03g","07d","06d","05d","04d","01g",
    "13d","09g","07g","06g","05g","04g","03j","12d","11d",
    "16g","15g","14g","13g","12g","11g","10g","14d","08g",
    "20g","24g","16d","17d","15d","18d","19g","18g","17g",
    "27g","26g","21d","25g","22g","23g","20d","21g","19d",
    "34g","35g","36g","24d","23d","28g","30g","29g","22d",
    "27d","26d","43g","42g","41g","33g","32g","31g","37g",
    "35d","34d","33d","40g","39g","38g","44g","29d","28d",
    "53g","54g","55g","56g","32d","31d","30d","37d","36d",
    "57g","45g","46g","47g","48g","49g","50g","51g","52g",
    "65g","63g","62g","38d","39d","61g","60g","59g","58g",
    "70g","04j","05j","68g","67g","40d","69g","66g","64g",
    "72g","74g","43d","04i","42d","41d","73g","71g","44d",
    "07i","77g","48d","47d","06i","05i","76g","45d","75g",
    "07j","02e","02k","01e","01h","06j","78g","50d","49d",
    "09h","07h","06h","05e","04h","05h","04e","03e","03h",
    "12k","11h","13h","09e","08e","07e","06e","08h","10h",
    "13e","12e","15h","14h","10i","09i","08i","11e","10e",
    "22k","14e","21h","15e","20h","17h","18h","16h","21h",
    "28h","27h","26h","25h","24h","16e","23h","19h",
    "33h","18e","17e","08j","32k","31h","30h","29h",
    "39h","21e","19e","20e","37h","36h","35h","34h",
    "22e","45h","42k","43h","11i","38h","41h","40h",
    "48h","51h","23e","25e","47h","24e","46h","44h",
    "30e","09j","54h","53h","27e","26e","50h","49h",
    "33e","32e","38e","12i","31e","52k","28e","29e",
    "56h","57h","58h","55h","37e","36e","35e","34e",
    "10j","62k","40e","41e","39e","59h","60h","61h"
]

# === Build coupon→level mapping from treasureclassex (row order) ===
# Find the 'Treasure Class' column robustly
tc_col = next((c for c in treasure.columns if c.strip().lower() == "treasure class"), treasure.columns[0])
coupon_rows = treasure[treasure[tc_col].str.contains("Coupon", case=False, na=False)]

# Determine item columns (Item1..ItemN), sorted numerically
item_cols = [c for c in treasure.columns if c.lower().startswith("item")]
def _suffix_num(col):
    digits = "".join([ch for ch in col if ch.isdigit()])
    return int(digits) if digits else 0
item_cols = sorted(item_cols, key=_suffix_num)

code_to_level = {}
level_counter = 1
for _, row in coupon_rows.iterrows():
    for col in item_cols:
        code = str(row.get(col, "")).strip()
        if code and code not in ("nan", "None", "Nothing", ""):
            # Only set the first time we encounter a code (earliest coupon level)
            code_to_level.setdefault(code, level_counter)
    level_counter += 1

# === Step 1: Clean cubemain input
cubemain["input1_clean"] = (
    cubemain["input 1"].astype(str).str.split(",").str[0].str.strip()
)

# === Step 2: Filter rows by your codes_of_interest
filtered = cubemain[cubemain["input1_clean"].isin(codes_of_interest)][
    ["input1_clean", "output"]
].copy()

# === Step 3: Normalize for matching
filtered["output_norm"]   = filtered["output"].astype(str).str.strip().str.lower()
uniqueitems["index_norm"] = uniqueitems["index"].astype(str).str.strip().str.lower()

# === Step 4: Merge cubemain outputs → uniqueitems (bring along code + index)
merged = filtered.merge(
    uniqueitems[["index_norm", "code", "index"]],
    left_on="output_norm",
    right_on="index_norm",
    how="left",
)

# === Step 5: Merge with item bases (type, type2, name)
weapons_subset = weapons[["code", "type", "type2", "name"]]
armor_subset   = armor[["code", "type", "name"]].copy()
armor_subset["type2"] = ""
misc_subset    = misc[["code", "type", "name"]].copy()
misc_subset["type2"] = ""

all_items = pd.concat([weapons_subset, armor_subset, misc_subset], axis=0, ignore_index=True)
final = merged.merge(all_items, on="code", how="left")

# === Add level column from coupon mapping (missing -> "")
final["level"] = final["input1_clean"].map(code_to_level).fillna("").astype(str)

# === Step 6: Sort and clean NaN
final_sorted = final.sort_values(by="type", na_position="last").fillna("")

# === Step 7: Deduplicate by code
final_unique = final_sorted.drop_duplicates(subset=["input1_clean"], keep="first")

# === Step 8: Write TSV with 6 columns (includes 'level')
out_path = "code_type_mapping.tsv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    w.writerow(["code", "type", "type2", "basename", "unique_item", "level"])
    for _, r in final_unique.iterrows():
        w.writerow([r["input1_clean"], r["type"], r["type2"], r["name"], r["index"], r["level"]])

print(f"✅ Wrote {len(final_unique)} unique rows to {out_path}")
