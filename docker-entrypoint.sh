#!/bin/bash

# Exit on any error
set -e

# Function to wait for database
wait_for_db() {
    echo "Waiting for database..."
    while ! python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sso_project.settings')
django.setup()
from django.db import connection
connection.ensure_connection()
print('Database is ready!')
" 2>/dev/null; do
        echo "Database is unavailable - sleeping"
        sleep 1
    done
}

# Wait for database to be ready
wait_for_db

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Load sample data if in development
if [ "$DEBUG" = "True" ]; then
    echo "Loading sample data..."
    python manage.py loaddata dev_data.json || echo "Sample data not loaded"
fi

# Start the application
echo "Starting SSO application..."
exec "$@"