from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.core.config import settings
from app.models.base import Base

# IMPORTANT:
# importing app.models ensures all model classes
# are registered inside Base.metadata.
import app.models


config = context.config

config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL,
)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata