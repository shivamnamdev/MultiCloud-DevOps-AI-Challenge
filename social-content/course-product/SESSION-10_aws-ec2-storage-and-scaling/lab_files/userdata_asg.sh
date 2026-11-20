#!/bin/bash
# Runs on every NEW building made from the atithi-web-v1 image. The image already has nginx, but its page was
# written on the builder and says the builder's name, so rewrite the page with THIS building's name.
echo "<h1>Atithi Hotels: Book Now</h1><p>Served by $(hostname)</p>" > /var/www/html/index.html
apt-get install -y stress-ng >/dev/null 2>&1
