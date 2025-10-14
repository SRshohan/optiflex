import json
import logging
from contextlib import contextmanager
from typing import Any, Optional
import os
from open_webui.internal.wrappers import register_connection
from open_webui.env import (
    OPEN_WEBUI_DIR,
    DATABASE_URL,
    DATABASE_SCHEMA,
    SRC_LOG_LEVELS,
    DATABASE_POOL_MAX_OVERFLOW,
    DATABASE_POOL_RECYCLE,
    DATABASE_POOL_SIZE,
    DATABASE_POOL_TIMEOUT,
)
from peewee_migrate import Router
from sqlalchemy import Dialect, create_engine, MetaData, types, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool, NullPool
from sqlalchemy.sql.type_api import _T
from typing_extensions import Self

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["DB"])


class JSONField(types.TypeDecorator):
    impl = types.Text
    cache_ok = True

    def process_bind_param(self, value: Optional[_T], dialect: Dialect) -> Any:
        return json.dumps(value)

    def process_result_value(self, value: Optional[_T], dialect: Dialect) -> Any:
        if value is not None:
            return json.loads(value)

    def copy(self, **kw: Any) -> Self:
        return JSONField(self.impl.length)

    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


# Workaround to handle the peewee migration
# This is required to ensure the peewee migration is handled before the alembic migration
def handle_peewee_migration(DATABASE_URL):
    db = None
    try:
        # Replace the postgresql:// with postgres:// to handle the peewee migration
        db = register_connection(DATABASE_URL.replace("postgresql://", "postgres://"))
        migrate_dir = OPEN_WEBUI_DIR / "internal" / "migrations"
        router = Router(db, logger=log, migrate_dir=migrate_dir)
        router.run()
        db.close()

    except Exception as e:
        log.error(f"Failed to initialize the database connection: {e}")
        raise
    finally:
        # Properly closing the database connection
        if db and not db.is_closed():
            db.close()

        # Assert if db connection has been closed (only if db was successfully created)
        if db:
            assert db.is_closed(), "Database connection is still open."


# Temporarily disable complex migrations for fresh start
handle_peewee_migration(DATABASE_URL)


from google.cloud.sql.connector import Connector, IPTypes
import pg8000

# Determine if we're using Cloud SQL or local database
def get_database_engine():
    """Create database engine for SQLite (local) or PostgreSQL (Cloud Run)"""
    
    # Check if running on Cloud Run with Cloud SQL
    if os.getenv("INSTANCE_CONNECTION_NAME"):
        # Cloud Run with Cloud SQL Python Connector
        instance_connection_name = os.getenv("INSTANCE_CONNECTION_NAME")
        db_user = os.getenv("DB_USER")
        db_pass = os.getenv("DB_PASS")
        db_name = os.getenv("DB_NAME")
        
        # Use PRIVATE IP if specified, otherwise PUBLIC
        ip_type = IPTypes.PRIVATE if os.getenv("PRIVATE_IP") else IPTypes.PUBLIC
        
        # Initialize Cloud SQL Python Connector
        connector = Connector(refresh_strategy="LAZY")
        
        def getconn() -> pg8000.dbapi.Connection:
            conn: pg8000.dbapi.Connection = connector.connect(
                instance_connection_name,
                "pg8000",
                user=db_user,
                password=db_pass,
                db=db_name,
                ip_type=ip_type,
            )
            return conn
        
        # Create engine with Cloud SQL connector
        engine = create_engine(
            "postgresql+pg8000://",
            creator=getconn,
            pool_size=DATABASE_POOL_SIZE if DATABASE_POOL_SIZE > 0 else 5,
            max_overflow=DATABASE_POOL_MAX_OVERFLOW if DATABASE_POOL_MAX_OVERFLOW > 0 else 2,
            pool_timeout=DATABASE_POOL_TIMEOUT if DATABASE_POOL_TIMEOUT > 0 else 30,
            pool_recycle=DATABASE_POOL_RECYCLE if DATABASE_POOL_RECYCLE > 0 else 1800,
            pool_pre_ping=True,
        )
        return engine
    
    # Local development or direct PostgreSQL connection
    elif "sqlite" in DATABASE_URL:
        # SQLite for local development
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False}
        )
        return engine
    else:
        # Direct PostgreSQL connection (for local testing with PostgreSQL)
        if DATABASE_POOL_SIZE > 0:
            engine = create_engine(
                DATABASE_URL,
                pool_size=DATABASE_POOL_SIZE,
                max_overflow=DATABASE_POOL_MAX_OVERFLOW,
                pool_timeout=DATABASE_POOL_TIMEOUT,
                pool_recycle=DATABASE_POOL_RECYCLE,
                pool_pre_ping=True,
                poolclass=QueuePool,
            )
        else:
            engine = create_engine(
                DATABASE_URL,
                pool_pre_ping=True,
                poolclass=NullPool
            )
        return engine

# Create the engine
engine = get_database_engine()

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)
metadata_obj = MetaData(schema=DATABASE_SCHEMA)
Base = declarative_base(metadata=metadata_obj)
Session = scoped_session(SessionLocal)

# Auto-create all tables on startup (fresh start approach)
try:
    log.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    log.info("Database tables created successfully")
except Exception as e:
    log.warning(f"Table creation skipped or failed: {e}")


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db = contextmanager(get_session)
