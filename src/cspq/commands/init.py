import typer
from pathlib import Path
import duckdb
from pathlib import Path
from typing import Annotated
import importlib.resources as res
import cspq.yaml_schema as ys


def init(path: Path = typer.Argument("", help="")):
    """
    データ置き場の雛形を作成するコマンドです
    実行すると csvpq.yaml csvpq.duckdb data/ が生成されます
    """
    files = res.files("cspq.templates")

    try:
        yaml_text = files.joinpath("cspq.yaml").read_text()
        duck_bytes = files.joinpath("cspq.duckdb").read_bytes()
    except FileNotFoundError as e:
        typer.echo(f"テンプレートファイルが見つかりません: {e}")
        raise typer.Exit(code=1)

    try:
        path.joinpath("cspq.yaml").write_text(yaml_text)
        path.joinpath("cspq.duckdb").write_bytes(duck_bytes)
    except OSError as e:
        typer.echo(f"ファイルの書き込みに失敗しました: {e}")
        raise typer.Exit(code=1)
