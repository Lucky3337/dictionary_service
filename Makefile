# Start services as develop mode
start-develop-services:
	docker-compose -f develop.yml up --build

# Stop all services
stop-all-services:
	docker-compose -f develop.yml down

# Run test in running django container
run-test:
	docker exec -ti dictionary_django_1 ./manage.py test

# Make migrations in running django container
run-makemigrations:
	docker exec -ti dictionary_django_1 ./manage.py makemigrations

# Create superuser in running django container
create-superuser:
	docker exec -ti dictionary_django_1 ./manage.py createsuperuser

# Delete db volumes
remove-db-volumes:
	 docker volume rm dictionary_dictionary_local_postgres_data_backups
	 docker volume rm dictionary_dictionary_local_postgres_data
