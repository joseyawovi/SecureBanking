# SecureBank Deployment Guide

This guide provides instructions for deploying the SecureBank application to production environments.

## Prerequisites

Before deploying, ensure you have the following:

- Python 3.9+ installed on your server
- PostgreSQL database server
- A web server (Nginx or Apache)
- WSGI server (Gunicorn or uWSGI)
- SSL certificate for HTTPS

## 1. Prepare Environment Variables

Create a `.env` file in the project root with the following variables (replace with your values):

```
# Django settings
DJANGO_SECRET_KEY=your-very-secure-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database settings
DATABASE_URL=postgres://username:password@host:port/dbname
PGDATABASE=dbname
PGUSER=username
PGPASSWORD=password
PGHOST=hostname
PGPORT=5432

# Email settings
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Security settings
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Set Up the Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

## 4. Collect Static Files

```bash
python manage.py collectstatic
```

## 5. Set Up Gunicorn

Install Gunicorn:

```bash
pip install gunicorn
```

Create a systemd service file at `/etc/systemd/system/securebank.service`:

```
[Unit]
Description=SecureBank Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/banking_system
ExecStart=/path/to/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/path/to/securebank.sock \
          banking_system.wsgi:application
EnvironmentFile=/path/to/banking_system/.env
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Start and enable the service:

```bash
sudo systemctl start securebank
sudo systemctl enable securebank
```

## 6. Configure Nginx

Create an Nginx configuration file at `/etc/nginx/sites-available/securebank`:

```
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/ssl/certificate.crt;
    ssl_certificate_key /path/to/ssl/private.key;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Other security headers
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' https://cdn.tailwindcss.com https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; img-src 'self' data:; font-src 'self' https://cdnjs.cloudflare.com; connect-src 'self'" always;

    location /static/ {
        alias /path/to/banking_system/staticfiles/;
    }

    location /media/ {
        alias /path/to/banking_system/media/;
    }

    location / {
        proxy_pass http://unix:/path/to/securebank.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/securebank /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 7. Setup Backups

### Database Backups

Create a backup script at `/path/to/backup.sh`:

```bash
#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/path/to/backups"
FILENAME="$BACKUP_DIR/securebank_db_$TIMESTAMP.sql"

# Ensure backup directory exists
mkdir -p $BACKUP_DIR

# Set environment variables from .env file
source /path/to/banking_system/.env

# PostgreSQL backup
pg_dump -h $PGHOST -U $PGUSER -d $PGDATABASE -f $FILENAME

# Compress backup
gzip $FILENAME

# Rotate backups (keep last 30 days)
find $BACKUP_DIR -name "securebank_db_*.sql.gz" -type f -mtime +30 -delete
```

Set up a cron job to run daily:

```bash
chmod +x /path/to/backup.sh
(crontab -l; echo "0 2 * * * /path/to/backup.sh") | crontab -
```

## 8. Security Considerations

- Regularly update all packages and dependencies
- Use a Web Application Firewall (WAF)
- Configure fail2ban to prevent brute force attacks
- Set up monitoring and alerts
- Perform regular security audits

## 9. Monitoring

Set up monitoring tools:

- Prometheus for metrics collection
- Grafana for visualization
- ELK stack for log management

## 10. Scaling (for high-traffic applications)

- Use a load balancer to distribute traffic
- Configure database replication
- Implement caching with Redis or Memcached
- Set up CDN for static assets

## Deployment Checklist

Before launching, verify:

- [ ] Environment variables are properly set
- [ ] Database migrations are applied
- [ ] Static files are collected
- [ ] SSL certificates are valid and properly configured
- [ ] Backup system is working
- [ ] Error monitoring is set up
- [ ] Security headers are configured
- [ ] Test all functionality in the production environment

## Troubleshooting

### Common Issues

1. **Static Files Not Loading**
   - Check your STATIC_ROOT and STATIC_URL settings
   - Verify Nginx configuration for static files

2. **Database Connection Issues**
   - Check database credentials in .env file
   - Verify firewall settings
   - Check PostgreSQL server logs

3. **WSGI Errors**
   - Check Gunicorn log files
   - Verify Python path and environment variables

For additional help, refer to the Django deployment documentation or contact the development team.