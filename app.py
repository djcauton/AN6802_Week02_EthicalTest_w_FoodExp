from flask import Flask, request, render_template
import datetime
import sqlite3
from flask import Markup

app = Flask(__name__)

name_flag = 0
name=""

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

#Action from index.html (post the user input "name")
@app.route("/main",methods=["GET","POST"])
def main():
    global name_flag,name
    if name_flag==0:
        name = request.form.get("name")
        name_flag=1
        conn = sqlite3.connect("log.db") #Connect to log.db (initially created via 'create database.ipynb' which also creates the table employee)
        c = conn.cursor()
        timestamp = datetime.datetime.now()
        c.execute("insert into employee (name,timestamp) values(?,?)",(name,timestamp))
        conn.commit()
        c.close()
        conn.close()
    return(render_template("main.html",name=name))

#Action from main.html
@app.route("/ethical_test",methods=["GET","POST"])
def ethical_test():   
    return(render_template("ethical_test.html"))

#Action from main.html
@app.route("/query",methods=["GET","POST"])
def query():
    conn = sqlite3.connect("log.db")
    c = conn.execute("select * from employee")
    r=""
    for row in c:
        r=r+str(row)+"<br>"
    print(r)
    r = Markup(r)
    c.close()
    conn.close()
    return(render_template("query.html",r=r))

#Action from main.html
@app.route("/delete",methods=["GET","POST"])
def delete():
    conn = sqlite3.connect("log.db")
    c = conn.cursor()
    c.execute("delete from employee;")
    conn.commit()
    c.close()
    conn.close()
    return(render_template("delete.html", name=name))

#Action from main.html
@app.route("/food_exp",methods=["GET","POST"])
def food_exp():
    return(render_template("food_exp.html"))

#Action from main.html
@app.route("/end",methods=["GET","POST"])
def end():  
    return(render_template("end.html"))


#Action from ethical_test.html (post defaulted value from "options" selection (true or false))
@app.route("/answer",methods=["GET","POST"])
def answer():
    ans = request.form["options"]
    print(ans)
    if ans == "true":
        return(render_template("wrong.html"))
    else:
        return(render_template("correct.html"))

#Action from food_expenditure.html (post the user input "income")
@app.route("/prediction",methods=["GET","POST"])
def prediction():
    print("prediction")
    income = float(request.form.get("income"))
    return(render_template("prediction.html", r =(income * 0.48517842)+ 147.47538852)) #output from the regression https://colab.research.google.com/drive/1rwt2FUF5HQYS2En9CBemD8MY8Ny72tQ4#scrollTo=zTVX0BIs25y7


if __name__ == "__main__":
    app.run(port=7171) #Optional parameter port =; used 7171 for fun