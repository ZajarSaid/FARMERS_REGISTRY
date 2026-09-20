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
# NOTE: migrations and seed data run in render.yaml's preDeployCommand,
# because the build phase is network-isolated from the Render Postgres.