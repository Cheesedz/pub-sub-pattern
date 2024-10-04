# Pub/Sub pattern
Mini project for Software Architecture course

## Requirements
- Python 3+
- Pika
- RabibitMQ
- Celery
- Docker

## Installation
- Install dependencies
```bash
cd backend
pip install -r requirements.txt
```
- Pull RabbitMQ image
```bash
docker pull rabbitmq
```
- Run RabbitMQ
```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
```
- Run applications
```bash
cd backend
uvicorn app:app --reload
```
- Run Celery worker
```bash
cd backend
celery -A celery_tasks.tasks worker --loglevel=INFO
```

