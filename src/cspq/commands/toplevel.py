from pathlib import Path
from typing import Annotated

import typer


def toplevel(
    path: Annotated[
        Path | None, typer.Argument(help="カレントディレクトリを指定します")
    ] = None,
    echo: Annotated[bool, typer.Option(help="パスを標準出力に表示します")] = False,
):
    """
    cspqのルートのパスを取得します
    """
    if path is None:
        path = Path.cwd()

    current = path.resolve()

    for parent in [current] + list(current.parents):
        if (parent / "cspq.yaml").exists():
            if echo:
                typer.echo(parent)
            return parent

    return None
