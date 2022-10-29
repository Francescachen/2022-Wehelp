from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)

app.config["SECRET_KEY"] = "sdlkjg!4654@@@%"


def mysql_conn():
    connection  = mysql.connector.connect(
        host="localhost",
        user="root",
        password="francyh0511",
        database="website", 
    )
    cursor = connection.cursor()
    return connection,cursor

def checktable(sql_commit,table_name):
    connection,cursor = mysql_conn()

    # 判斷資料庫內有沒有已經建立的 member 資料表，若不存在就建立 member 資料表
    cursor.execute(f"select * from information_schema.tables where table_name ='{table_name}'")
    if cursor.fetchall() == []:
        cursor.execute(sql_commit)
    
    cursor.close()
    connection.close()

# 檢查table 
checktable("CREATE TABLE member ( id BIGINT PRIMARY KEY AUTO_INCREMENT, name varchar(255) NOT NULL, username varchar(255) NOT NULL, password varchar(255) NOT NULL)","member")
checktable("CREATE TABLE message ( id BIGINT PRIMARY KEY AUTO_INCREMENT, username varchar(255) NOT NULL, message varchar(255) NOT NULL)","message")

@app.route('/')
@app.route('/login')
@app.route('/login/<message>')
def login(message=""):
    return render_template('login.html',message=message)


@app.route('/signin', methods=['POST'])
def signIn():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    #Create variables for easy access
        username = request.form["username"]
        password = request.form["password"]
        if username == "" or password == "":
            return redirect(url_for("error", message="請輸入帳號、密碼"))
        # Check if account exists using MySQL
        connection,cursor = mysql_conn()
        cursor.execute('SELECT name,username FROM member WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        cursor.close()
        connection.close()
        if account != None:
            session["login"] = "yes"
            session['name'] = account[0]
            session['username'] = account[1]
            return redirect("member")
        else:
            return redirect(url_for("error", message="帳號、或密碼輸入錯誤"))
    else:
        status = session.get("login")
        if status == "no":
            return redirect("/")


@app.route('/signup', methods=['POST'])
def signUp():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'name' in request.form and 'username' in request.form and 'password' in request.form:
    #Create variables for easy access
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        
        connection,cursor = mysql_conn()
        cursor.execute('SELECT * FROM member WHERE name = %s OR username = %s', (name, username,))
        if cursor.fetchall() == []:
            cursor.execute('INSERT INTO member VALUES (NULL, %s, %s, %s)', (name,username, password,))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for("login",message="帳號註冊成功"))
        else:
            cursor.close()
            connection.close()
            return redirect(url_for("error",message="帳號已被註冊"))

@app.route("/signout")
def signOut():
    session["login"] = "no"
    return render_template("logout.html")

@app.route("/member")
def member():
    status = session.get("login")
    if status == "no":
        return redirect("/")
    connection,cursor = mysql_conn()
    cursor.execute("SELECT username,message FROM message")
    datas = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("sucess.html",username=session.get("username"),messageData=datas)

@app.route("/message", methods=['POST'])
def message():
    if request.method == 'POST' and 'message' in request.form:
        connection,cursor = mysql_conn()
        comment = request.form["message"]
        if comment != "":
            cursor.execute("INSERT INTO message VALUES (NULL, %s, %s)", (session.get("username"), comment,))
            connection.commit()
        cursor.execute("SELECT username,message FROM message")
        datas = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("sucess.html",username=session.get("username"),messageData=datas)

@app.route("/error")
@app.route("/error/<message>")
def error(message=None):
    return render_template("error.html",message=message)


if __name__ == '__main__':
    app.run(port=3000)