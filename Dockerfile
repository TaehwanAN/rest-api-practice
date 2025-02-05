# 언어
FROM python:3.10
# 포트
# EXPOSE 5000 # gunicorn -> http 80 port
# 디렉토리:
WORKDIR /app
# 디펜던시
COPY requirements.txt .
# 실행
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# 현재 디렉토리(.) 를 도커 이미지 내 디렉토리(.)로 카피
COPY . .
# --host 0.0.0.0 : 컨테이너 밖에서도 실행될 수 있도록
RUN chmod +x docker-entrypoint.sh

CMD ["/bin/bash","docker-entrypoint.sh"]

# Dokcer Commands
# 터미널 이미지 생성 명령: docker build -t rest-api-flask-python .
## -t : 태그 / rest-api-flask-python: 이미지명 / . : 도커파일 위치
# 터미널 이미지 실행 명령: docker run -p 5005:5000 rest-api-flask-python -> 도커 컨테이너 생성됨
## -p : 포트 / n1:n2 : n1은 외부로부터 입력받을 포트, n2는 실행될 포트 / rest-api-flask-python 이미지 이름
## -d : 터미널 점유 없이 백그라운드에서 실행
## -w : 작업디렉토리(WORKDIR) 임의 설정
## -v : 볼륨 마운트. 호스트와 컨테이너 간 파일시스템(볼륨)을 공유함. <호스트 디렉토리>:<컨테이너 디렉토리>

# docker run -d -p 5001:5000 -w /app -v "$(pwd):/app" rest-api-smorest-python