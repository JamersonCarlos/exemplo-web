from flask import Flask, render_template, request
import sqlite3
import hashlib

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


connect = sqlite3.connect('database.db')
connect.execute(
    'CREATE TABLE IF NOT EXISTS PARTICIPANTS (name TEXT, \
    email TEXT, password TEXT, city TEXT, country TEXT, phone TEXT)')

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        with sqlite3.connect("database.db") as users: 
            cursor = users.cursor()
            cursor.execute("SELECT * FROM PARTICIPANTS WHERE password = (?) and email = (?)", (hashlib.md5(password.encode("utf-8")).hexdigest(), email))
            result = cursor.fetchall()
            
            
            if len(result) != 0: 
                return render_template("participants.html", data=result)
            else: 
                return render_template("login.html")
    else: 
        return render_template('login.html')



@app.route('/join', methods=['GET','POST'])
def join():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = str(hashlib.md5(request.form['password'].encode('utf-8')).hexdigest())
        city = request.form['city']
        country = request.form['country']
        phone = request.form['phone']

        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("INSERT INTO PARTICIPANTS \
            (name,email, password, city,country,phone) VALUES (?,?,?,?,?,?)",
                           (name, email, password, city, country, phone))
            users.commit()
        return render_template("index.html")
    else:
        return render_template('join.html')
    

@app.route('/participants')
def participants():
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM PARTICIPANTS')

    data = cursor.fetchall()
    return render_template("participants.html", data=data)


if __name__ == '__main__':
    app.run(debug=False)
