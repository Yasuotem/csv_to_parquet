from dataclasses import asdict
from pathlib import Path
from typing import Annotated

import duckdb
import typer
import yaml

from cspq import utl
from cspq.yaml_schema import Schema, Table

from .toplevel import toplevel


def add(
    csv: Annotated[Path, typer.Argument(help="csv ファイルのパス")],
    name: Annotated[str | None, typer.Argument(help="テーブル/ディレクトリ名")] = None,
    encoding: Annotated[
        str, typer.Option(help="csvファイルのエンコード")
    ] = "SHIFT_JIS",
    skip: Annotated[
        int, typer.Option(help="csvファイルのヘッダー前のスキップする行数")
    ] = 0,
    offset: Annotated[
        int, typer.Option(help="csvファイルのヘッダー後のスキップする行数")
    ] = 0,
    alias: Annotated[bool, typer.Option(help="")] = False,
    rate: Annotated[bool, typer.Option()] = False,
):
    """
    csv ファイルを読み込み
    csvpq.yaml にスキーマのテンプレートを追加します
    csvpq.duckdb に VIEW を追加します
    """
    if not csv.exists():
        typer.echo("csv ファイルが見つかりませんでした")
        return

    # name が指定されていない場合csvファイル名をテーブル名とする
    if name is None:
        name = csv.stem

    schema = get_schema(
        csv=csv,
        alias=alias,
        encoding=encoding,
        name=name,
        skip=skip,
        offset=offset,
        rate=rate,
    )

    # schemaを保存
    root = toplevel()
    if root is None:
        typer.echo("cspq.yamlが見つかりませんでした")
        return

    schema_file = name + ".yaml"
    schema_path = root / "schemas" / schema_file
    schema_path.parent.mkdir(parents=True, exist_ok=True)
    with schema_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(asdict(schema), f, sort_keys=False, allow_unicode=True)

    # cspq.yamlにテーブル情報を追加
    config = utl.load_config()

    tables = config.tables

    tables[name] = Table(path="schemas/" + schema_file, pattern=csv.name)
    config.tables = tables

    utl.write_config(config)


def get_schema(
    csv: Path, encoding: str, skip: int, offset: int, name: str, alias: bool, rate: bool
) -> Schema:
    columns = duckdb.sql(f"""
    SELECT * FROM read_csv_auto('{csv.resolve()!s}', encoding='{encoding}') LIMIT 1
    """).columns

    desc = duckdb.sql(f"""
    DESCRIBE SELECT * FROM read_csv_auto('{csv.resolve()!s}', encoding='{encoding}', skip={skip + 1 + offset}, header=false) LIMIT 1
    """).fetchall()
    types = [row[1] for row in desc]
    # schemaを作成
    schema = Schema(name=name, encoding=encoding, skip=skip, columns=columns)

    schema.types = {col: typ for col, typ in zip(columns, types)}

    if alias:
        schema.aliases = {col: col for col in columns}
    if rate:
        schema.rates = {col: 1.0 for col in columns}

    return schema
