# python-fastapi-api — Build Notes

## Status
- [x] Template: fastapi-ec2@1.0.0 selected and applied
- [x] Architecture + pipeline designed and approved
- [x] Plan approved (Tier 1)
- [x] Files generated and validated (PASS)
- [ ] Repo created and pushed
- [ ] Deployed

## Key Decisions
- Blueprint: fastapi-ec2@1.0.0 (official, monitoring=none module selected)
- Region: us-east-1 (user's AWS default)
- Instance: t3.micro Ubuntu 22.04, EIP, SG 22/80/443
- nginx on port 80 → proxies to uvicorn on 127.0.0.1:8000
- Systemd service runs as `ubuntu` user (not root)
- `acl` package added to apt installs (required for Ansible become + non-root setfacl)

## Known Warnings Cleared
- `acl` package added → addresses setfacl privilege escalation warning
- No `ansible.builtin.synchronize` used → uses `ansible.builtin.copy` instead
- `wait_for_connection` tmp dir warning is benign (no www user in this stack)
- No job outputs threading masked values → all stages re-read `terraform output -raw`
- Dockerfile updated: non-root USER + HEALTHCHECK (not on deploy path but clean)

## Deploy Path
provision (Terraform: EC2 + EIP + SG + key pair)
  → configure (Ansible: apt, venv, pip, nginx, systemd, wait_for port 8000)
    → verify (curl /health with 12 retries × 15s delay; curl /)
