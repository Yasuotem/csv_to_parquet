from typing import TypedDict, Required, NotRequired
from pathlib import Path


# cspq.yaml
class TableConfig(TypedDict):
    name: Required[str]  # DuckDB のテーブル名
    pattern: Required[str]  # ファイル名パターン (例: "*.csv")
    schema_path: Required[Path]


class Config(TypedDict):
    db_file: Required[Path]  # DuckDB データベースファイル名
    data: Required[Path]
    tables: NotRequired[list[TableConfig]]  # 複数テーブルの設定リスト


# schema/*.yaml
class Schema(TypedDict, total=False):
    skip_rows: Required[list[int] | None]  # スキップする行番号リスト (例: [1])
    encoding: Required[str | None]
    aliases: NotRequired[list[dict[str, str]]]
    column_types: NotRequired[list[dict[str, str]]]
    rates: NotRequired[list[dict[str, float]]]


def test():
    print("hello")


# ファイル名管理テーブルの定義
TABLE_FILES = """
    CREATE TABLE IF NOT EXISTS files (
        source VARCHAR,
        last_modified TIMESTAMP,
        inserted_at TIMESTAMP)"""
