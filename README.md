# Comprehensive Backend Services Suite

A robust and modular backend infrastructure toolkit designed for scalable and maintainable backend systems. This suite includes API management, database interactions, and cron job scheduling, all containerized using Docker.

## Features

- **Modular Backend Architecture**: Implemented using Flask for API management and PostgreSQL for database interactions.
- **Transaction Management**: Custom-built Transaction Manager for handling complex operations and ensuring data consistency.
- **Automated Job Scheduling**: Cron jobs for scheduling and automating backend tasks.
- **Dockerized Services**: All components are containerized for ease of deployment and consistency.

## Project Structure
.
├── docker-swarm-compose
├── Services
│ ├── backend-db
│   ├── db
│   │ └── init.sql
│   ├── clean.bat
│   ├── clean.sh
│   └── Dockerfile
│ ├── backend-flask
│   ├── Dockerfile
│   ├── README
│   ├── requirements
│   └── server.py
│ ├── backend-ingest-data
│   ├── Dockerfile
│   └── (Django-related files)
│ ├── backend-internal-api
│   ├── Jobs
│     ├── PUSHDATA_JOB.py
│     └── file.txt
│   ├── Dockerfile
│   ├── API.py
│   ├── cronjob.py
│   ├── pgconn.py
│   ├── Dockerfile
│   └── tmmanage.py
└── README.md

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Project

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. **Start the Services**
   
   ```
   Use Docker Swarm to start all services: docker-compose -f docker-swarm-compose.yml up

Service Descriptions

    pg: PostgreSQL database service.
    api: Internal API service built with Python (Flask).
    django: Django service for data ingestion.
    flask: External API service built with Flask.

API Endpoints

    /testinit: Basic endpoint to verify server operation.
    /m/req_table/<table>: Manage table operations (GET, POST, DELETE).
    /pg/conn/<dbname>/<user>/<password>/<host>/<port>: Establish PostgreSQL connection.
    /pg/chk/<user>: Check PostgreSQL connection status.
    /pg/query/<query>/<user>: Execute a query on PostgreSQL.
    /admin/job/<password>/<job_action>/<job_py_name>/<time>: Manage cron jobs.

Code Structure

    backend-flask: Contains the main Flask API service.
    backend-ingest-data: Contains the Django service for data ingestion.
    backend-internal-api: Implements internal API and transaction management logic.
    backend-db: Manages PostgreSQL database setup and initialization.

Contributing

    Fork the Repository: Create your own fork of the repository.
    Create a Feature Branch: git checkout -b feature/YourFeature
    Commit Changes: git commit -am 'Add new feature'
    Push to the Branch: git push origin feature/YourFeature
    Create a New Pull Request

License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.
