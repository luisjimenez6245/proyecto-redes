from db import database
from uuid import UUID

class Pack(database.Model):
    id:UUID = database.Column(database.String(36), primary_key=True)
    conent : str = database.Column(database.Text(), nullable=False)