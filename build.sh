#!/usr/bin/env bash
# Render build script for FARMERS_REGISTRY
# Reference: https://render.com/docs/deploy-django

# Exit immediately on any command failure so the deploy is marked failed.
set -o errexit

# 1. Upgrade pip and install all Python dependencies from requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

# 2. Collect static files into STATIC_ROOT (served by WhiteNoise in production)
python manage.py collectstatic --noinput

# 3. Apply any outstanding database migrations to the PostgreSQL database
python manage.py migrate --noinput

# 4. Seed base data (crops, regions, districts and market prices).
#    Uses get_or_create, so it is safe to run on every deploy.
python manage.py create_data