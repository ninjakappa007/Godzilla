# DRF Production-Style Project Requirement

## Project: Task Processing & Notification System

A backend service where users create tasks that are processed
asynchronously.\
Demonstrates DRF APIs, Redis caching, Celery workers, background
processing, and containerized deployment.

------------------------------------------------------------------------

# Architecture

Client\
↓\
DRF API (Django)\
↓\
PostgreSQL (Primary Database)

Background Processing:

API → Redis (Message Broker) → Celery Worker → DB Update / Notification

Supporting Components:

-   Redis cache for frequently accessed data
-   Celery Beat for scheduled jobs

------------------------------------------------------------------------

# APIs

## 1. Create Task

POST `/api/tasks`

Creates a new task that will be processed asynchronously.

Example Request

{ "title": "Generate Report", "payload": "input data" }

Flow

1.  Save task in PostgreSQL (status=PENDING)
2.  Send job to Celery queue
3.  Return task_id

Tech

-   DRF serializer
-   PostgreSQL transaction
-   Celery async task

------------------------------------------------------------------------

## 2. Get Task Status

GET `/api/tasks/{id}`

Example Response

{ "task_id": 1, "status": "PROCESSING", "result": null }

Flow

1.  Check Redis cache
2.  If cache miss → query PostgreSQL
3.  Store response in Redis

Tech

-   Redis caching
-   Django ORM optimization
-   indexing on task_id

------------------------------------------------------------------------

## 3. List Tasks

GET `/api/tasks`

Features

-   pagination
-   filtering
-   ordering

Tech

-   DRF pagination
-   query optimization
-   Redis cache for first page

------------------------------------------------------------------------

## 4. Retry Task

POST `/api/tasks/{id}/retry`

Flow

1.  Change status to RETRY
2.  Send task to Celery queue again

Tech

-   Celery retry queue

------------------------------------------------------------------------

## 5. Authentication

POST `/api/auth/login`

Returns JWT token.

Protected endpoints require JWT.

Tech

-   JWT authentication
-   RBAC roles (admin, user)

------------------------------------------------------------------------

# Background Processing (Celery)

Celery worker processes heavy jobs.

Example task:

process_task(task_id)

Steps

1.  Update task status → PROCESSING
2.  Execute heavy processing
3.  Save result
4.  Update status → COMPLETED
5.  Invalidate cache

Tech

-   Redis broker
-   Celery worker
-   idempotent task design

------------------------------------------------------------------------

# Scheduled Jobs (Celery Beat)

## Cleanup Old Tasks

Runs daily.

Delete tasks older than 30 days.

------------------------------------------------------------------------

## Task Monitoring

Runs every 5 minutes.

-   Detect stuck tasks
-   Retry processing

------------------------------------------------------------------------

# Redis Usage

## Message Broker

Django → Redis → Celery Worker

Used for async task queue.

------------------------------------------------------------------------

## Caching

Example cache keys

task:{id} tasks:page:1

TTL Example

300 seconds

------------------------------------------------------------------------

# Database Design

## Task Table

Fields

id\
title\
payload\
status\
result\
created_at\
updated_at

Indexes

status\
created_at

Purpose

-   fast filtering
-   background cleanup

------------------------------------------------------------------------

# Security

Authentication

-   JWT tokens

Authorization

-   RBAC

Roles

Admin - retry tasks - delete tasks

User - create tasks - view tasks

------------------------------------------------------------------------

# DevOps Setup

## Docker Containers

django-api\
postgres\
redis\
celery-worker\
celery-beat

------------------------------------------------------------------------

## Deployment Mapping

Local Component → Cloud Equivalent

Redis → AWS ElastiCache\
Postgres → AWS RDS\
Celery Worker → ECS Worker\
Celery Beat → EventBridge Scheduler

------------------------------------------------------------------------

# Logging & Monitoring

-   request logging middleware
-   structured logging

Metrics

-   task duration
-   failure count

Optional

Sentry

------------------------------------------------------------------------

# Testing

Test types

-   API tests
-   Celery task tests
-   database tests
-   authentication tests

Tools

pytest\
pytest-django

------------------------------------------------------------------------

# Project Structure

task_service

apps/ - tasks - users

api/ - serializers - views - urls

services/ - task_service.py

workers/ - celery.py - tasks.py

config/ - settings

docker/ docker-compose.yml

------------------------------------------------------------------------

# Technologies Covered

DRF APIs\
PostgreSQL\
Redis cache\
Redis message broker\
Celery workers\
Celery Beat scheduler\
JWT authentication\
RBAC authorization\
Docker containers\
ORM query optimization\
CI/CD pipeline
