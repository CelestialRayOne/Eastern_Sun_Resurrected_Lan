import pandas as pd

# === CONFIG ===
mapping_path  = "code_type_mapping.tsv"   # output from your previous script (must have columns: code, type, level)
treasure_path = "treasureclassex.txt"     # original treasure class file
out_path      = "treasureclassex2.txt"    # output file to write
MULTIPLIER    = 5                         # multiply ProbX by this for matching codes

# <<<--- Put your filter here: only codes with these 'type' values will be boosted
types_filter = ["shie", "swor", "ashd", "head"]   # <-- example, edit as needed

# === LOAD FILES ===
mapping  = pd.read_csv(mapping_path, sep="\t", dtype=str).fillna("")
treasure = pd.read_csv(treasure_path, sep="\t", dtype=str).fillna("")

# Column name for treasure class (be robust to capitalization/spacing)
tc_col = next((c for c in treasure.columns if c.strip().lower() == "treasure class"), treasure.columns[0])

# Identify all Item/Prob columns, sorted numerically (Item1..ItemN, Prob1..ProbN)
def num_suffix(col):
    d = "".join(ch for ch in col if ch.isdigit())
    return int(d) if d else 0

item_cols = sorted([c for c in treasure.columns if c.lower().startswith("item")], key=num_suffix)
prob_cols = sorted([c for c in treasure.columns if c.lower().startswith("prob")], key=num_suffix)

# === Build code -> (level, type) mapping from mapping TSV ===
code_info = {
    str(row["code"]).strip(): (int(str(row["level"]).strip()), str(row["type"]).strip())
    for _, row in mapping.iterrows()
    if str(row.get("code", "")).strip() and str(row.get("level", "")).strip().isdigit()
}

# === Extract only COUPON rows, in file order, and number them 1..N ===
coupon_rows = treasure[treasure[tc_col].str.contains("coupon", case=False, na=False)].copy()
coupon_rows["__coupon_level__"] = range(1, len(coupon_rows) + 1)

# Convert Prob columns to integers for math (blank -> 0)
for c in prob_cols:
    if c in coupon_rows.columns:
        coupon_rows[c] = coupon_rows[c].replace("", "0").astype(int)

# === For each coupon row, multiply ProbX if code is in mapping, level matches, and type matches filter ===
for idx, row in coupon_rows.iterrows():
    lvl = int(row["__coupon_level__"])
    for icol, pcol in zip(item_cols, prob_cols):
        if icol not in coupon_rows.columns or pcol not in coupon_rows.columns:
            continue
        code = str(row[icol]).strip()
        if not code or code.lower() == "nothing":
            continue
        if code in code_info:
            code_level, code_type = code_info[code]
            if code_level == lvl and code_type in types_filter:
                coupon_rows.at[idx, pcol] = int(row[pcol]) * MULTIPLIER

# Clean up helper column
coupon_rows = coupon_rows.drop(columns=["__coupon_level__"])

# Convert probs back to strings (to keep same txt style)
for c in prob_cols:
    if c in coupon_rows.columns:
        coupon_rows[c] = coupon_rows[c].astype(str)

# === WRITE OUTPUT: only coupon rows ===
coupon_rows.to_csv(out_path, sep="\t", index=False)
print(f"✅ Wrote coupon-only file with boosted probabilities for types {types_filter} to {out_path}")
