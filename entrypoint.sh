#!/bin/bash

echo "PostgreSQL started"

export PYTHONPATH="."

alembic upgrade head

echo "
O——————————————————O
     programming_quiz started…
O——————————————————O
"
uvicorn --host=0.0.0.0 app.main:app

exec "$@"
