from pathlib import Path
from cspq.commands.toplevel import toplevel
import cspq.yaml_schema as ys
import yaml


def load_config() -> ys.Config | None:
    root = toplevel()
    if root == None:
        return None
    config_path = root / "cspq.yaml"
    with config_path.open("r", encoding="utf-8") as f:
        config: ys.Config = yaml.safe_load(f)

    return config


def load_schema(path: Path) -> ys.Schema | None:
    root = toplevel()
    if root == None:
        return None
    schema_path = root / path
    with schema_path.open("r", encoding="utf-8") as f:
        schema: ys.Schema = yaml.safe_load(f)

    return schema


def write_config(config: ys.Config):
    root = toplevel()
    config_path = root / "cspq.yaml"
    with config_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, allow_unicode=True)
