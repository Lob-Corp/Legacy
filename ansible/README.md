# Ansible Deployment for GeneWeb

This directory contains Ansible configuration for deploying the GeneWeb Docker application.

## Quick Start

### 1. Install Ansible

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ansible

# macOS
brew install ansible

# Or via pip
pip install ansible
```

### 2. Configure Inventory

Edit `inventory.yml` to set your server details:

```yaml
production:
  hosts:
    geneweb-prod:
      ansible_host: your-server.example.com
      ansible_user: deploy
      ansible_port: 22
```

### 3. Test Connection

```bash
cd ansible
ansible all -i inventory.yml -m ping --limit production

# If inventory is encrypted with vault:
ansible all -i inventory.yml -m ping --limit production --ask-vault-pass
# Or if vault_password_file is configured in ansible.cfg, just:
ansible all -i inventory.yml -m ping --limit production
```

### 4. Deploy

```bash
cd ansible

# Deploy to production
ansible-playbook -i inventory.yml deploy.yml --limit production

# Deploy to staging
ansible-playbook -i inventory.yml deploy.yml --limit staging

# Deploy to specific host
ansible-playbook -i inventory.yml deploy.yml --limit geneweb-prod
```

## What the Playbook Does

1. **Install Dependencies**: Installs Docker and Docker Compose
2. **Copy Files**: Syncs application files to the server
3. **Build Image**: Builds the Docker image on the server
4. **Start Containers**: Starts the application with docker-compose

## Directory Structure

```
ansible/
├── ansible.cfg        # Ansible configuration
├── inventory.yml      # Server inventory
├── deploy.yml         # Main deployment playbook
└── README.md         # This file
```

## Deployment Variables

Edit these in `inventory.yml`:

| Variable | Default | Description |
|----------|---------|-------------|
| `ansible_host` | - | Server hostname or IP |
| `ansible_user` | `deploy` | SSH user |
| `ansible_port` | `22` | SSH port |
| `deploy_dir` | `/home/deploy/geneweb` | Deployment directory |

## Requirements

### On Control Machine (your computer)
- Ansible 2.9+
- SSH access to target servers

### On Target Servers
- Ubuntu 20.04+ or Debian 10+ (or adjust package manager)
- SSH access
- Sudo privileges for the deploy user
- Python 3

## Common Tasks

### Deploy to Production

```bash
cd ansible
ansible-playbook -i inventory.yml deploy.yml --limit production
```

### Deploy with Verbose Output

```bash
ansible-playbook -i inventory.yml deploy.yml --limit production -vv
```

### Check What Would Change (Dry Run)

```bash
ansible-playbook -i inventory.yml deploy.yml --limit production --check
```

### Deploy Only to Specific Host

```bash
ansible-playbook -i inventory.yml deploy.yml --limit geneweb-prod
```

### Update Only Application Code (Skip Docker Build)

```bash
# Edit deploy.yml and comment out the build step, or use tags
ansible-playbook -i inventory.yml deploy.yml --limit production --skip-tags build
```

## SSH Key Setup

### Generate SSH Key

```bash
ssh-keygen -t ed25519 -C "deployment@geneweb"
```

### Copy Key to Server

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub deploy@your-server.example.com
```

### Use Custom SSH Key

Edit `inventory.yml`:

```yaml
geneweb-prod:
  ansible_host: your-server.example.com
  ansible_user: deploy
  ansible_ssh_private_key_file: ~/.ssh/geneweb_deploy_key
```

## Security Best Practices

### Protect Sensitive Files

Ensure these files are never committed to git:

```bash
# Already in .gitignore, but verify:
echo "vault_pass.txt" >> ansible/.gitignore
echo "*.pem" >> ansible/.gitignore
echo "*.key" >> ansible/.gitignore
```

### Use Ansible Vault for Inventory

If your inventory contains sensitive information (IPs, usernames):

```bash
# Encrypt inventory
ansible-vault encrypt inventory.yml

# Configure vault password file in ansible.cfg
echo "vault_password_file = vault_pass.txt" >> ansible.cfg
```

### Secure Vault Password

```bash
# Store vault password securely
echo "your-vault-password" > ~/.ansible/vault_pass.txt
chmod 600 ~/.ansible/vault_pass.txt

# Or use environment variable
export ANSIBLE_VAULT_PASSWORD_FILE=~/.ansible/vault_pass.txt
```

## Server Setup

### Create Deploy User

On the target server:

```bash
# Create user
sudo useradd -m -s /bin/bash deploy

# Add to sudo group
sudo usermod -aG sudo deploy

# Set password (optional)
sudo passwd deploy

# Allow passwordless sudo (optional, for automation)
echo "deploy ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/deploy
```

## Troubleshooting

### Connection Issues

```bash
# Test SSH connection
ssh deploy@your-server.example.com

# Test Ansible connection
ansible all -i inventory.yml -m ping --limit production
```

### Docker Permission Issues

If containers fail to start, ensure the deploy user is in the docker group:

```bash
# On the server
sudo usermod -aG docker deploy

# Log out and back in, or
sudo -u deploy -i
```

### Application Not Starting

