from contextlib import contextmanager
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from time import sleep


# init in init_db_connection
engine = None
Session = None


def generate_db_uri(
    driver: str = "postgresql",
    user: str = None,
    password: str = None,
    host: str = None,
    port: int = 5432,
    db: str = None,
):
    """
    Generate a database URI string with optional overrides for any env variable
    @param driver: default "postgres"
    @param user
    @param password
    @param host
    @param port: default 5432
    @param db
    @return: string URI
    """
    driver = getenv("DB_DRIVER") or driver
    user = getenv("POSTGRES_USER") or user
    password = getenv("POSTGRES_PASSWORD") or password
    host = getenv("POSTGRES_HOST") or host
    port = getenv("POSTGRES_PORT") or port
    db = getenv("POSTGRES_DB") or db

    for uri_key, uri_val in [
        ("user", user),
        ("password", password),
        ("host", host),
        ("db", db),
    ]:
        if uri_val == None:
            raise RuntimeError(
                f"Incomplete DB URI component given: '{uri_key}'")
    return f"{driver}://{user}:{password}@{host}:{port}/{db}"


def init_db_connection():
    """
    Instantiates a singleton DB engine
    """
    global engine, Session
    if engine != None:
        return
    uri = generate_db_uri()
    sleep(10)    # wait for postgres container to launch
    engine = create_engine(uri)
    engine.connect()
    Session = sessionmaker(bind=engine)


@contextmanager
def create_session():
    """
    Creates and returns a session
    Uses contextlib's contextmanager decorator to allow for generator syntax:
    with create_session() as session:
        ...etc.
    @return: active session
    """
    global Session
    if Session == None:
        raise RuntimeError(
            """
        Session Maker is None. 
        Please run init_db_connection() before defining tables
        """
        )
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def create_table(table):
    """
    Generate table from declarative base definition
    @param table: table which inherits from Base
    """
    global engine
    if engine == None:
        raise RuntimeError(
            """
        DB engine is None. 
        Please run init_db_connection() before defining tables
        """
        )
    table.__table__.create(bind=engine, checkfirst=True)


def get_engine():
    """
    Get raw engine object. Should not be used unless explicitly needed.
    """
    global engine
    return engine
