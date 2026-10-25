import typer
import yaml
import duckdb
from pathlib import Path
from typing import Annotated
import importlib.resources as res
import cspq.yaml_schema as ys
from .toplevel import toplevel
import cspq.utl as utl


def add(
    csv: Annotated[Path, typer.Argument(help="csv ファイルのパス")],
    name: Annotated[str | None, typer.Argument(help="テーブル/ディレクトリ名")] = None,
    encoding: Annotated[
        str, typer.Option(help="csvファイルのエンコード")
    ] = "SHIFT_JIS",
    skip: Annotated[int, typer.Option(help="csvファイルのスキップする行数")] = 0,
    alias: Annotated[bool, typer.Option(help="")] = False,
    type_info: Annotated[bool, typer.Option()] = False,
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

    root = toplevel()

    if root == None:
        typer.echo("cspq.yamlが見つかりませんでした")
        return

    with (root / "cspq.yaml").open("r", encoding="utf-8") as f:
        config: ys.Config = yaml.safe_load(f)

    # csvファイルから、列名と型を取得する
    columns = duckdb.sql(f"""
    SELECT * FROM read_csv_auto('{str(csv.resolve())}', encoding='{encoding}') LIMIT 1
    """).columns

    desc = duckdb.sql(f"""
    DESCRIBE SELECT * FROM read_csv_auto('{str(csv.resolve())}', encoding='{encoding}', skip={skip+1}, header=false) LIMIT 1
    """).fetchall()

    types = [row[1] for row in desc]
    # schemaを作成
    schema: ys.Schema = {
        "name": name,
        "pattern": name,
        "encoding": encoding,
        "skip_rows": skip,
        "columns": columns,
    }

    if alias:
        schema["aliases"] = {col: col for col in columns}
    if type_info:
        schema["types"] = {col: typ for col, typ in zip(columns, types)}
    if rate:
        schema["rates"] = {col: 1.0 for col in columns}

    # schemaを保存
    schema_file = name + ".yaml"
    schema_path = root / "schemas" / schema_file
    schema_path.parent.mkdir(parents=True, exist_ok=True)
    with schema_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(schema, f, allow_unicode=True)

    # cspq.yamlにテーブル情報を追加
    config = utl.load_config()

    if "tables" in config:
        tables = config["tables"]
    else:
        tables = {}

    tables[name] = {"path": "schemas/" + schema_file, "pattern": csv.name}
    config["tables"] = tables

    utl.write_config(config)
