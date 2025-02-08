from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort



blp = Blueprint("Conn_Test", "conn_test", description="Connection Test")

@blp.route("/conn-test")
class ConnTest(MethodView):
    def get(self):
        # print(request)
        # print(request.headers)
        # print(request.headers["Host"])
        # print("Headers:", request)  # 요청 헤더 출력
        # print("Args:", request.args)  # 쿼리 파라미터 출력
        # print("JSON Body:", request.get_json())  # JSON 요청 본문 출력
        # print("Form Data:", request.form)  # 폼 데이터 출력
        try:
          return {"message": "Check server logs for request details"}, 200
        except Exception as e:
           return {"message": "Error", "error": e.__str__}
