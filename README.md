# python-fastapi-api

Production-ready Python REST API on AWS EC2, built with FastAPI and deployed behind nginx via a fully automated CI/CD pipeline.

**Stack:** Python 3 · FastAPI · Uvicorn · nginx · Ubuntu 22.04 EC2 (t3.micro) · Terraform · Ansible · GitHub Actions

---

## Endpoints

| Method | Path      | Description                              |
|--------|-----------|------------------------------------------|
| GET    | `/`       | HTML landing page                        |
| GET    | `/health` | Health probe (used by deploy pipeline)   |
| GET    | `/api/info` | API version and environment info       |

---

## Local Development

**Prerequisites:** Python 3.11+, pip

```bash
# Clone and install dependencies
git clone https://github.com/<your-org>/python-fastapi-api.git
cd python-fastapi-api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

# Run locally
uvicorn app.main:app --reload
# → http://localhost:8000

# Interactive API docs
# → http://localhost:8000/docs

# Run tests
pytest tests/
```

---

## Configuration

The app reads the following environment variables (see `.env.example`):

| Variable  | Description             | Default       | Secret? |
|-----------|-------------------------|---------------|---------|
| `APP_ENV` | Runtime environment     | `development` | No      |

Copy `.env.example` to `.env` for local overrides (never commit `.env`).

---

## Deployment Pipeline

Pushes to `main` trigger the GitHub Actions deploy workflow automatically:

| Stage       | Description                                                   |
|-------------|---------------------------------------------------------------|
| `provision` | Terraform: EC2 t3.micro + EIP + security group (22/80/443)    |
| `configure` | Ansible: install Python venv, FastAPI app, nginx, systemd     |
| `verify`    | Health-check `GET /health` with retries; checks `/` responds  |

Pipeline secrets are managed by the UDAP platform — no manual secret setup required.

---

## Operations

**View application logs (on the EC2 instance):**
```bash
sudo journalctl -u app -f
```

**Restart the service:**
```bash
sudo systemctl restart app
sudo systemctl restart nginx
```

**Check service status:**
```bash
sudo systemctl status app
sudo systemctl status nginx
```

**Add a new route:**
Edit `app/routers/api.py` and push to `main` — the pipeline redeploys automatically.

**Destroy infrastructure:**
Use the UDAP platform Destroy action, or dispatch the `destroy` workflow from GitHub Actions.

---

## Project Structure

```
app/
  main.py          # FastAPI app factory and root routes
  config.py        # Settings from environment variables
  routers/
    api.py         # /api/* routes (add yours here)
    health.py      # /health endpoint
  models/          # Pydantic models
  schemas/         # Request/response schemas
  static/          # Static assets (index.html landing page)
infra/
  main.tf          # Terraform backend + provider
  ec2.tf           # EC2 instance, EIP, security group, key pair
  variables.tf     # Input variables
  outputs.tf       # public_ip output consumed by pipeline
ansible/
  playbook.yml     # Server configuration playbook
tests/
  test_app.py      # pytest test suite
```

---

## Cost Estimate

~$12–20/month (1× t3.micro + Elastic IP, low traffic, us-east-1). No managed database or monitoring in this Tier 1 configuration.
