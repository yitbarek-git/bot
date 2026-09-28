import sqlite3
import logging
from contextlib import contextmanager
from app.config import DB_PATH

logger = logging.getLogger(__name__)


def dict_factory(cursor, row):
    """Row factory to return results as dictionaries (similar to PyMySQL DictCursor)."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@contextmanager
def get_db():
    """
    Context manager that yields an SQLite connection with dict-like row access.
    Automatically commits on normal exit and rolls back on exception.
    """
    connection = sqlite3.connect(
        DB_PATH,
        timeout=20.0,
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
    )
    # Enable foreign keys and set row factory
    connection.execute("PRAGMA foreign_keys = ON;")
    connection.row_factory = dict_factory

    try:
        yield connection
        connection.commit()
    except Exception as e:
        logger.error(f"Database error occurred: {e}")
        try:
            connection.rollback()
        except Exception:
            pass
        raise
    finally:
        try:
            connection.close()
        except Exception:
            pass
