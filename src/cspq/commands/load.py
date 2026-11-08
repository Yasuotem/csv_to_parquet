import fnmatch
import os
from pathlib import Path
from typing import Annotated

import duckdb
import typer

from cspq import utl
from cspq.yaml_schema import Table

from .toplevel import toplevel


def load(files: Annotated[list[Path], typer.Argument()]):
    """
    csvpq.yaml のスキーマを元に csv を parquet に変換します
    """
    config = utl.load_config()
    if config.tables is None:
        return

    print(files[0].name)
    table = matched_table(files[0].name, config.tables)
    if table == None:
        typer.echo("適合するパターンはありませんでした")
        return
    schema = utl.load_schema(Path(table.path))
    columns = schema.columns
    types = schema.types
    alias = schema.aliases
    rates = {k: f" * {v}" for k, v in schema.rates.items()}
    print(schema)
    print(types)
    for file in files:
        mtime = file.stat().st_mtime

        sql = (
            "SELECT\n"
            + ",\n".join(
                [
                    f"CAST({col} AS {types[col]}){rates.get('col', '')} AS '{alias[col]}'"
                    for col in columns
                ]
            )
            + f"\nFROM (SELECT * FROM read_csv('{file.resolve()}', encoding='{schema.encoding}', skip={schema.skip}) OFFSET {schema.offset});"
        )
        print(sql)

        root = toplevel()
        output_file = root / config.data / schema.name / (file.stem + ".parquet")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        duckdb.sql(sql).to_parquet(str(output_file))
        os.utime(output_file, (mtime, mtime))


def matched_table(file_name: str, tables: dict[str, Table]) -> Table | None:
    """file_nameにマッチするTableを返す"""
    for tbl in tables.values():
        if fnmatch.fnmatch(tbl.pattern, file_name):
            return tbl

    return None
