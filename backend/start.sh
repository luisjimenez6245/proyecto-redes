#!/bin/bash

pip freeze > requirements.txt
export DYLD_LIBRARY_PATH=/usr/local/mysql/lib/
export PATH=/usr/lib/postgresql/X.Y/bin/:$PATH
cd app
alembic upgrade head
cd app
python3 main.py