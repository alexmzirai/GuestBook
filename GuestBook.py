from flask import Flask, render_template, request

from flask import session

import pymysql

app = Flask(__name__)
app.secret_key = "hgh65h6gh6gh254sbvnhfnmj"


@app.route('/check_in', methods=['GET', 'POST'])  # takes both http methods as arguments
def check_in():
    if 'x' in session:  # check if there is an existing session in 'x' based on username..
        user = session['x']  # retrieve session

        if request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            room = request.form['room']
            mpesa = request.form['mpesa']
            timein = request.form['timein']
            mobile = request.form['mobile']
            email = request.form['email']

            # connecting to host and DB
            con = pymysql.connect('localhost', 'root', '', 'guestbook')  # server, user, password (empty), database name

            # create a cursor object
            cursor = con.cursor()

            sql = "INSERT INTO `users`(`username`, `password`, `password_confirmation`, `access_level`, `user`) VALUES (%s,%s,%s,%s,%s)"

            # put values into a tuple
            data = (fname, lname, room, mpesa, timein, mobile, email, user)

            # append data to sql
            cursor.execute(sql, data)
            con.commit()   # enables commit to save data if it is lost in sudden power loss for example
            return render_template('check_in.html', msg="DETAILS SAVED SUCCESSFULLY")

        else:
            return render_template('check_in.html')

    else:
        return 'You are not logged in!!<a href="/">Login here</a>'


@app.route('/carpark', methods=['GET', 'POST'])
def carpark():
    if request.method == 'POST':
        ownername = request.form['ownername']
        idnumber = request.form['idnumber']
        regnum = request.form['regnum']

        # connecting to host and DB
        con = pymysql.connect('localhost', 'root', '', 'guestbook')  # server, user, password (empty), database name

        # create a cursor object
        cursor = con.cursor()

        sql = "INSERT INTO `cars`(`ownername`, `idnumber`, `regnum`) VALUES (%s, %s, %s)"

        # put values into a tuple
        data = (ownername, idnumber, regnum)

        # append data to sql
        cursor.execute(sql, data)
        con.commit()   # enables commit to save data if it is lost in sudden power loss for example
        return render_template('carpark.html', msg="DETAILS SAVED SUCCESSFULLY")

    else:
        return render_template('carpark.html')


@app.route('/searchbyroom', methods=['GET', 'POST'])
def searchbyroom():
    if request.method == 'POST':
        room = request.form['room']

        if room == '':
            return render_template('searchbyroom.html', msg1='please enter the room number: ')
        con = pymysql.connect('localhost', 'root', '', 'guestbook')
        cursor = con.cursor()

        sql = "SELECT * FROM clients WHERE room = %s AND flag = %s"
        data = room, "yes"
        cursor.execute(sql, data)

        if cursor.rowcount < 1:
            return render_template('searchbyroom.html', error="No Records Found!")

        results = cursor.fetchall()
        return render_template('searchbyroom.html', results=results)
    else:
        return render_template('searchbyroom.html')


@app.route('/checkout/<mobile>', methods=['GET', 'POST'])
def checkout(mobile):
    if 'x' in session:
        user = session['x']  # retrieve session

        if request.method == 'GET':  # remember nobody posted a phone number, so this is a GET method!! when using a variable, use a GET method.
            con = pymysql.connect('localhost', 'root', '', 'guestbook')
            cursor = con.cursor()

            sql = "UPDATE `clients` SET flag = %s WHERE mobile = %s"

            # put this data inside the data variable
            data = "no", mobile

            cursor.execute(sql, data)

            con.commit()

            return render_template('searchbyroom.html', msg='SUCCESSFULLY CHECKED OUT.')


@app.route('/delete', methods=['GET', 'POST'])  # THE DELETE ROUTE
def delete():
    if request.method == 'POST':
        mobile = request.form['mobile']

        if mobile == "":
            return render_template('delete.html', msgdel="Please Enter the Mobile No")

        con = pymysql.connect('localhost', 'root', '', 'guestbook')
        cursor = con.cursor()

        sql = "DELETE FROM clients WHERE mobile = %s  AND flag = %s "
        data = (mobile, "no")	 # when client has checked out and the records to be deleted

        cursor.execute(sql, data)
        con.commit()

        if cursor.rowcount > 0:
            return render_template('delete.html', msgdel="Deleted Successfully!")

        else:
            return render_template('delete.html', msgdel="Deleted Failed!")

    else:
        return render_template('delete.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username == "" or password == "":
            return render_template('login.html', msg1="Empty fields")

        con = pymysql.connect('localhost', 'root', '', 'guestbook')
        cursor = con.cursor()

        sql = "SELECT * FROM users WHERE username = %s  AND password = %s "
        data = (username, password)
        cursor.execute(sql, data)
        # con.commit()(hashed out because we are not committing anything to the DB)

        # check if any field is empty
        if cursor.rowcount == 0:
            return render_template('login.html', msg1="LOGIN FAILED...")

        elif cursor.rowcount == 1:
            results = cursor.fetchall()

            # store username in a session
            session['x'] = username   # *** a person's username is to be used to track the user sessions ****

            return render_template('check_in.html', msg2="Welcome To the Guestbook Application", results=results)

        else:
            return render_template('login.html', msg1="Contact the administrator")

    else:
        return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']

        # connecting to host and database
        con = pymysql.connect('localhost', 'root', '', 'guestbook')  # server, user, password (empty), database name

        # create a cursor object
        cursor = con.cursor()

        sql = "INSERT INTO `users`(`username`, `password`, `password_confirmation`) VALUES (%s,%s,%s)"

        # put values into a tuple
        data = (username, password, password_confirmation)

        # append data to sql
        cursor.execute(sql, data)
        con.commit()   # enables commit to save data if it is lost in sudden power loss for example
        return render_template('check_in.html', msg="USER SUCCESSFULLY REGISTERED.")

    else:
        return render_template('registration.html')


@app.route('/logout')
def logout():
    session.pop('x', None)  # we are killing the session named x
    return render_template('login.html', )


if __name__ == '__main__':
    app.run()
