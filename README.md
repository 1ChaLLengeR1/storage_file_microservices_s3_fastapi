# EN
# Storage - Microservices - FastAPI
### This is my seventh project, which is typically backend - Microservices - FastApi

### Storage - Microservices - FastAPI
<img width="100%" align="left" alt="photo" src="https://github.com/1ChaLLengeR1/1ChaLLengeR1/blob/main/images/bacgrround_storage_fastapi.png" />

- link to the page: None
- similar information: None

# Project idea:
###### The idea behind the project was to build the first of its microservices to be more advanced. The plan was to build something that has a real-world impact on synchronous tasks, i.e. uploading large amounts of files or heavy files or downloading them. Also for this project I used Amazon's service - S3 for this one, because it takes a powerful machine that is able to save such amounts of data at once and a very common service used by companies/corporations, so I decided to use it and more or less understand what it connects to and is used for.

# What the project presents:
###### The project is made with the idea to use it in each subsequent project, because each project has sections with updating files or acting on them. When creating such a project, I thought about how it would be used in future projects.
-
# Technologies:
- FastAPI - Python
- Celery
- Redis
- RabbitMq
- AWS S3 Bucket
- PostgreSQL
- Docker

# Installation
###### If you want the application to run then you need to create a database in your database with your name and add the url in the alembic.ini file. Look for the key “sqlalchemy.url”. Then you need to fill in the ./env.example/dev.env.example folder (remove the .example) with the data to run your application, as it is needed for the application to run properly. You can run applications in several ways. The first is through Docker, and the second is by manually running services on your machine, i.e. redis, rabbitmq. These services need to walk on your machine to run locally without docker.

# Makefile for help commends
- install_dependencies: Installs the necessary dependencies to run the application
- migration_revision: If you have a well configured link in alembic.ini with the url to the database then this command builds tables in the database and creates migrations init
- migration_up: migrates tables to the database
- migration_down: beats tables in the database
- run_test: Starts all tests. There are about 20 of them.
- run_worker: Launches worker for work
- run_flower: Launches additional gui for celery task previews 
- run_worker_status: worker status preview
- run_app: Launching the main fastapi application

# Scripts
- ./scripts/deploy.sh: Starts building applications in production.
- ./scripts/developer.sh: Runs the entire backend for the developer using docker for tools such as fastapi, celery_worker, postgresql, rabbitmq and redis
