from flask import Flask, render_template, request 
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/hello")
# def hi():
#     return "인사드립니다..."

# request이 들어온 웹 페이지는 route에 명시해줘야함
@app.route("/cal", methods=["GET"])
def add_two_number():
    if request.method == "GET":
        num1 = int(request.args["num1"])
        num2 = int(request.args["num2"])
        result = num1 + num2
    return f"{num1} + {num2} = {num1+num2}"

@app.route("/login", methods = ["POST"])
def member_login():
    if request.method == "POST":
        login_id = request.form["login_id"]
        login_pw = request.form["login_pw"]
        
        if login_id == "yhr" and login_pw =="1234":
            return "로그인 성공"
        else:
            return "로그인 실패"
@app.route("/detect_label", methods=["POST"])
def detect_label():
    # 보내 온 파일을 디코딩 -> 해당 정보 -> aws 보낼 수 있음
    # 보내온 파일 자체를 서버에 저장하는 방식 이용
    # 단, flask server에는 html을 로드하는 templates 폴더가 정해진 것처럼 
    # 다른 파일/폴더에 접근 및 저장하는 것도 static 폴더로 정해져 있다

    # 현재 flask server와 같은 경로에 있는 static에 이미지를 저장하자
    if request.method == "POST":
        f = request.files["file"]
        # 파일을 저장할 때, 파일 이름이 암호화가 되어야 한다
        # 관련 암호화 라이브러리 하나 import
        from werkzeug.utils import secure_filename
        f_name = secure_filename(f.filename)
        f_path = "static/" + f_name
        f.save(f_path)

#파이썬의 장점인 모듈화
        from aws import detect_labels_local_file
        result = detect_labels_local_file(f_path)
        r = "<br/>".join(result.split("\n"))

        return r

    return "Hello World !!"

if __name__ =="__main__":
    app.run(host="0.0.0.0")  # app.run이 가장 아래로 와야함. 이 아래 코드는 실행 안됨

# 실행 시 이전 웹 페이지가 뜨는 경우 
# cmd 관리자 권한으로실행 
# 1)포트 번호를 바꿈
# 2)netstat -ano|findstr 5000로 실행중인 5000번대 포트를 찾아서 죽여야함
#  TCP    0.0.0.0:5000           0.0.0.0:0              LISTENING       3028
# 위의 LISTENING뒤 숫자를 n값에 넣고 
# taskkill /pid nnnn /f 코드를 실행


# 공용 ip 발급
# 나의 공유기를 바라볼 수 있도록 (포트포워딩?) - 보안이나 ~

# 상용 서비스 중 하나를 사용하여 보안되어있는 포트포워딩을 해보기
# ngrok http http://localhost:5000     