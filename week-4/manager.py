from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)
app.config["SECRET_KEY"] = "sdlkjg!4654@@@%"


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/signin', methods=['POST', 'GET'])
def signIn():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        if username == "" or password == "":
            return redirect(url_for("error", message="請輸入帳號、密碼"))
        elif username == "test" and password == "test":
            session["login"] = "yes"
            return redirect("member")
        else:
            return redirect(url_for("error", message="帳號、或密碼輸入錯誤"))
    else:
        status = session.get("login")
        if status == "no":
            return redirect("/")


@app.route("/signout")
def signOut():
    session["login"] = "no"
    return redirect("/")


@app.route("/member")
def member():
    status = session.get("login")
    if status == "no":
        return redirect("/")
    return render_template("sucess.html")


@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == '__main__':
    app.run(port=3000)
