from flask import Flask 
from flask import request
from flask import render_template
from flask import redirect
from flask import session 
from flask.helpers import url_for
from flaskext.mysql import MySQL

app=Flask(__name__, static_folder="public", static_url_path="/")
app.secret_key="jjhome"
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'qaz28331016'
app.config['MYSQL_DATABASE_DB'] = 'website'

mysql = MySQL(app)


mycursor = mysql.connect().cursor()


#使用GET方法，處理路徑/的對應函式
@app.route("/", methods=["GET"])
def home_page():
    if "name_now" in session:
        return render_template("member.html", name=session["name_now"])
    else:
        return render_template("home_page.html")
    
 #使用POST方法，處理路徑/的對應函式
@app.route("/signin", methods=["POST"])
def signin_function():
    account_data=request.form["account"]
    secret_data=request.form["secret"]
    mycursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (account_data, secret_data))
    account_password_situation = mycursor.fetchone()
    if account_password_situation:
        mycursor.execute('SELECT name FROM user  WHERE username = %s AND password = %s', (account_data, secret_data))
        name_right=mycursor.fetchone()
        name_right=''.join(name_right)
        session["name_now"]=name_right
        return render_template("member.html", name=session["name_now"])
    else: 
        message='?message=帳號密碼有誤'
        return redirect(url_for(('fail_function'),message=message))

@app.route("/signup",methods=["POST"])
def register_function():
    new_username_data=request.form["signup_username"]
    new_account_data=request.form["signup_account"]
    new_secret_data=request.form["signup_secret"]
    mycursor.execute('SELECT * FROM user WHERE username = %s', (new_account_data))
    account_ori = mycursor.fetchone()
    if account_ori:
         return render_template("been_signup.html")
    else:
        sql = '''INSERT INTO user (name, username, password) VALUES (%s, %s, %s)'''
        val = (new_username_data, new_account_data, new_secret_data)
        mycursor.execute(sql, val)
        mycursor.connection.commit()
        return render_template("home_page.html")
    
#登出系統並刪去使用者後台資料
@app.route("/signout")
def delete_function():
    session.pop("name_now",None) 
    return render_template("signout.html") 
#會員頁面
@app.route("/member")
def member_function():
    return render_template("member.html")  
#密碼錯誤頁面
@app.route("/error/<message>")
def fail_function(message):
    return render_template("error_inputwrong.html")  


app.run(port=3000)
