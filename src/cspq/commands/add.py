import typer
import yaml
import duckdb
from pathlib import Path
from typing import Annotated
import importlib.resources as res
import cspq.yaml_schema as ys


def add(
    csv: Annotated[Path, typer.Argument(help="csv ファイルのパス")],
    name: Annotated[str | None, typer.Argument(help="テーブル/ディレクトリ名")] = None,
    arias: Annotated[bool, typer.Option(help="")] = False,
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
        name = csv.stem()
