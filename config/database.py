import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.models import Base

load_dotenv()

_REQUIRED = ("USER", "PASSWORD", "HOST", "PORT", "DB")
_missing = [k for k in _REQUIRED if not os.getenv(k)]
if _missing:
    raise RuntimeError(f"Missing required env variables: {', '.join(_missing)}")

USER = os.environ["USER"]
PASSWORD = quote_plus(os.environ["PASSWORD"])
HOST = os.environ["HOST"]
PORT = os.environ["PORT"]
DB = os.environ["DB"]
CHARSET = os.getenv("CHARSET", "utf8mb4")
TIMEOUT = int(os.getenv("TIMEOUT", "10"))

DATABASE_URL = (
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}?charset={CHARSET}"
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    connect_args={"connect_timeout": TIMEOUT},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
