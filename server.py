from flask import Flask
from flask import render_template
from flask import redirect
from flask import make_response
from flask import request

app = Flask(__name__)

db_board=[]

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/write")
def write():
    return render_template("write.html")

count = 0
@app.route("/post" , methods=['POST'])
def post():
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
    return render_template(
        "board.html",
        boardList=db_board)

@app.route("/detail_board", methods=['GET'])
def detail():
    board_id = int(request.args.get("detail"))
    for i in range(0, len(db_board)):
        if board_id == db_board[i]["id"]:
            return render_template("detail.html", detail=db_board[i])



if __name__ == "__main__":
    app.run(port=3009)