from typing import TypedDict, Required, NotRequired
from pathlib import Path


# cspq.yaml
class TableConfig(TypedDict):
    name: Required[str]  # DuckDB のテーブル名
    pattern: Required[str]  # ファイル名パターン (例: "*.csv")
    schema_path: Required[Path]


class Config(TypedDict):
    database: str  # DuckDB データベースファイル名
    tables: list[TableConfig]  # 複数テーブルの設定リスト


# schema/*.yaml
class Schema(TypedDict, tatal=False):
    skip_rows: NotRequired[list[int] | None]  # スキップする行番号リスト (例: [1])
    encoding: NotRequired[str | None]
    aliases: NotRequired[list[dict]]
    column_types: NotRequired[list[dict]]
    rates: NotRequired[list[dict]]


# ファイル名管理テーブルの定義
TABLE_FILES = """
    CREATE TABLE IF NOT EXISTS files (
        source VARCHAR,
        last_modified TIMESTAMP,
        inserted_at TIMESTAMP)"""
