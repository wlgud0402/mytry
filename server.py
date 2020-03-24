from flask import Flask
from flask import render_template
from flask import redirect
from flask import make_response
from flask import request
from uuid import uuid1

app = Flask(__name__)
db_board=[]
db_users=[]

#쿠키
@app.route("/")
def register():
    return render_template("register.html")

@app.route("/register_process", methods=['POST'])
def register_process():
    userId = request.form['userId']
    userPw = request.form['userPw']
    uniqueUserId = str(uuid1())

    user = {
		"id": userId,
		"pw": userPw,
		"uniqueUserId": uniqueUserId,
	}
    db_users.append(user)
    response = make_response(redirect("/register_success"))
    response.set_cookie("uniqueUserId", uniqueUserId)
    return response

@app.route("/register_success")
def register_success():
    return render_template("register_success.html")

@app.route("/check")
def check():
    uniqueUserId = request.cookies.get("uniqueUserId")
    if uniqueUserId == None:
        return render_template("re_register.html")
    for i in range(0, len(db_users)):
        if uniqueUserId == db_users[i]["uniqueUserId"]:
            return render_template("check_success.html")
    return "<불법프로그램이 감지되었습니다>"
            
@app.route("/main")
def main():
    return render_template("main.html")

#글쓰기
@app.route("/write")
def write():
    return render_template("write.html")

#board에서 보여줌
@app.route("/board")
def board():
    return render_template(
        "board.html",
        boardList=db_board)

#글 내용을 받아옴
count = 0
@app.route("/post" , methods=['POST'])
def post():
    print("sdfsdf")
    global count
    month = request.form['month']
    date = request.form['date']
    title = request.form['title']
    comment = request.form['comment']

    board = {
        "board_month": month,
        "board_date":date,
        "board_title":title,
        "board_comment":comment,
        "id":count
    }
    db_board.append(board)
    count += 1
    print(board)
    return redirect("/board")

#세부내용이 있는곳으로 보내줌
@app.route("/detail_board", methods=['GET'])
def detail():
    board_id = int(request.args.get("detail"))
    for i in range(0, len(db_board)):
        if board_id == db_board[i]["id"]:
            return render_template("detail.html", detail=db_board[i])

#삭제
@app.route("/delete", methods=['GET'])
def delete():
    delete_num = int(request.args.get("delete_num"))
    for i in range(len(db_board)):
        if delete_num == db_board[i]["id"]:
            db_board.pop(i)
            return redirect("/board")
#수정
@app.route("/edit", methods=['POST', 'GET'])
def edit():
    edit_num = int(request.args.get("edit_num"))
    edit = request.form["edit"]
    for i in range(0, len(db_board)):
        if edit_num == db_board[i]["id"]:
            db_board[i]["board_comment"] = edit
            return redirect("/detail_board?detail=" + str(db_board[i]["id"]))

if __name__ == "__main__":
    app.run(port=3009)