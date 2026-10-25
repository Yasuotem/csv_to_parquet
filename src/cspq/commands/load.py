import typer
import duckdb
from pathlib import Path
from typing import Annotated
import importlib.resources as res
import cspq.yaml_schema as ys
import cspq.utl as utl
import fnmatch


def load(files: Annotated[list[Path], typer.Argument()]):
    """
    csvpq.yaml のスキーマを元に csv を parquet に変換します
    """
    config = utl.load_config()
    table = matched_table(files[0].name, config["tables"])
    if table == None:
        typer.echo("適合するパターンはありませんでした")
        return
    schema = utl.load_schema(table["path"])
    columns = schema["columns"]
    types = schema["types"]
    alias = schema["aliases"]
    rates = {k: f" * {v}" for k, v in schema["rates"].items()}
    print(schema)
    print(types)
    for file in files:

        sql = (
            "SELECT\n"
            + ",\n".join(
                [
                    f"CAST({col} AS {types[col]}){rates.get("col", "")} AS '{alias[col]}'"
                    for col in columns
                ]
            )
            + f"\nFROM (SELECT * FROM read_csv('{file.resolve()}', encoding='{schema['encoding']}') OFFSET {schema['skip_rows']});"
        )
        print(sql)

        duckdb.sql(sql).to_parquet("test.parquet")


def matched_table(file_name: str, tables: dict[str, ys.Table]) -> ys.Table | None:
    """file_nameにマッチするschemaを返す"""
    for name, tbl in tables.items():
        if fnmatch.fnmatch(tbl["pattern"], file_name):
            return tbl

    return None
