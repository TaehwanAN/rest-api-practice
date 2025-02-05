# #!/bin/sh

# flask db synchronization
flask db upgrade

# run flask app
echo "Starting Flask app..."
exec gunicorn --bind 0.0.0.0:80 "app:create_app()"
