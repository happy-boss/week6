from flask import Flask,request,render_template,redirect,session,url_for
import mysql.connector

app=Flask(
    __name__,static_folder="public",static_url_path="/")   

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="2021",
    database="mydatabase",
    buffered = True
    #Buffered游标适用于多个小结果集的查询,且多个结果集之间的数据需要一起使用。
#使用buffered游标执行查询语句时 ,取行方法（如fetchone()，fechcall()等）返回的是缓冲区中的行。nonbuffered游标不从服务器获取数据,直到调用了某个获取数据行的方法, 在使用nonbuffered游标时,必须确保取出的结果是结果集中的所有行，才能再用同一连接执行其他语句,否则会报错InternalError(Unread result found)。
)

mycursor = mydb.cursor()



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup",methods=["POST"])
def signup():
    username=request.form['username']
    mycursor.execute("SELECT  username FROM user where username='%s'"% (username))
    user=mycursor.fetchone()
    #試試user==username可不可以，發現問題點在於資料型態根本不同
    #印出"test"跟test要再去處理東西才是正確的
    if user!=None:
        return redirect("/error?message=帳號重複註冊")
    else:
        sql = "INSERT INTO user (name, username,password) VALUES (%s, %s,%s)"
        val = (request.form['name'],request.form['username'], request.form['password'])
        mycursor.execute(sql,val)
        mydb.commit()
        return redirect("/")  

@app.route("/signin",methods=["POST"])
def signin():
    username=request.form['username']
    password=request.form['password']
    mycursor.execute("SELECT username,password FROM user where username='%s'and password='%s'"% (username,password))
    checkuser = mycursor.fetchone()
    if checkuser!=None:
        session['username'] = request.form['username']
        return redirect("/member")              
    else:

        return redirect("/error?message=帳號或密碼錯誤")

@app.route("/signout")
def signout():
    session.pop('username', None)
    return redirect("/")

@app.route("/member")
def member():
    mycursor.execute("SELECT name FROM user where username='%s'"%(session['username']))
    name = mycursor.fetchone()
    name=name[0]
    #我在登入頁面時，第一次想錯，根本沒有從前端取得資料
    #是從session中的資料取得再來用資料庫寫入難算取得
    #但應出來是有逗號 要用陣列的觀念去想
    #第一次多此一舉再創一個陣列去執行 後面發現這根本就是一個陣列 直接name[0]就可以
    if username in session:
        return render_template("member.html",name=name)
    else:
        return redirect("/")

@app.route("/error")
def error():
    message= request.args.get('message')
    print(message)
    return render_template("error.html",message=message)
app.run(port=3000)    