Check logs on the server:

```bash
cd /home/deploy/geneweb
docker-compose logs -f
```

### Firewall Issues

Ensure port 8080 is open:

```bash
# Ubuntu/Debian with ufw
sudo ufw allow 8080/tcp

# Or with iptables
sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
```

## Advanced Usage

### Using Ansible Vault for Secrets

Ansible Vault allows you to encrypt sensitive data like passwords, SSH keys, and inventory files.

#### Create Vault Password File

Store your vault password in a file (recommended for automation):

```bash
# Create password file
echo "your-secure-vault-password" > ~/.ansible/vault_pass.txt
chmod 600 ~/.ansible/vault_pass.txt

# Or for this project specifically
echo "your-secure-vault-password" > ansible/vault_pass.txt
chmod 600 ansible/vault_pass.txt
```

**Important**: Add `vault_pass.txt` to `.gitignore` to prevent committing it!

#### Configure Ansible to Use Vault Password File

In `ansible.cfg`:

```ini
[defaults]
vault_password_file = vault_pass.txt
# or
vault_password_file = ~/.ansible/vault_pass.txt
```

With this configured, you won't need `--ask-vault-pass` on every command.

#### Encrypt Sensitive Files

```bash
# Encrypt entire inventory file
ansible-vault encrypt inventory.yml
```

#### Edit Encrypted Files

```bash
# Edit encrypted inventory
ansible-vault edit inventory.yml

# Edit with specific vault password file
ansible-vault edit inventory.yml --vault-password-file=vault_pass.txt
```

#### Decrypt Files (if needed)

```bash
# Decrypt file
ansible-vault decrypt inventory.yml

# View encrypted file without decrypting
ansible-vault view inventory.yml
```

#### Run Playbook with Vault

```bash
# If vault_password_file is NOT configured in ansible.cfg:
ansible-playbook -i inventory.yml deploy.yml --ask-vault-pass

# With vault password file specified:
ansible-playbook -i inventory.yml deploy.yml --vault-password-file=vault_pass.txt

# If vault_password_file IS configured in ansible.cfg:
ansible-playbook -i inventory.yml deploy.yml
# (no additional flags needed)
```

#### Best Practices for Vault

1. **Separate sensitive data**: Keep secrets in separate files (e.g., `vars/secrets.yml`)
2. **Use vault password file**: Store in `~/.ansible/vault_pass.txt` and add to `ansible.cfg`
3. **Add to .gitignore**: Never commit `vault_pass.txt` or decrypted files
4. **Use different vault passwords**: Use different passwords for production vs staging
5. **Encrypt inventory**: If your inventory contains IP addresses or hostnames you want to keep private

#### Example: Encrypted Inventory Setup

```bash
# 1. Create vault password file
echo "MySecureVaultPassword123!" > ansible/vault_pass.txt
chmod 600 ansible/vault_pass.txt

# 2. Encrypt inventory
ansible-vault encrypt ansible/inventory.yml --vault-password-file=ansible/vault_pass.txt

# 3. Configure ansible.cfg (already done in this project)
# vault_password_file = vault_pass.txt

# 4. Deploy normally (vault is transparent now)
cd ansible
ansible-playbook -i inventory.yml deploy.yml --limit production

# 5. To edit inventory later
ansible-vault edit inventory.yml
```

#### Multiple Vault Passwords

If you need different passwords for different environments:

```bash
# Create separate password files
echo "prod-password" > ~/.ansible/vault_pass_prod.txt
echo "staging-password" > ~/.ansible/vault_pass_staging.txt

# Encrypt with specific password
ansible-vault encrypt prod_inventory.yml --vault-id prod@~/.ansible/vault_pass_prod.txt

# Deploy with specific vault ID
ansible-playbook -i prod_inventory.yml deploy.yml --vault-id prod@~/.ansible/vault_pass_prod.txt
```

### Custom Variables

Create `vars.yml`:

```yaml
---
app_name: geneweb
deploy_dir: /opt/geneweb
docker_image: geneweb:latest
```

Update playbook to include:

```yaml
- name: Deploy GeneWeb
  hosts: all
  vars_files:
    - vars.yml
  tasks:
    # ... tasks
```

## Environment-Specific Configurations

You can create separate variable files for each environment:

```bash
ansible/
├── vars/
│   ├── production.yml
│   ├── staging.yml
│   └── development.yml
```

Then deploy with:

```bash
ansible-playbook -i inventory.yml deploy.yml \
  --limit production \
  --extra-vars "@vars/production.yml"
```

## Continuous Deployment

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Ansible
        run: pip install ansible
      
      - name: Setup SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
      
      - name: Deploy with Ansible
        run: |
          cd ansible
          ansible-playbook -i inventory.yml deploy.yml --limit production
```

## Rollback

To rollback to a previous version:

```bash
# On the server
cd /home/deploy/geneweb
git checkout <previous-commit>
docker-compose build
docker-compose up -d
```

## Support

For issues:
1. Check server logs: `docker-compose logs`
2. Check Ansible output for errors
3. Verify SSH access and sudo permissions
4. Ensure Docker is installed and running
