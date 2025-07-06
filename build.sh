#!/usr/bin/env bash

# Install dependencies (already done by Render, but can be kept for redundancy)
pip install -r requirements.txt

# Run migrations (optional, you can also do this manually)
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
