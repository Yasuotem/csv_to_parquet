import typer
import duckdb
from pathlib import Path
from typing import Annotated
import importlib.resources as res

app = typer.Typer()


def main():
    app()


@app.command()
def init(path: Path = typer.Argument("", help="")):
    """
    データ置き場の雛形を作成するコマンドです
    実行すると csvpq.yaml csvpq.duckdb data/ が生成されます
    """
    print("Hello")


@app.command()
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


@app.command()
def load(csv: Annotated[list[Path], typer.Argument()]):
    """
    csvpq.yaml のスキーマを元に csv を parquet に変換します
    """
    for e in csv:
        print(e)
