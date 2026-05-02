# Real-Time Order Lifecycle Data Platform

## Overview

This project is a **production-style event-driven data engineering system** that simulates the lifecycle of an order — from creation to delivery — using Kafka and microservices.

It is designed to demonstrate **real-world data engineering concepts** like:

* Event-driven architecture
* Asynchronous processing
* Fault tolerance (retry + DLQ)
* State management
* Observability (metrics API)

---

## Architecture

```
Order API -> Kafka -> Consumer Service -> PostgreSQL
                |           
            DLQ (Dead Letter Queue)
```

---

## Data Flow

1. User hits API -> creates an order
2. Order event is published to Kafka (`order-events`)
3. Consumer reads event:

   * Stores event in `order_events` (event log)
   * Updates `orders` (current state)
4. If DB write fails:

   * Retry (3 attempts)
   * If still fails -> send to `dlq-events`
5. Metrics are tracked for monitoring

---

## Tech Stack

* **FastAPI** -> API layer
* **Kafka** -> Event streaming
* **PostgreSQL** -> Storage
* **Python (kafka-python, psycopg2)** -> Processing
* **Docker (optional)** -> Containerization

---

## Database Design

### 1. `order_events` (Event Store - Immutable)

```sql
CREATE TABLE order_events (
    event_id TEXT PRIMARY KEY,
    order_id TEXT,
    event_type TEXT,
    service TEXT,
    timestamp TIMESTAMP
);
```

---

### 2. `orders` (State Store - Mutable)

```sql
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    user_id TEXT,
    current_status TEXT,
    updated_at TIMESTAMP
);
```

---

## Setup Instructions

---

### 1. Start Kafka (Docker)

```bash
docker-compose up -d
```

---

### 2. Create Kafka Topics

```bash
kafka-topics --create \
  --topic order-events \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1

kafka-topics --create \
  --topic dlq-events \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1
```

---

### 3. Setup PostgreSQL

Create database:

```sql
CREATE DATABASE orders_db;
```

Connect and create tables:

```sql
-- Event table
CREATE TABLE order_events (
    event_id TEXT PRIMARY KEY,
    order_id TEXT,
    event_type TEXT,
    service TEXT,
    timestamp TIMESTAMP
);

-- State table
CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,
    user_id TEXT,
    current_status TEXT,
    updated_at TIMESTAMP
);
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Run Services

#### Start API

```bash
uvicorn api.main:app --reload --port 8001
```

---

#### Start Consumer

```bash
python processor/consumer.py
```

---

## API Endpoints
Refer to FAST API Docs one app is UP and running

### Order Timeline

```http
GET /orders/{order_id}/timeline
```

Returns full lifecycle of an order.

---

## Reliability Features

* Retry mechanism (3 attempts)
* Dead Letter Queue (DLQ)
* Idempotent processing (no duplicate inserts)
* Fault-tolerant consumer design

---

---

## Key Learnings

* Event-driven system design
* Kafka consumer groups & scaling
* Schema separation (event store vs state store)
* Handling failures in distributed systems
* Building observable data pipelines

---

## Future Improvements

* Dockerize full system (API + Consumer + DB)
* Add Prometheus + Grafana for monitoring
* DLQ reprocessing service
* Partition-based scaling
* CI/CD pipeline

---

## Summary

This project demonstrates how to build a **resilient, scalable, and observable data pipeline** using modern data engineering practices.

It goes beyond a simple Kafka demo and implements **real production concepts** like retry handling, DLQ, and event sourcing.

---
