import typer
import duckdb
from pathlib import Path
from typing import Annotated
import importlib.resources as res
import cspq.yaml_schema as ys

app = typer.Typer()


@app.command()
def load(csv: Annotated[list[Path], typer.Argument()]):
    """
    csvpq.yaml のスキーマを元に csv を parquet に変換します
    """
    for e in csv:
        print(e)
