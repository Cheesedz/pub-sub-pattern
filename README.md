# PubSub (Publisher-Subscriber) Pattern

## Context and Problem

The Publisher-Subscriber (PubSub) pattern is a messaging pattern that enables communication between multiple components in a system by decoupling the message producers (publishers) from the message consumers (subscribers). This pattern is particularly useful in scenarios where:

- Components need to communicate dynamically without tight coupling.
- The system must support asynchronous, scalable, and extensible communication.
- Multiple components may need to react to the same event.

### Typical Problem

In a tightly coupled system:

- **Scaling Challenges**: As more components are added, direct communication leads to increased complexity and dependency.
- **Flexibility Issues**: Adding new components or modifying existing ones requires changes to other components.
- **Reduced Fault Tolerance**: Failures in one component can directly impact others.

For example, in an e-commerce application:

- A new order is placed (publisher event).
- Multiple services (subscribers) need to react: inventory management, email notifications, analytics, etc.

Hardcoding these interactions introduces complexity, dependencies, and scalability issues.

## Benefits

PubSub messaging has the following benefits:

1. **Decoupling Subsystems**
   - Subsystems that need to communicate can be managed independently. Messages are properly managed even if one or more receivers are offline.

2. **Scalability and Responsiveness**
   - The sender can quickly send a single message to the input channel and return to its core processing responsibilities, improving scalability and responsiveness. The messaging infrastructure ensures messages are delivered to subscribers.

3. **Improved Reliability**
   - Asynchronous messaging enables applications to continue running smoothly under increased loads and handle intermittent failures more effectively.

4. **Deferred or Scheduled Processing**
   - Subscribers can delay processing messages until off-peak hours, or messages can be routed or processed according to a specific schedule.

5. **Simpler Integration**
   - Facilitates integration between systems using different platforms, programming languages, or communication protocols, as well as between on-premises systems and cloud applications.

6. **Asynchronous Workflows**
   - Supports asynchronous workflows across an enterprise, improving overall system flexibility and efficiency.

7. **Improved Testability**
   - Channels can be monitored, and messages can be inspected or logged as part of an overall integration test strategy.

8. **Separation of Concerns**
   - Each application can focus on its core capabilities, while the messaging infrastructure handles everything required to reliably route messages to multiple consumers.

## Issues and Considerations

When implementing the PubSub pattern, consider the following points:

1. **Existing Technologies**
   - Use existing messaging products and services that support the PubSub model rather than building your own. For example, Azure Service Bus, Event Hubs, Event Grid, Redis, RabbitMQ, and Apache Kafka are widely used technologies for PubSub messaging.

2. **Subscription Handling**
   - Ensure the messaging infrastructure provides mechanisms for consumers to subscribe to or unsubscribe from available channels easily.

3. **Security**
   - Restrict access to message channels using strict security policies to prevent unauthorized access and potential eavesdropping.

4. **Subsets of Messages**
   - Subscribers often need only specific subsets of messages distributed by a publisher. This can be implemented through:
     - **Topics**: Each topic has a dedicated output channel, allowing consumers to subscribe to specific topics of interest.
     - **Content Filtering**: Inspect messages and distribute them based on content. Subscribers can specify the content they want to receive.
     - **Wildcard Subscribers**: Allow subscribers to use wildcards to subscribe to multiple topics simultaneously.

5. **Bi-directional Communication**
   - In PubSub, channels are unidirectional. If subscribers need to communicate back to publishers, consider using the **Request/Reply Pattern**, which uses separate channels for sending messages and receiving replies.

6. **Message Ordering**
   - The order in which subscribers receive messages isn't guaranteed and might not reflect the order of message creation. Design the system to ensure message processing is idempotent, eliminating dependencies on message order.

7. **Message Priority**
   - For scenarios where specific messages must be processed first, implement the **Priority Queue Pattern**, ensuring high-priority messages are delivered and processed before others.

8. **Poison Messages**
   - Malformed messages or tasks requiring unavailable resources can cause failures. Use dead-letter queues to capture and store details of these messages for later analysis instead of returning them to the queue.

9. **Repeated Messages**
   - Messages might be sent more than once due to failures or retries. Implement duplicate message detection (de-duplication) using unique message IDs or ensure the message processing logic is idempotent.

10. **Message Expiration**
    - Some messages have a limited lifetime. Include expiration times in messages and discard expired ones during processing.

11. **Message Scheduling**
    - Temporarily embargo messages until a specified date or time, ensuring they are not processed prematurely.

12. **Scaling Out Subscribers**
    - If a subscriber cannot handle the rate of incoming messages, apply the **Competing Consumers Pattern** to scale out by adding more subscriber instances to process messages concurrently.

## Disadvantages

PubSub also has several disadvantages:

1. **Complexity**
   - Additional infrastructure, such as message brokers, adds complexity to the system, requiring maintenance and monitoring.

2. **Latency**
   - Asynchronous delivery might introduce delays, especially under heavy load.

3. **Debugging**
   - Troubleshooting distributed systems with PubSub can be challenging because of the decoupled nature and asynchronous communication.

4. **Message Ordering**
   - Messages may not always be processed in the order they are sent, which can lead to inconsistent states if not handled properly.

5. **Failure Handling**
   - If subscribers or brokers fail, messages might be lost unless specific mechanisms like dead-letter queues are implemented.
   - 
## When to Use This Pattern

The PubSub pattern is suitable in the following scenarios:

- **Event-Driven Systems**: Systems where components react to events, such as user actions, system state changes, or external inputs.
- **Scalable Applications**: Applications that need to handle multiple producers and consumers with minimal latency.
- **Asynchronous Communication**: Environments where components cannot afford to wait for responses from other components.
- **Extensible Architectures**: Systems where new features or services are added frequently without disrupting existing ones.

### Examples

1. **E-commerce Application**
   - **Publisher**: Order Service publishes an "Order Placed" event.
   - **Subscribers**:
     - Inventory Service updates stock.
     - Notification Service sends an order confirmation email.
     - Analytics Service logs the order for insights.

2. **IoT System**
   - **Publisher**: Temperature sensors publish data periodically.
   - **Subscribers**:
     - Dashboard Service updates live graphs.
     - Alert Service sends notifications if thresholds are exceeded.

3. **Microservices Architecture**
   - **Publisher**: User Service publishes "User Registered" events.
   - **Subscribers**:
     - Welcome Email Service sends a welcome message.
     - Rewards Service credits initial rewards to the user account.

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

