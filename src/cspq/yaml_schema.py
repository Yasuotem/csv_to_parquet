from dataclasses import dataclass, field


@dataclass
class Table:
    path: str
    pattern: str


# cspq.yaml
@dataclass
class Config:
    db_file: str
    data: str
    tables: dict[str, Table] = field(default_factory=dict)


# schema/*.yaml
@dataclass
class Schema:
    name: str
    columns: list[str]
    skip: int = 0  # ヘッダー前のスキップする行数
    offset: int = 0  # ヘッダー後のスキップする行数
    encoding: str = "SHIFT_JIS"
    types: dict[str, str] = field(default_factory=dict)
    aliases: dict[str, str] = field(default_factory=dict)
    rates: dict[str, float] = field(default_factory=dict)


def test():
    print("hello")


# ファイル名管理テーブルの定義
TABLE_FILES = """
    CREATE TABLE IF NOT EXISTS files (
        source VARCHAR,
        last_modified TIMESTAMP,
        inserted_at TIMESTAMP)"""
