import ormar as orm
from .config import db_config

class MainMeta(orm.ModelMeta):
    metadata = db_config.metadata
    database = db_config.database
