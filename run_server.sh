#!/bin/bash
echo "Starting application..."

# Activate your virtual environment
source ../bin/activate

# Run Django server
python manage.py runserver 0.0.0.0:8000