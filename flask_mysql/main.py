# %%
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'shopdb'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)

class User():
    def login_check(username, password):
        # MySQL DB에 해당 계정 정보가 있는지 확인
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # 값이 유무 확인 결과값 account 변수로 넣기
        account = cursor.fetchone()
        return account
    def get_information(id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', id)
        account = cursor.fetchone()
        return account
    def check_username_exist(username):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"SELECT * FROM accounts WHERE username = '{username}'")
        account = cursor.fetchone()
        return account
    def check_email_exist(email):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"SELECT * FROM accounts WHERE email = '{email}'")
        account = cursor.fetchone()
        return account
    def useradd(username, password, email):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = f"INSERT INTO accounts  VALUES (NULL,'{username}', '{password}', '{email}')"
        cursor.execute(sql)
        mysql.connection.commit()
        account = cursor.fetchone()
        # cursor.close()
        return account
    def check_all_userinfo():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"SELECT * FROM accounts")
        data = cursor.fetchall()
        return data

# %%
@app.route("/")
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        # return render_template('home.html')
        return render_template('home.html', username=session['username'], email=session['email'])
    # User is not loggedin redirect to login page
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    # username과 password에 입력값이 있을 경우
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # 쉬운 checking을 위해 변수에 값 넣기
        username = request.form['username']
        password = request.form['password']
        account = User.login_check(username, password)
        # 정상적으로 유저가 있으면 새로운 세션 만들고, 없으면 로그인 실패 문구 출력하며 index 리다이렉트
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['email'] = account['email']
            #return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = 'Creating User Page'
    # If already loggedin, redirect to home
    if 'loggedin' in session:
        return redirect(url_for('home'))
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        print(username, password, email)
        username_already_exist = User.check_username_exist(username)
        email_already_exist = User.check_email_exist(email)
        if username_already_exist:
            msg = 'That username is already exist'
        elif email_already_exist:
            msg = 'That email is already exist'
        else:
            User.useradd(username, password, email)
            msg = 'Create User Success!'
            return redirect(url_for('login'))
    return render_template('register.html', msg=msg)

@app.route("/member_list")
def member_list():
    msg = User.check_all_userinfo()
    return render_template('member_list.html', msg=msg)


