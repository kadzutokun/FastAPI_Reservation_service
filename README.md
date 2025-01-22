Евгений Кононов, [22.01.2025 20:40]
# Booking System Backend

## Overview
This project provides a backend for a booking system that enables users to book seats for events, manage their bookings, and allows administrators to manage events. The backend is built using FastAPI and integrates with Kafka for logging.

## Features
- Event listing and details.
- Booking management (create, modify, cancel).
- Admin tools for event management.
- Kafka-based logging for monitoring and analysis.

## Technology Stack
- Backend: FastAPI
- Messaging: Kafka
- Database: [Specify Database, e.g., PostgreSQL]
- Frontend: Telegram Bot

## Getting Started

### Prerequisites
- Python 3.10+
- Kafka server
- Docker and Docker Compose
- [Database requirements]

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/booking-system.git

2. Build and start services using Docker Compose:
docker-compose up --build
3. Configure environment variables in .env file.
4. Use the Makefile for common tasks, such as:
Use the Makefile for common tasks, such as:
Run tests:
make test
Start development server:
make run
API Documentation
Visit /docs for interactive API documentation powered by Swagger.