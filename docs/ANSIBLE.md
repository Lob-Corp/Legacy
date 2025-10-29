# Ansible Deployment Quick Start

Minimal Ansible setup for deploying GeneWeb Docker application.

## Prerequisites

- Ansible 2.9+ installed on your machine
- SSH access to target server(s)
- Sudo privileges on target server(s)

## Quick Deployment

### 1. Install Ansible

```bash
# Ubuntu/Debian
sudo apt-get install ansible

# macOS
brew install ansible

# Or via pip
pip install ansible
```

### 2. Configure Your Server

Edit `ansible/inventory.yml`:

```yaml
production:
  hosts:
    geneweb-prod:
      ansible_host: your-server-ip-or-hostname
      ansible_user: deploy
      ansible_port: 22
```

### 3. Test Connection

```bash
cd ansible
ansible all -i inventory.yml -m ping --limit production
```

### 4. Deploy!

```bash
cd ansible
ansible-playbook -i inventory.yml deploy.yml --limit production

# Or using Make
make deploy-prod
```

## What It Does

The deployment playbook automatically:

1. ✅ Installs Docker and Docker Compose
2. ✅ Creates deployment directory (`/home/deploy/geneweb`)
3. ✅ Copies all application files
4. ✅ Creates `.env` from `.env.example` if needed
5. ✅ Stops old containers
6. ✅ Builds Docker image
7. ✅ Starts containers
8. ✅ Waits for application to be ready

## Common Commands

```bash
# Deploy to production
make deploy-prod

# Deploy to staging
make deploy-staging

# Test connection
make ping

# Dry run (check what would change)
make check

# View all commands
make help
```

## Server Requirements

Your target server needs:
- Ubuntu 20.04+ or Debian 10+
- Python 3
- SSH access
- Sudo privileges

## File Structure

```
ansible/
├── ansible.cfg       # Ansible configuration
├── inventory.yml     # Your servers
├── deploy.yml        # Deployment playbook
├── Makefile          # Helper commands
└── README.md         # Full documentation
```

## Next Steps

See [ansible/README.md](../ansible/README.md) for:
- Detailed configuration options
- Troubleshooting guide
- Advanced usage
- CI/CD integration

## Quick Troubleshooting

**Connection fails?**
```bash
# Test SSH manually
ssh deploy@your-server

# Copy SSH key
ssh-copy-id deploy@your-server
```

**Docker permission errors?**
```bash
# On the server
sudo usermod -aG docker deploy
# Then log out and back in
```

**Application not starting?**
```bash
# Check logs on the server
cd /home/deploy/geneweb
docker-compose logs -f
```
