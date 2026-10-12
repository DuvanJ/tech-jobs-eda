"""
Reduce survey_results_public_2025.csv a solo las columnas que usa la app.
Ejecutar una sola vez: python slim_csv.py
"""
import pandas as pd
import os

INPUT  = "survey_results_public_2025.csv"
OUTPUT = "survey_results_public_2025.csv"  # sobreescribe el mismo archivo

KEEP = [
    "Country", "Employment", "EdLevel",
    "JobSat", "LanguageHaveWorkedWith",
    "DatabaseHaveWorkedWith", "WebframeHaveWorkedWith",
    "DevType", "OrgSize", "RemoteWork", "Age",
    # columnas de experiencia (varía por año del survey)
    "YearsCodePro", "YearsCode", "WorkExp",
    # columnas de salario (varía por año del survey)
    "ConvertedCompYearly", "ConvertedComp", "CompTotal",
]

print(f"Leyendo {INPUT}...")
all_cols = pd.read_csv(INPUT, nrows=0).columns.tolist()
use = [c for c in KEEP if c in all_cols]
print(f"Columnas encontradas: {use}")

df = pd.read_csv(INPUT, usecols=use, low_memory=False)
print(f"Filas: {len(df):,}  |  Columnas: {len(df.columns)}")

size_before = os.path.getsize(INPUT) / 1024 / 1024
df.to_csv(OUTPUT, index=False)
size_after = os.path.getsize(OUTPUT) / 1024 / 1024

print(f"\nAntes: {size_before:.1f} MB")
print(f"Después: {size_after:.1f} MB")
print(f"Reducción: {(1 - size_after/size_before)*100:.0f}%")
print(f"\nListo → {OUTPUT}")