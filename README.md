DevOps Final Project — Flask Cinema Booking System
Project Overview

This project demonstrates a complete CI/CD pipeline for a containerized Flask web application, deployed on a local virtual machine using Docker and Docker Compose, with Jenkins used for automation.

The application simulates a cinema booking system, where users can view movie sessions, cinema halls, and reserve seats.
Business logic prevents double booking of the same seat for the same session.

Technologies Used

Python 3.11

Flask

Flask-SQLAlchemy

SQLite (with Docker volume for persistence)

Docker

Docker Compose

Jenkins

Git / GitHub

Gunicorn

Application Features

Multiple cinema halls with configurable rows and seats

Multiple movies and sessions

Seat reservation with buyer name

Prevention of double booking (occupied seats cannot be booked again)

Persistent database storage using Docker volumes

Production-ready WSGI setup using Gunicorn

Project Structure
devops_devops_final/
│
├── app/                  # Flask application package
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Service orchestration
├── Jenkinsfile           # CI/CD pipeline definition
├── entrypoint.sh         # Container startup script
├── wsgi.py               # Gunicorn WSGI entrypoint
├── init_db.py            # Database initialization and seed
├── config.py             # Application configuration
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── .gitignore

Local Run (Without Jenkins)

To run the application manually on the local VM:

docker compose up -d --build


Check running containers:

docker ps


Access the application:

http://127.0.0.1:5000


To stop the application:

docker compose down

CI/CD Pipeline (Jenkins)

The Jenkins pipeline performs the following stages:

Checkout

Cleans workspace

Clones the GitHub repository

Build & Deploy

Stops existing containers

Builds Docker image

Deploys application using Docker Compose

Healthcheck

Verifies that the application becomes available on port 5000

The pipeline is executed manually due to the use of a local virtual machine with a dynamic IP address.

Database Persistence

SQLite database is stored inside a Docker volume

Data remains intact between container restarts

Database file is not stored in Git (ignored via .gitignore)

Notes

The project is deployed on a local Kali Linux virtual machine

Auto-trigger via webhook is not used due to dynamic IP address

The focus of the project is on DevOps practices: containerization, automation, and CI/CD

Author

GitHub: https://github.com/timuuurka
