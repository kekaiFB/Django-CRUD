#!/usr/bin/env bash

# Setup script for Django-CRUD project
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Ensure python3 is installed
if ! command -v python3 >/dev/null 2>&1; then
  echo "Installing python3..."
  sudo apt-get update
  sudo apt-get install -y python3
fi

# Ensure pip3 is installed
if ! command -v pip3 >/dev/null 2>&1; then
  echo "Installing pip3..."
  sudo apt-get update
  sudo apt-get install -y python3-pip
fi

# Ensure python3-venv is installed
if ! python3 -m venv --help >/dev/null 2>&1; then
  echo "Installing python3-venv..."
  sudo apt-get update
  sudo apt-get install -y python3-venv
fi

# Create virtual environment if it doesn't exist
if [ ! -d env ]; then
  python3 -m venv env
fi

source env/bin/activate

pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Database setup
DB_NAME="diagnosisDB"
if command -v psql >/dev/null 2>&1; then
  if ! psql -lqt | cut -d '|' -f 1 | grep -qw "$DB_NAME"; then
    echo "Creating database $DB_NAME..."
    createdb "$DB_NAME"
  else
    echo "Database $DB_NAME already exists."
  fi
else
  echo "PostgreSQL not found. Please install PostgreSQL and create database $DB_NAME manually."
fi

# Apply migrations
cd src
python manage.py makemigrations
python manage.py migrate

echo "Setup complete."
echo "Activate the virtual environment with: source env/bin/activate"
echo "Run the development server with: cd src && python manage.py runserver"
