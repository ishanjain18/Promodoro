

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
import random
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "3d6f45a5fc12445dbaae552853j34h50342"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)



import psycopg2
try:
    connection = psycopg2.connect(user = "iwaidnjbhtfzfe",
                                  password = "f6b90eafd51e0ec65b1aea2c121d953e8c3f5dd41c2ca30d79f9c7cc5f62e926",
                                  host = "ec2-34-225-162-157.compute-1.amazonaws.com",
                                  port = "5432",
                                  database = "dg5kliec8asc5")




    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

Session(app)

db = SQL("postgres://iwaidnjbhtfzfe:f6b90eafd51e0ec65b1aea2c121d953e8c3f5dd41c2ca30d79f9c7cc5f62e926@ec2-34-225-162-157.compute-1.amazonaws.com:5432/dg5kliec8asc5")

@app.route("/")
def index():
    '''Show MainPage'''
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    '''log-in page'''
    #forget any user id
    session.clear()

    if request.method == "POST": # request recieved by submitting the login form

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/taskpage")

    else: # route reached via link, address bar or redirect
        return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():
    ''' register page '''
    session.clear()

    if request.method == "POST":

         # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",username=request.form.get("username"))

        # Ensure username is available
        if len(rows) == 1:
            return apology("Username Already Taken, Please try again")

        # Password authentication
        if not request.form.get("password"):
            return apology("must enter password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match.", 400)

        hsh = generate_password_hash(request.form.get("password"))
        r = random.randint(0, 1248234345734)

        b = db.execute("INSERT INTO users(id, username, hash) VALUES (:id1, :username, :hasher);", id1=r, username=request.form.get("username"), hasher=hsh)





        try:


           connection = psycopg2.connect(user = "iwaidnjbhtfzfe",
                                  password = "f6b90eafd51e0ec65b1aea2c121d953e8c3f5dd41c2ca30d79f9c7cc5f62e926",
                                  host = "ec2-34-225-162-157.compute-1.amazonaws.com",
                                  port = "5432",
                                  database = "dg5kliec8asc5")

           cursor = connection.cursor()

           postgres_insert_query = """ INSERT INTO users (id, username, hash) VALUES (%s,%s,%s)"""
           record_to_insert = (r, request.form.get("username"), hsh)
           cursor.execute(postgres_insert_query, record_to_insert)

           connection.commit()
           count = cursor.rowcount
           print (count, "Record inserted successfully into users table")

        except (Exception, psycopg2.Error) as error :
            if(connection):
                print("Failed to insert record into users table", error)

        finally:
            #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

















        a = db.execute("SELECT * FROM users;")
        print(a)

        # Redirect user to login page
        return redirect("/login")


    else:
        return render_template("register.html")



@app.route("/taskpage")
@login_required
def taskpage():


    """define tasks as a select query from the tasks table
        containing the tasks in a list format"""
    tasks=[]
    foo = db.execute("SELECT * FROM tasks WHERE username = :username", username=session["username"])
    for i in foo:
        tasks.append(i["task"])

    count = len(tasks)
    session["taskcount"] = count
    session["tasks"] = tasks

    tasks = enumerate(tasks)


    return render_template("taskpage.html", tasks=tasks, count=count)

@app.route("/add", methods=["GET","POST"])
@login_required
def add():

        task = request.form.get("task")
        if not task:
            return apology("Enter a Task")
        #db.execute("INSERT INTO tasks(username, task) VALUES (:username, :task);", username=session["username"], task=task)

        else:
            try:


               connection = psycopg2.connect(user = "iwaidnjbhtfzfe",
                                  password = "f6b90eafd51e0ec65b1aea2c121d953e8c3f5dd41c2ca30d79f9c7cc5f62e926",
                                  host = "ec2-34-225-162-157.compute-1.amazonaws.com",
                                  port = "5432",
                                  database = "dg5kliec8asc5")

               cursor = connection.cursor()

               postgres_insert_query = """ INSERT INTO tasks (username, task) VALUES (%s,%s)"""
               record_to_insert = (session["username"], task)
               cursor.execute(postgres_insert_query, record_to_insert)

               connection.commit()
               count = cursor.rowcount
               print (count, "Record inserted successfully into tasks table")

            except (Exception, psycopg2.Error) as error :
                if(connection):
                    print("Failed to insert record into tasks table", error)

            finally:
                #closing database connection.
                if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")

        return redirect("/taskpage")

@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():


        for i in range(session["taskcount"]):

            foo = "check"+str(i)
            #bar = "removed"+str(i)
            if request.form.get(foo):
                try:


                   connection = psycopg2.connect(user = "iwaidnjbhtfzfe",
                                  password = "f6b90eafd51e0ec65b1aea2c121d953e8c3f5dd41c2ca30d79f9c7cc5f62e926",
                                  host = "ec2-34-225-162-157.compute-1.amazonaws.com",
                                  port = "5432",
                                  database = "dg5kliec8asc5")

                   cursor = connection.cursor()

                   postgres_delete_query = """ DELETE FROM tasks WHERE task=%s;"""

                   cursor.execute(postgres_delete_query, (session["tasks"][i],))

                   connection.commit()
                   count = cursor.rowcount
                   print (count, "Record inserted successfully into tasks table")

                except (Exception, psycopg2.Error) as error :
                    if(connection):
                        print("Failed to insert record into tasks table", error)

                finally:
                    #closing database connection.
                    if(connection):
                        cursor.close()
                        connection.close()
                        print("PostgreSQL connection is closed")

                #db.execute("DELETE FROM tasks WHERE task=:task;", task=session["tasks"][i])

        return redirect("/taskpage")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


if __name__ == '__main__':
 app.debug = True
 port = int(os.environ.get("PORT", 5000))
 app.run(host='0.0.0.0', port=port)