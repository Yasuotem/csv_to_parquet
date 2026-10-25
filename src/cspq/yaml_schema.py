from typing import TypedDict, Required, NotRequired


class Table(TypedDict):
    path: Required[str]
    pattern: Required[str]


# cspq.yaml
class Config(TypedDict):
    db_file: Required[str]  # DuckDB データベースファイル名
    data: Required[str]
    tables: NotRequired[
        dict[str, Table]
    ]  # 複数テーブルの設定リスト[テーブル名, schemaのパス]


# schema/*.yaml
class Schema(TypedDict, total=False):
    name: Required[str]
    skip_rows: Required[list[int] | None]  # スキップする行番号リスト (例: [1])
    encoding: Required[str | None]
    columns: Required[list[str]]
    aliases: NotRequired[list[dict[str, str]]]
    types: NotRequired[list[dict[str, str]]]
    rates: NotRequired[list[dict[str, float]]]


def test():
    print("hello")


# ファイル名管理テーブルの定義
TABLE_FILES = """
    CREATE TABLE IF NOT EXISTS files (
        source VARCHAR,
        last_modified TIMESTAMP,
        inserted_at TIMESTAMP)"""
