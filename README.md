# Two-Tier CI/CD App — FastAPI + MySQL on AWS EC2

A fully automated CI/CD pipeline that builds and deploys a two-tier web application (FastAPI + MySQL) on AWS EC2, using Jenkins, Docker, and Docker Compose. Every push to `main` triggers Jenkins via a GitHub webhook, which builds a fresh Docker image and redeploys the stack automatically — no manual steps required.

---

## Architecture

```
Developer --push--> GitHub Repo --webhook--> Jenkins (EC2)
                                                   |
                                        1. Clone repo
                                        2. Build Docker image
                                        3. docker compose up -d --build
                                                   |
                                                   v
                                     +--------------------------+
                                     |     EC2 Instance         |
                                     |                          |
                                     |  +--------------------+  |
                                     |  |  FastAPI Container |  |
                                     |  +--------------------+  |
                                     |            |             |
                                     |            v             |
                                     |  +--------------------+  |
                                     |  |  MySQL Container   |  |
                                     |  +--------------------+  |
                                     +--------------------------+
```

---

## Tech Stack

- **App**: Python (FastAPI, SQLAlchemy)
- **Database**: MySQL 8
- **Containerization**: Docker, Docker Compose
- **CI/CD**: Jenkins (Pipeline as Code via `Jenkinsfile`)
- **Infra**: AWS EC2 (Ubuntu)
- **Automation**: GitHub Webhooks

---

## Repository Structure

```
.
├── app.py              # FastAPI application entrypoint
├── config.py           # Database configuration (DATABASE_URL, etc.)
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container build definition for the app
├── docker-compose.yml   # Orchestrates app + MySQL containers
├── Jenkinsfile          # Pipeline-as-code build/deploy stages
└── README.md
```

---

## API Endpoints

| Method | Path          | Description                          |
|--------|---------------|---------------------------------------|
| GET    | `/`           | Basic health/status message           |
| GET    | `/health`     | App liveness check                    |
| GET    | `/db-health`  | Verifies live connectivity to MySQL   |

---

## Running Locally (without Docker)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

The app will be available at `http://localhost:5000`. Note that `/db-health` will report `disconnected` when run this way, since MySQL is only available via Docker Compose.

## Running Locally (with Docker)

```bash
docker build -t flask-app:latest .
docker run -p 5000:5000 flask-app:latest
```

## Running the Full Stack (App + MySQL)

```bash
docker compose up -d --build
```

Check container status:

```bash
docker ps
```

---

## CI/CD Pipeline (Jenkins)

The `Jenkinsfile` defines three stages:

1. **Clone Code** — pulls the latest commit from the `main` branch
2. **Build Docker Image** — builds the app image via `docker build -t flask-app:latest .`
3. **Deploy with Docker Compose** — tears down any existing stack and redeploys with `docker compose up -d --build`

### Trigger

Builds run automatically on every push to `main`, via a GitHub webhook pointed at:

```
http://<ec2-public-ip>:8080/github-webhook/
```

---

## Infrastructure Setup Summary (EC2)

- **Instance type**: t3.micro
- **Swap**: 1 GB swap file added for headroom on low-RAM builds
- **Root volume**: resized to 30 GB to accommodate Docker images, build workspaces, and Jenkins plugins
- **Security Group inbound rules**:

| Type       | Port | Source      | Purpose            |
|------------|------|-------------|---------------------|
| SSH        | 22   | My IP       | Server access        |
| HTTP       | 80   | 0.0.0.0/0   | Web (if used)        |
| Custom TCP | 5000 | 0.0.0.0/0   | FastAPI app           |
| Custom TCP | 8080 | 0.0.0.0/0   | Jenkins dashboard      |

---

## License

This project is provided as-is for learning and demonstration purposes.