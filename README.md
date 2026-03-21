# mcp-based-web-app

A full-stack web application powered by Anthropic's **Model Context Protocol (MCP)** for AI-assisted Python code analysis. Submit Python code through a clean React frontend, and receive intelligent feedback — style suggestions, bug detection, and improvement recommendations — driven by Claude via MCP.

---

## Architecture

```
┌─────────────┐       ┌──────────────────┐       ┌────────────────┐
│  React/TS   │──REST──▶  FastAPI Server  │──MCP──▶  MCP Server    │
│  Frontend   │◀──────│  (Auth + Proxy)   │◀──────│  (FastMCP)     │
└─────────────┘       └──────────────────┘       └────────────────┘
                              │
                         ┌────┴────┐
                         │ SQLite  │
                         │   DB    │
                         └─────────┘
```

**Dual-server design:**
- **FastAPI REST server** (`server.py`) — handles user authentication (signup/login), JWT token management, and proxies code analysis requests to the MCP server.
- **MCP server** (`mcp_server.py`) — exposes AI-powered code analysis tools via the Model Context Protocol using FastMCP.

---

## Features

- **AI Code Analysis** — Submit Python code and get detailed feedback on style, bugs, and improvements via Claude (Anthropic API)
- **JWT Authentication** — Secure access & refresh token flow with password hashing (bcrypt)
- **User Management** — SQLite-backed signup/login with duplicate-user prevention
- **MCP Integration** — Protocol-driven AI tool invocation, not ad-hoc API calls
- **Infrastructure as Code** — Terraform for AWS provisioning (EC2, Route 53, NLB)
- **Automated Setup** — Ansible playbooks for server configuration and Certbot HTTPS
- **Containerized** — Dockerized for consistent deployments
- **CI/CD** — GitHub Actions pipeline for automated builds and deployments

---

## Tech Stack

| Layer          | Technology                              |
|----------------|------------------------------------------|
| Frontend       | React, TypeScript                        |
| Backend        | FastAPI, FastMCP, Python                 |
| Auth           | JWT (access + refresh tokens), bcrypt    |
| Database       | SQLite                                   |
| AI             | Anthropic Claude API via MCP             |
| Infrastructure | Terraform (AWS EC2, Route 53, NLB)       |
| Provisioning   | Ansible, Certbot (HTTPS)                 |
| Containerization | Docker                                 |
| CI/CD          | GitHub Actions                           |

---

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker (optional, for containerized deployment)
- Anthropic API key
- AWS account (for infrastructure provisioning)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/huzaifa678/mcp-based-web-app.git
cd mcp-based-web-app
```

### 2. Backend setup

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ANTHROPIC_API_KEY="your-api-key"
export SECRET_KEY="your-jwt-secret"
```

### 3. Start the MCP server

```bash
python mcp_server.py
```

### 4. Start the FastAPI server

```bash
uvicorn server:app --reload --port 8000
```

### 5. Frontend setup

```bash
cd frontend  # or wherever the React app lives
npm install
npm run dev
```

---

## API Endpoints

### Authentication

| Method | Endpoint       | Description          |
|--------|----------------|----------------------|
| POST   | `/signup`      | Register a new user  |
| POST   | `/login`       | Get access + refresh tokens |
| POST   | `/refresh`     | Refresh access token |

### Code Analysis

| Method | Endpoint       | Description                        |
|--------|----------------|------------------------------------|
| POST   | `/analyze`     | Submit Python code for AI analysis |

> All `/analyze` requests require a valid JWT access token in the `Authorization` header.

---

## Infrastructure & Deployment

### Terraform (AWS)

Provisions:
- **EC2 instance** for hosting the application
- **Route 53** DNS records
- **Network Load Balancer** for traffic distribution

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### Ansible

Automates server setup:
- Docker installation
- Application deployment
- Certbot HTTPS certificate provisioning

```bash
ansible-playbook -i inventory playbook.yml
```

### Docker

```bash
docker build -t mcp-web-app .
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY="your-key" \
  -e SECRET_KEY="your-secret" \
  mcp-web-app
```

### GitHub Actions

CI/CD is configured to automatically build and deploy on pushes to the main branch. See `.github/workflows/` for pipeline configuration.

---

## Project Structure

```
mcp-based-web-app/
├── server.py            # FastAPI REST server (auth + proxy)
├── mcp_server.py        # MCP server (AI code analysis tools)
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container configuration
├── terraform/           # AWS infrastructure as code
├── ansible/             # Server provisioning playbooks
├── frontend/            # React/TypeScript UI
├── .github/workflows/   # CI/CD pipelines
└── README.md
```

---

## How It Works

1. User signs up / logs in via the React frontend → receives JWT tokens
2. User submits Python code through the UI
3. FastAPI server validates the token and forwards the request to the MCP server
4. MCP server invokes Claude (Anthropic) via the Model Context Protocol
5. AI analyzes the code for style issues, potential bugs, and improvements
6. Results are returned to the frontend and displayed to the user

---

## License

This project is open source. See the repository for license details.

---

## Author

**Huzaifa** — [GitHub](https://github.com/huzaifa678)
