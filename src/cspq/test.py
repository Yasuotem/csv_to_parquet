import duckdb


def main():
    records = duckdb.sql(
        "DESCRIBE SELECT * FROM read_csv_auto('TBL01_20250101.csv', encoding='SHIFT_JIS', skip=1)"
    ).fetchall()
    print(records)
