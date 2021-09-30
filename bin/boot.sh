echo "User API is starting up.."

set -e

alembic upgrade head

uvicorn main:app --host 0.0.0.0 --port 80 --reload


