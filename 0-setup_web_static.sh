#!/usr/bin/env bash
# Set up web servers for the deployment of web_static

# Install Nginx if it's not already installed
sudo apt-get update -y
sudo apt-get install nginx -y

# Create necessary directories if they don't already exist
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
sudo touch /data/web_static/releases/test/index.html
echo "<html><head></head><body>Holberton School</body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create a symbolic link to /data/web_static/releases/test/
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test /data/web_static/current

# Change ownership of the /data/ directory to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve the content of /data/web_static/current/
# Use alias inside your Nginx configuration
nginx_config="\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}"
sudo sed -i "/^\s*server_name\s/ a $nginx_config" /etc/nginx/sites-available/default
sudo service nginx restart

