#!/bin/bash
set -e

echo "=== Pulling latest changes from GitHub ==="
git pull origin main

echo "=== Activating virtual environment ==="
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "../venv" ]; then
    source ../venv/bin/activate
fi

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Applying database migrations ==="
python manage.py migrate

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Restarting Gunicorn / Web service ==="
if systemctl is-active --quiet gunicorn; then
    sudo systemctl restart gunicorn
elif systemctl is-active --quiet ppai; then
    sudo systemctl restart ppai
fi

echo "=== Deployment Complete ==="
