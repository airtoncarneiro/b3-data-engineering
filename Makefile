up:
	docker compose -f airflow/docker-compose-Airflow.yml up --build -d

down:
	docker compose -f airflow/docker-compose-Airflow.yml down

clean:
	docker rm -f airflow || true
	docker volume prune -f
	docker system prune -f
