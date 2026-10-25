import typer
import duckdb
from pathlib import Path
from typing import Annotated
import importlib.resources as res
import cspq.yaml_schema as ys


def toplevel(
    path: Annotated[
        Path, typer.Argument(help="カレントディレクトリを指定します")
    ] = Path.cwd(),
    echo: Annotated[bool, typer.Option(help="パスを標準出力に表示します")] = False,
):
    """
    cspqのルートのパスを取得します
    """

    current = path.resolve()

    for parent in [current] + list(current.parents):
        if (parent / "cspq.yaml").exists():
            if echo:
                typer.echo(parent)
            return parent

    return None
