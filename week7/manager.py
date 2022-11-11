from flask import Flask, render_template, request, redirect, session,url_for, jsonify
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdlkjg!4654@@@%'

def mysql_conn():
    connection  = mysql.connector.connect(
        user='root',
        password='francyh0511',
        host='localhost',
        database='website', 
    )
    cursor = connection.cursor()
    return connection,cursor

def checklogin():
    try:
        if 'login' in session:
            if session.get('login') == 'no':
                return False
            else:
                return True
        if 'name' in session:
            if session.get('name') == None:
                return False
            else:
                return True
        if 'username' in session:
            if session.get('username') == None:
                return False
            else:
                return True
        return False
    except:
        return False

@app.route('/')
@app.route('/login')
@app.route('/login/<message>')
def login(message=''):
    return render_template('login.html',message=message)

@app.route('/signin', methods=['POST', 'GET'])
def signIn():
    # Check if 'username' and 'password' POST requests exist (user submitted form)
    if 'username' in request.form and 'password' in request.form:
    #Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        if username == '' or password == '':
            return redirect(url_for('error', message='請輸入帳號、密碼'))
        # Check if account exists using MySQL
        connection,cursor = mysql_conn()
        cursor.execute('SELECT name,username FROM member WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        cursor.close()
        connection.close()
        if account != None:
            session['login'] = 'yes'
            session['name'] = account[0]
            session['username'] = account[1]
            return redirect('member')
        else:
            return redirect(url_for('error', message='帳號、或密碼輸入錯誤'))
    else:
        if not checklogin():
            return redirect('/')

@app.route('/signup', methods=['POST'])
def signUp():
    #Create variables for easy access
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        
        connection,cursor = mysql_conn()
        cursor.execute('SELECT * FROM member WHERE name = %s OR username = %s', (name, username,))
        if cursor.fetchall() == []:
            cursor.execute('INSERT INTO member VALUES (NULL, %s, %s, %s)', (name,username, password,))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('login',message="帳號註冊成功"))
        else:
            cursor.close()
            connection.close()
            return redirect(url_for('error',message='帳號已被註冊'))

@app.route('/signout')
def signOut():
    session.clear()
    return render_template('logout.html')

@app.route('/member')
def member():
    check = checklogin()
    if not check:
        return redirect(url_for('error',message='您已經登出，請回登入頁重新登入'))
    connection,cursor = mysql_conn()
    cursor.execute('SELECT username,message FROM message')
    datas = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('sucess.html',name=session.get('name'),messageData=datas)

@app.route('/message', methods=['POST'])
def message():
    if 'message' in request.form:
        connection,cursor = mysql_conn()
        comment = request.form['message']
        if comment != '':
            cursor.execute('INSERT INTO message VALUES (NULL, %s, %s)', (session.get('username'), comment,))
            connection.commit()
        cursor.execute('SELECT username,message FROM message')
        datas = cursor.fetchall()
        cursor.close()
        connection.close()
        return redirect('/member')

@app.route('/error')
@app.route('/error/<message>')
def error(message=None):
    return render_template('error.html',message=message)

@app.route('/api/member',methods=["GET"])
def member_search():
    resp_datas = {
        'data':{}
    }
    username = request.values.get('username')
    connection,cursor = mysql_conn()
    cursor.execute('SELECT id,name FROM member WHERE username = %s',(username,))
    datas = cursor.fetchone()

    cursor.close()
    connection.close()
    if datas == None:
        resp_datas['data'] = None
    else:
        resp_datas['data'] = {
            'id':datas[0],
            'name':datas[1],
            'username':username
        }

    return jsonify(resp_datas)  

@app.route('/api/member',methods=['PATCH'])
def member_update():
    if 'Content-Type' in request.headers:
        if request.headers['Content-Type'] != 'application/json':
            resp_datas = {
                'error':True,
            }
        else:
            request_params = request.get_json()
            name = request_params['name']
            username = session.get('username')
            resp_datas = {
                'ok':True
            }
            connection,cursor = mysql_conn()
            cursor.execute('SELECT id FROM member WHERE username = %s',(username,))
            datas = cursor.fetchone()
            if datas == None:
                resp_datas = {
                    'error':True
                }
            else:
                cursor.execute('UPDATE member SET name=%s WHERE id=%s',(name,datas[0],))
                connection.commit()
                resp_datas = {
                    'ok':True
                }
                session['name'] = name
            cursor.close()
            connection.close()
    else:
        resp_datas = {
                "error":True,
            }
    return jsonify(resp_datas)

if __name__ == '__main__':
    app.run(port=3000)