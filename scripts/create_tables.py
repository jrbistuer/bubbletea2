"""Create all tables defined by the SQLAlchemy models in the configured database."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import inspect

from config.database import engine, init_db
from model.models import Base


def main() -> int:
    tables = list(Base.metadata.tables.keys())
    print(f"Creating tables: {tables}")
    init_db()

    inspector = inspect(engine)
    existing = inspector.get_table_names()
    print("Tables in database after create_all:")
    for name in existing:
        print(f"  - {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
