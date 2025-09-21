"""
Generate SQL INSERT statements from an Excel file.

- Uses the first row as column headers.
- Converts each subsequent row into a single INSERT statement.
- Handles strings, numbers, booleans, dates/timestamps, NULLs, and JSON-like objects.
- Quotes identifiers appropriately for the chosen SQL dialect.

Example:
    python person.py -i ./data.xlsx -t my_table -o inserts.sql --dialect postgres
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Iterable, List

import pandas as pd
import numpy as np
from decimal import Decimal
from datetime import date, datetime


DIALECTS = ("postgres", "mysql", "sqlserver", "sqlite", "oracle")


def quote_identifier(name: str, dialect: str) -> str:
    """
    Quote SQL identifiers (table and column names) safely for the given dialect.
    """
    if not isinstance(name, str) or name.strip() == "":
        raise ValueError("Identifier must be a non-empty string")

    if dialect in ("postgres", "sqlite", "oracle"):
        q = '"'
        return f'{q}{name.replace(q, q + q)}{q}'
    elif dialect == "mysql":
        q = "`"
        return f'{q}{name.replace(q, q + q)}{q}'
    elif dialect == "sqlserver":
        # SQL Server uses [name], escape ] as ]]
        return f'[{name.replace("]", "]]")}]'
    else:
        raise ValueError(f"Unsupported dialect: {dialect}")


def is_null(value: Any) -> bool:
    """
    Determine if a value should be treated as SQL NULL.
    """
    if value is None:
        return True
    try:
        # Pandas/Numpy aware null check
        return pd.isna(value)  # type: ignore[arg-type]
    except Exception:
        return False


def _format_datetime(dt: datetime) -> str:
    """
    Format datetime as 'YYYY-MM-DD HH:MM:SS' (no timezone).
    """
    # If timezone-aware, convert to UTC then drop tzinfo
    if getattr(dt, "tzinfo", None) is not None and dt.tzinfo is not None:
        # Convert to naive UTC
        dt = dt.astimezone(tz=None).replace(tzinfo=None)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def value_to_sql(value: Any, dialect: str) -> str:
    """
    Convert a Python value to a SQL literal string for the given dialect.
    """
    # NULL
    if is_null(value):
        return "NULL"

    # Booleans (support numpy bool_)
    if isinstance(value, (bool, np.bool_)):
        if dialect in ("postgres", "oracle"):
            return "TRUE" if bool(value) else "FALSE"
        # MySQL, SQL Server, SQLite often accept 1/0
        return "1" if bool(value) else "0"

    # Integers
    if isinstance(value, (int, np.integer)):
        return str(int(value))

    # Floats
    if isinstance(value, (float, np.floating)):
        f = float(value)
        if not math.isfinite(f):
            return "NULL"
        # Use repr for precision
        return repr(f)

    # Decimal
    if isinstance(value, Decimal):
        return format(value, "f")

    # Datetime-like (pandas Timestamp counts as datetime)
    if isinstance(value, pd.Timestamp):
        # Convert to Python datetime
        dt = value.to_pydatetime()
        return f"'{_format_datetime(dt)}'"
    if isinstance(value, datetime):
        return f"'{_format_datetime(value)}'"

    # Date
    if isinstance(value, date):
        return f"'{value.isoformat()}'"

    # Bytes -> hex literal when possible, else base64 could be used (kept as string here)
    if isinstance(value, (bytes, bytearray, memoryview)):
        # Represent as hex string literal
        hex_str = bytes(value).hex()
        if dialect == "postgres":
            return f"E'\\\\x{hex_str}'"  # bytea hex input
        # Generic fallback as hex in quotes
        return f"'{hex_str}'"

    # List/Dict -> JSON string
    if isinstance(value, (list, dict)):
        s = json.dumps(value, ensure_ascii=False)
        return "'" + s.replace("'", "''") + "'"

    # Everything else -> string
    s = str(value)
    return "'" + s.replace("'", "''") + "'"


def build_insert_statement(
    table: str,
    columns: List[str],
    values: Iterable[Any],
    dialect: str,
) -> str:
    col_idents = [quote_identifier(c, dialect) for c in columns]
    val_literals = [value_to_sql(v, dialect) for v in values]
    return f"INSERT INTO {quote_identifier(table, dialect)} ({', '.join(col_idents)}) VALUES ({', '.join(val_literals)});"


def read_excel(input_path: Path, sheet_name: str | int | None) -> pd.DataFrame:
    # dtype=object preserves original values better; dates will still parse as Timestamp by default
    return pd.read_excel(input_path, sheet_name=(sheet_name if sheet_name is not None else 0), dtype=object, engine="openpyxl")


def generate_inserts(
    df: pd.DataFrame,
    table: str,
    dialect: str,
    limit: int | None = None,
) -> List[str]:
    if df.empty:
        return []

    # Use columns as-is from the file
    columns = [str(c) for c in df.columns]

    inserts: List[str] = []
    row_iter = df.itertuples(index=False, name=None)
    if limit is not None and limit >= 0:
        row_iter = (row for i, row in enumerate(row_iter) if i < limit)

    for row in row_iter:
        inserts.append(build_insert_statement(table, columns, row, dialect))
    return inserts


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate SQL INSERT statements from an Excel file.")
    p.add_argument("-i", "--input", required=True, help="Path to the .xlsx file")
    p.add_argument("-t", "--table", required=True, help="Target table name")
    p.add_argument("-s", "--sheet", default=None, help="Sheet name (or index). Defaults to first sheet")
    p.add_argument("-o", "--output", default=None, help="Output .sql file. If not provided, prints to stdout")
    p.add_argument("--dialect", choices=DIALECTS, default="sqlserver", help="SQL dialect for quoting and literals")
    p.add_argument("--limit", type=int, default=378, help="Limit number of rows to convert")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    # Allow numeric sheet index as string
    sheet: str | int | None = args.sheet
    if sheet is not None and isinstance(sheet, str) and sheet.isdigit():
        sheet = int(sheet)

    df = read_excel(input_path, sheet)

    inserts = generate_inserts(df, table=args.table, dialect=args.dialect, limit=args.limit)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("\n".join(inserts) + ("\n" if inserts else ""), encoding="utf-8")
        print(f"Generated {len(inserts)} INSERT statements -> {out_path}")
    else:
        # Print to stdout
        for stmt in inserts:
            print(stmt)


if __name__ == "__main__":
    main()
