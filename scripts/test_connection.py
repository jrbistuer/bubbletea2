"""Quick check that the database connection works."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import text

from config.database import engine


def main() -> int:
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            print(f"Connection OK. SELECT 1 -> {result}")
            print(f"Dialect: {engine.dialect.name}")
            print(f"URL: {engine.url.render_as_string(hide_password=True)}")
        return 0
    except Exception as exc:
        print(f"Connection FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
