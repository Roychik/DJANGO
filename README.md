## Django Bank App
### Prerequisites
Make sure you have the following tools installed on your machine.
- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker compose: [Install Docker Compose](https://docs.docker.com/compose/)
### Clone the repository
```bash
git clone https://github.com/zakharilchuk/django-app.git
cd django-app
```
### Setting up environment
```bash
cp .env.example .env
```
Open the **\`.env\`** file and set the appropriate values for environment variables.
### Run and build
To start the application services inside Docker containers (without rebuilding images), use:
```bash
docker compose up
```
If you need to rebuild images before running the services, use:
```bash
docker compose up --build
```
To stop and remove the running services, run:
```bash
docker compose down
```

