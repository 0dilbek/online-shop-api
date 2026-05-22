#!/bin/bash
# Kod yangilanganida ishlatish uchun
set -e

PROJECT_DIR=/home/online-shop-api

echo "=== Yangilash boshlandi ==="
cd $PROJECT_DIR

git pull origin main

myenv/bin/pip install -r requirements.txt
myenv/bin/python manage.py migrate
myenv/bin/python manage.py collectstatic --noinput

systemctl restart gunicorn
echo "✓ Yangilash tugadi"
