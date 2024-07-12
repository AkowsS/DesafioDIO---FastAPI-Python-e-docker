run:
	@uvicorn src.main:app --reload

create-migrations:
	@PYTHONPATH=$PYTHONPATH:${pwd} alembic revision --autogenerate -m "init_db"

run-migrations:
	@PYTHONPATH=$PYTHONPATH:${pwd} alembic upgrade head