from flask import Flask, render_template, request, redirect,session
import os
import mysql.connector

app = Flask(__name__)
app.secret_key = os.urandom(24) # secret key is required to sign session and send it as a cookie to the browser

conn = mysql.connector.connect(host="127.0.0.1", user="NirajBasnet", password="Niraj_009", database="nirajbasnet")
cursor = conn.cursor()

@app.route('/')
def login():
    if "user_id" not in session:
        return render_template('login.html')
    else:
        return redirect('/home')

@app.route("/register")
def about():
        if "user_id" not in session:
            return render_template('register.html')
        else:
         return redirect('/home')

@app.route("/home")
def home():
    if 'user_id' in session:
        print("user_id is already in session")
        return render_template("home.html")
    else:
        return redirect('/')


@app.route("/login_validation", methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    # Use placeholders and pass values as a tuple to prevent SQL injection
    # query = "SELECT * FROM `users` WHERE `email` LIKE {0} AND `password` LIKE {1}".format(f"%{email}%", password)

    # either this 
    # cursor.execute("SELECT * FROM `users` WHERE `email`LIKE %s AND `password` LIKE %s", email, password)  # Use '%' to match any part of the email

    # or this
    query = """SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}' """.format(email, password)
    cursor.execute(query)  # Use '%' to match any part of the email

    users = cursor.fetchall()

    if len(users) > 0:
        session['user_id']=users[0][0]
        print("new session created")
        return redirect('/home')# redirecting to home page
        print(len(users))
    else:
        return redirect('/login')
    

@app.route("/add_user", methods=["POST"])
def add_user():
    regis_name = request.form.get('name')
    regis_email = request.form.get('email')
    regis_password = request.form.get('password')
    cursor.execute("""INSERT INTO `users` (`user_id`,`Name`,`email`,`password`) VALUES(0,'{}','{}','{}')""".format(regis_name, regis_email, regis_password))
    conn.commit()

    cursor.execute("""SELECT * FROM `users` WHERE email LIKE '{}' """.format(regis_email))
    users = cursor.fetchall()
    session['user_id'] = users[0][0]

    return redirect('/home')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
