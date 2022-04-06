#!/bin/bash
pip freeze > requirements.txt
cd app
alembic upgrade head
cd app
python main.py