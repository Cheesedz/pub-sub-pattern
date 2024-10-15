# Pub/Sub pattern
Demo project for Software Architecture course

## Context & problem
- Asynchronous messaging decouples senders from consumers and avoids blocking.
- Dedicated message queues for each consumer do not scale well.
- Consumers may be interested in only a subset of information.
- The publish-subscribe model allows senders to broadcast events without knowing consumer identities.
- Consumers subscribe to receive relevant events, enabling efficient scaling.

## Pub/Sub & its benefits
- **Publish-Subscribe (Pub/Sub) Model**: A messaging pattern where senders (publishers) broadcast messages without needing to know who the receivers (subscribers) are.
- **Topics**: Publishers send messages to topics, which act as channels for communication.
- **Subscribers**: Consumers subscribe to topics to receive messages that match their interests.
- **Decoupling**: Publishers and subscribers are loosely coupled, allowing them to operate independently.
- **Scalability**: Enables efficient communication with multiple consumers without direct connections.
- **Filtering**: Subscribers receive only the messages relevant to the topics they are subscribed to.

## Issues & considerations
When using the **Pub/Sub** model, there are several issues and drawbacks to consider:

1. **Message Ordering**: Ensuring message delivery in the correct order across multiple subscribers can be challenging.
   
2. **Delivery Guarantees**: Messages may be delivered more than once (duplicate messages) or not at all, depending on the implementation.

3. **Latency**: There can be a delay in message delivery to subscribers, especially in large distributed systems.

4. **Overhead in Filtering**: Subscribers may receive irrelevant messages if filtering is not fine-grained, leading to wasted processing.

5. **Complexity in Scaling**: Scaling across multiple regions or data centers can introduce complexity, such as data consistency and message loss.

6. **Subscriber Failures**: Handling slow or failed subscribers can complicate the system, as messages may need to be retried or buffered.

7. **Lack of Direct Response**: Since Pub/Sub is asynchronous, the sender does not receive immediate feedback on the message status or response from subscribers.

8. **Resource Consumption**: High throughput systems can consume significant computational resources for maintaining the message broker infrastructure.

# Demo guideline
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
- Modify .env in backend & services
```bash
PACKAGE_SERVICE_URL=
BACKEND_URL=
```
- Run backend
```bash
cd backend
uvicorn app:app --reload
```
- Run package service
```bash
cd package_service
uvicorn app:app --reload --port 8081
```
- Run Celery worker
```bash
cd backend
celery -A celery_tasks.tasks worker --loglevel=info --queues=package_queue
celery -A celery_tasks.tasks worker --loglevel=info --queues=delivery_queue
celery -A celery_tasks.tasks worker --loglevel=info --queues=mail_queue
```

