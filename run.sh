# We created the project using Pycharm Create Project

# Otherwise we can do
pip install fastapi uvicorn

# For database support
pip install psycopg2 psycopg2-binary sqlalchemy
pip install python-decouple databases


# After creating the models: user.py and complaint.py in models folder, we need to migrate
pip install alembic
alembic init migrations

# We create database using Pycharm, we could have done
create database alembic

# Edit alembic.ini for sqlalchemy.url
# The migrations folder has env.py
# Include the models in env.py which in turn looks in models/__init__.py
# Set target_metadata = metadata

alembic revision --autogenerate -m "Initial"

