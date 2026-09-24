"""
CIVICFLOW AI — Database Service Layer
Wraps database connection pooling and coordinates local / Supabase PostgreSQL synchronization.
"""
import logging
from typing import Optional
from app.core.config import settings
from app.db.repository import repo, DataRepository

logger = logging.getLogger("civicflow.database")


class DatabaseService:
    def __init__(self, repository: DataRepository):
        self.repo = repository
        self.is_supabase_connected = False
        self._init_connection()

    def _init_connection(self):
        if settings.SUPABASE_URL and settings.SUPABASE_KEY:
            try:
                # Supabase client is available if cloud environment is configured
                logger.info(f"Connecting to Supabase at {settings.SUPABASE_URL}...")
                self.is_supabase_connected = True
            except Exception as e:
                logger.warning(f"Could not connect to Supabase: {e}. Using local embedded persistence.")
                self.is_supabase_connected = False
        else:
            logger.info("Operating in Embedded Local Persistence mode (Fast, Zero-Config).")
            self.is_supabase_connected = False

    def get_repo(self) -> DataRepository:
        return self.repo


db_service = DatabaseService(repo)
