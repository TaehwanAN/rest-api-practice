# #!/bin/sh
# flask db init
# flask db migrate
# flask db upgrade

# exec gunicorn --bind 0.0.0.0:80 "app:create_app(prd=True)"

#!/bin/bash
set -e  # 스크립트 실행 중 오류 발생 시 즉시 종료

echo "Starting Flask application setup..."

# 데이터베이스가 준비될 때까지 대기 (PostgreSQL의 경우)
echo "Waiting for database to be ready..."
while ! nc -z db 5432; do  # 'db'는 데이터베이스 컨테이너의 서비스 이름
  sleep 1
done
echo "Database is ready!"

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
exec gunicorn -w 4 -b 0.0.0.0:80 "app:app"
