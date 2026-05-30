import pandas as pd
import re
import os

FILE_PATH = r"c:\Users\hp\Documents\ds_materials\data_cleaning\data-for-calling_compress.xlsx"
OUTPUT_CSV = r"c:\Users\hp\Documents\ds_materials\data_cleaning\extracted_contacts.csv"

# ── Step 1: Inspect the raw file ─────────────────────────────────────────────
print("=" * 60)
print("STEP 1 – Inspecting raw Excel file")
print("=" * 60)

xl = pd.ExcelFile(FILE_PATH)
print(f"Sheet names: {xl.sheet_names}\n")

for sheet in xl.sheet_names:
    df_raw = pd.read_excel(FILE_PATH, sheet_name=sheet, header=None)
    print(f"--- Sheet: '{sheet}' | Shape: {df_raw.shape} ---")
    print(df_raw.head(20).to_string())
    print()

# ── Step 2: Smart extraction ─────────────────────────────────────────────────
print("=" * 60)
print("STEP 2 – Extracting structured data")
print("=" * 60)

# Read first sheet (adjust sheet_name/header if needed after inspection)
df = pd.read_excel(FILE_PATH, sheet_name=0, header=None)

# Flatten all cell values into one long list for quick pattern scan
all_values = df.values.flatten().tolist()
all_values = [str(v).strip() for v in all_values if pd.notna(v) and str(v).strip() not in ("", "nan")]

print(f"Total non-empty cells: {len(all_values)}")
print("Sample values:", all_values[:30])
print()

# ── Step 3: Detect column positions automatically ────────────────────────────
# Try reading with the first row as header
df_header = pd.read_excel(FILE_PATH, sheet_name=0, header=0)
print("Columns detected (first row as header):")
print(df_header.columns.tolist())
print(df_header.head(10).to_string())
print()

# ── Step 4: Map columns → Serial No / Name / Phone / Address ────────────────
def find_column(df, keywords):
    """Return the first column whose name contains any of the keywords (case-insensitive)."""
    for col in df.columns:
        col_str = str(col).lower()
        if any(kw.lower() in col_str for kw in keywords):
            return col
    return None

col_serial  = find_column(df_header, ["serial", "sr", "s.no", "sno", "no.", "sl"])
col_name    = find_column(df_header, ["name", "customer", "client", "person"])
col_phone   = find_column(df_header, ["phone", "mobile", "contact", "cell", "number", "mob"])
col_address = find_column(df_header, ["address", "addr", "location", "area", "city", "place"])

print(f"Mapped columns:")
print(f"  Serial  → {col_serial}")
print(f"  Name    → {col_name}")
print(f"  Phone   → {col_phone}")
print(f"  Address → {col_address}")
print()

# ── Step 5: Build clean output DataFrame ────────────────────────────────────
records = []
for idx, row in df_header.iterrows():
    serial  = row[col_serial]  if col_serial  else idx + 1
    name    = row[col_name]    if col_name    else ""
    phone   = row[col_phone]   if col_phone   else ""
    address = row[col_address] if col_address else ""

    # Skip clearly empty rows
    if pd.isna(name) and pd.isna(phone) and pd.isna(address):
        continue

    # Clean phone: keep digits, +, spaces, dashes
    phone_clean = re.sub(r"[^\d\+\-\s]", "", str(phone)).strip() if pd.notna(phone) else ""

    records.append({
        "Serial Number": serial,
        "Name":          str(name).strip()    if pd.notna(name)    else "",
        "Phone Number":  phone_clean,
        "Address":       str(address).strip() if pd.notna(address) else "",
    })

df_out = pd.DataFrame(records, columns=["Serial Number", "Name", "Phone Number", "Address"])

# Add auto serial if column was missing
if col_serial is None:
    df_out["Serial Number"] = range(1, len(df_out) + 1)

print(f"Records extracted: {len(df_out)}")
print(df_out.head(10).to_string(index=False))

# ── Step 6: Save to CSV ──────────────────────────────────────────────────────
df_out.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"\n✅  CSV saved → {OUTPUT_CSV}")
