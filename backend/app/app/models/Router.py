from db import database

class Router (database.Model):
    id:str = database.Column(database.String(36), primary_key=True)
    name:str = database.Column(database.String(80), nullable=False)
    description:str = database.Column(database.String(255), nullable=False)
    status:str = database.Column(database.String(80), nullable=False)
    created_at:str = database.Column(database.DateTime, nullable=False)
    updated_at:str = database.Column(database.DateTime, nullable=False)