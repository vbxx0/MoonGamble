docker-compose build
docker-compose run --rm api alembic upgrade head
docker-compose run --rm api alembic upgrade head
# docker-compose run --rm api python create_support.py --username admin --password keyfrfpbyj777!
docker-compose up
