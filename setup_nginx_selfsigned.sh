#!/bin/bash

# Variables
DOMAIN="example.com"  # Change this to your domain or public IP address
CERT_DIR="/etc/ssl/certs"
KEY_DIR="/etc/ssl/private"
NGINX_CONF="/etc/nginx/sites-available/$DOMAIN"
NGINX_CONF_LINK="/etc/nginx/sites-enabled/$DOMAIN"

echo "Installing Nginx..."
apt update && apt install nginx -y

# Step 2: Create self-signed SSL certificate
echo "Creating self-signed SSL certificate..."
mkdir -p "$CERT_DIR" "$KEY_DIR"
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout "$KEY_DIR/$DOMAIN.key" -out "$CERT_DIR/$DOMAIN.crt" \
    -subj "/C=US/ST=YourState/L=YourCity/O=YourOrganization/OU=YourDepartment/CN=$DOMAIN"

# Step 3: Set up Nginx configuration for reverse proxy with SSL
echo "Setting up Nginx configuration..."
cat > "$NGINX_CONF" <<EOF
server {
    listen 80;
    server_name $DOMAIN;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name $DOMAIN;

    ssl_certificate $CERT_DIR/$DOMAIN.crt;
    ssl_certificate_key $KEY_DIR/$DOMAIN.key;

    location / {
        proxy_pass http://YOUR_INTERNAL_IP_OR_DOMAIN;  # Change this to your internal service IP or domain
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location ws/ {
       proxy_pass http://YOUR_INTERNAL_IP_OR_DOMAIN;
       proxy_http_version 1.1;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection "Upgrade";
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# Step 4: Enable the configuration by creating a symbolic link
ln -s "$NGINX_CONF" "$NGINX_CONF_LINK"

# Step 5: Restart Nginx to apply changes
echo "Restarting Nginx..."
systemctl restart nginx

echo "Nginx is now configured with a self-signed SSL certificate and acts as a reverse proxy."
