from urllib import request
from flask import Flask,render_template,request
import pymysql

con=None
cur=None

app=Flask(__name__)

def connectToDb():
    global con,cur
    con=pymysql.connect(host="localhost",user="root",password="",database="student_register")
    cur=con.cursor()
    createQuery="create table if not exists student(sno int primary key auto_increment,name varchar(50),email varchar(50),password varchar(50))"
    cur.execute(createQuery)
    con.commit()

def disconnectDb():
    cur.close()
    con.close()

def insertIntoStudent(name,email,password):
    try:
        connectToDb()
        insertQuery="insert into student (name,email,password) values (%s,%s,%s)"
        values=(name,email,password)
        cur.execute(insertQuery,values)
        con.commit()
        disconnectDb()
        return True
    except:
        disconnectDb()
        return False

def findEmailDuplicate(email):
        try:
            connectToDb()
            findEmailDuplicateQuery="select email from student where email=%s"
            values=(email,)
            cur.execute(findEmailDuplicateQuery,values)
            con.commit()
            data=cur.fetchone()
            disconnectDb()
            if data:
                return True
            else:
                return False
        except:
            disconnectDb()
            return False

    
def findPassword(email,password):
    try:
        connectToDb()
        findPasswordQuery="select password from student where email=%s"
        values=(email,)
        cur.execute(findPasswordQuery,values)
        con.commit()
        data=cur.fetchone()
        disconnectDb()
        print(data)
        if data[0]==password:
            return True
        else:
            return False
    except:
        disconnectDb()
        return False

def insertToTodo(email,title,des):
    try:
        connectToDb()
        createQuery="create table if not exists todo (tsno int primary key auto_increment,temail varchar(50),ttitle varchar(50),tdes varchar(50)"
        cur.execute(createQuery)
        con.commit()
        insertQuery="insert inti todo values(%s,%s,%s)"
        values=(email,title,des)
        cur.execute(insertQuery,values)
        con.commit()
        disconnectDb()
        return True
    except:
        disconnectDb()
        return False





@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sign_up/",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        data=request.form
        if findEmailDuplicate(data["email"]):
            message="Email id already in use"
        else:
            if data["password"]==data["repassword"]:
                if insertIntoStudent(data["name"],data["email"],data["password"]):
                    message="You have signed up successfully. Now login to continue"
                    return render_template("index.html",message=message)
                else:
                    message="Something went wrong"
            elif data["password"]!=data["repassword"]:
                message="Passwords do not match"
        return render_template("signup.html",message=message)
    return render_template("signup.html")



@app.route("/login/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        data=request.form
        if findEmailDuplicate(data["email"]):
            if findPassword(data["email"],data["password"]):
                email=data["email"]
                return render_template("home.html",email=email)
            else:
                message="Incorrect password"
                return render_template("login.html",message=message)
        else:
            message="Incorrect email id"
            return render_template("login.html",message=message)
    return render_template("login.html")


if __name__=="__main__":
    app.run(debug=True)