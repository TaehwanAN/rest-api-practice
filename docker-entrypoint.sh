# #!/bin/sh
# flask db init
# flask db migrate
# flask db upgrade

# exec gunicorn --bind 0.0.0.0:80 "app:create_app(prd=True)"

#!/bin/bash

# Flask 마이그레이션 설정
if [ ! -d "migrations" ]; then
  echo "Running flask db init (only once)..."
  flask db init
fi

echo "Running flask db migrate and flask db upgrade..."
flask db migrate -m "Auto migration" || true  # 오류가 나도 계속 진행
flask db upgrade

# Flask 애플리케이션 실행
echo "Starting Flask app..."
exec gunicorn --bind 0.0.0.0:80 "app:create_app(prd=True)"
