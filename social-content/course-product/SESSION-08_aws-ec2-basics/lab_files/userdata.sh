#!/bin/bash
apt-get update -y
apt-get install -y nginx
echo "<h1>Atithi Hotels: Book Now</h1><p>Served by $(hostname)</p>" > /var/www/html/index.html
