# Global Configuration Module


from pydantic import PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    '''
    Application-wide settings.
    Every field can be overridden by the corresponding upper-case env var.
    '''

    model_config = SettingsConfigDict(
        # Load from the .env file at project root
        env_file = '.env',
        env_file_encoding = 'utf-8',
        # Ignore extra fields in .env
        extra = 'ignore',
        case_sensitive = False,
    )

    # Database confifuration
    # PostgreSQL async DSN — must use the asyncpg driver scheme.
    DATABASE_URL: PostgresDsn

    # Redis configuration
    REDIS_URL: RedisDsn
    # Redis connection URL  

    # application runtime settings
    APP_ENV: str = 'development'
    # current runtime environment (development, staging, production)

    DEBUG: bool = False
    # enable debug mode

    # DB connection pool settings
    DB_POOL_SIZE: int = 10
    # core connection pool size

    DB_MAXOVERFLOW: int = 20
    # max overflow overflow above pool_size

    DB_pool_recycle: int = 1800
    # Recycle connections after this many seconds to prevent stale connections

    REDIS_MAX_CONNECTIONS: int = 50
    #max connections after this many

    @field_validator('DATABASE_URL', mode = 'before')
    @classmethod
    def _ensure_asyncpg_scheme(cls, v: str) -> str:
        """
        Validate that DATABASE_URL uses the asyncpg driver scheme.
        """
        v = str(v)
        if v.startswith("postgresql://") or v.startswith("postgres://"):
            # Auto-upgrade sync scheme to async
            v = v.replace("postgresql://", "postgresql+asyncpg://", 1).replace(
                "postgres://", "postgresql+asyncpg://", 1
            )
        return v
    
# Global singleton 
# Instantiated at module level — shared across the entire application.
# pydantic-settings objects are immutable and safe to use across threads/coroutines.
settings = Settings()  # type: ignore[call-arg]
