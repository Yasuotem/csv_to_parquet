from dataclasses import asdict
from pathlib import Path

import typer
import yaml

from cspq.commands.toplevel import toplevel
from cspq.yaml_schema import Config, Schema


def load_config() -> Config:
    root = toplevel()
    if root == None:
        raise typer.Exit(code=1)

    config_path = root / "cspq.yaml"
    with config_path.open("r", encoding="utf-8") as f:
        config = Config(**yaml.safe_load(f))

    return config


def load_schema(path: Path) -> Schema:
    root = toplevel()
    if root == None:
        raise typer.Exit(code=1)

    schema_path = root / path
    with schema_path.open("r", encoding="utf-8") as f:
        schema = Schema(**yaml.safe_load(f))

    return schema


def write_config(config: Config):
    root = toplevel()
    config_path = root / "cspq.yaml"
    with config_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(asdict(config), f, sort_keys=False, allow_unicode=True)
