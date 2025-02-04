# dev cmd: flask db init, flask db migrate, flask db upgrade, flask db downgrade
## migrate: 변경사항관리
## upgrade, downgrade: 실제 DDL
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()