#!/bin/bash
# Birinchi marta server sozlash uchun
set -e

PROJECT_DIR=/home/online-shop-api

echo "=== 1. Paketlar o'rnatilmoqda ==="
apt update && apt install -y python3 python3-pip python3-venv nginx

echo "=== 2. Python venv va paketlar ==="
cd $PROJECT_DIR
python3 -m venv myenv
myenv/bin/pip install --upgrade pip
myenv/bin/pip install gunicorn
myenv/bin/pip install -r requirements.txt

echo "=== 3. .env fayl ==="
if [ ! -f .env ]; then
    cp deploy/.env.example .env
    echo ">>> .env faylni to'ldiring: nano $PROJECT_DIR/.env"
    exit 1
fi

echo "=== 4. Django setup ==="
myenv/bin/python manage.py migrate
myenv/bin/python manage.py collectstatic --noinput

echo "=== 5. Log papka ==="
mkdir -p /var/log/gunicorn
chown www-data:www-data /var/log/gunicorn

echo "=== 6. Gunicorn service ==="
cp deploy/gunicorn.service /etc/systemd/system/gunicorn.service
systemctl daemon-reload
systemctl enable gunicorn
systemctl start gunicorn

echo "=== 7. Nginx sozlash ==="
cp deploy/nginx.conf /etc/nginx/sites-available/online-shop
ln -sf /etc/nginx/sites-available/online-shop /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

echo ""
echo "✓ Deploy tugadi!"
echo "  Server: http://$(curl -s ifconfig.me)"
