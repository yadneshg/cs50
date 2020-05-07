from flask import Flask, render_template, request, url_for, redirect, flash
import datetime
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, session
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'd:/cs50/flask/static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



engine = create_engine("postgresql://postgres:Cyber123@localhost:5432/postgres")
db = scoped_session(sessionmaker(bind=engine))
"""
@app.route("/")
def index():
    return render_template("index.html")
"""
@app.route('/')
def hello():
        return render_template('login.html')


@app.route("/showForm")
def showForm():
    # show our html form to the user
    message = "Python and Postgres Registration Application"
    return render_template("register.html", message=message)


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    # check for blanks
    if username == "":
        message = "Please fill in your email address"
        return render_template("register.html", message=message)

    if password == "":
        message = "Please fill in your password"
        return render_template("register.html", message=message)

    db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
               {"username": username, "password": password})

    try:
        db.commit()
    except psycopg2.Error as e:
        message = "Database error: " + e + "/n SQL: " + s
        return render_template("register.html", message=message)

    message = "Your user account has been added. click on Login for logging in."
    return render_template("register.html", message=message)

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    uname = request.form.get("username")
    psd = request.form.get("password")

    result = db.execute("SELECT username, password FROM users where username= :username",
                        {'username': uname}).fetchone()
    if result is not None and result.password == psd:
        message = "None"
        return render_template('index.html', message=message)
    else :
        message="username/password invalid"
        return render_template('login.html', message=message)


@app.route("/logout")
def logout():
    return render_template("login.html")

@app.route("/airlines")
def airlines():
    flights = db.execute("select * from flights").fetchall()
    return render_template("airlines.html", flights=flights)

@app.route("/book", methods=["post"])
def book():
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("response.html", message="invalid Flight Number")
    if db.execute("select * from flights where id = :id", {"id": flight_id}).rowcount == 0:
        return render_template("response.html", message="No such flight")

    db.execute("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id)",
               {"name": name, "flight_id": flight_id})
    try:
        db.commit()
    except psycopg2.Error as e:
        message = "Database error: " + e + "/n SQL: " + s
        return render_template("response.html", message=message)
    message = "successfully Registered!!"
    return render_template("response.html", message=message)

@app.route("/flights")
def flights():
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("flights.html", flights=flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    flight = db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).fetchone()
    if flight is None:
        return render_template("resopnse.html", message="No such flight.")

    passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
                            {"flight_id": flight_id}).fetchall()
    return render_template("flight.html", flight=flight, passengers=passengers)

@app.route("/tshirt")
def tshirt():
    return render_template("tshirt.html")


@app.route("/tshirtsize", methods=["POST"])
def tshirtsize():
    id = request.form.get("member_id")
    size = request.form.get("tshirtsize")
    number = request.form.get("tshirtnumber")
    db.execute("UPDATE members SET t_size = :t_size, t_number = :t_number WHERE id= :id",
               {"t_size": size, "t_number": number,"id":id })
    try:
        db.commit()
    except psycopg2.Error as e:
        message = "Database error: " + e + "/n SQL: " + s
        return render_template("response.html", message=message)
    return render_template("tshirtsize.html", id=id, size=size, number=number)


@app.route("/newyear")
def newyear():
    now = datetime.datetime.now()
    d = now.date
    m = now.month
    y = now.year
    new_year = m == 1 and d == 1
    new_year_date = datetime.datetime(y + 1, 1, 1)
    no_of_days = new_year_date - now
    no_of_days_str = str(no_of_days)
    no_of_days_str1 = ""
    for i in no_of_days_str:
        no_of_days_str1 += i
        if i == ',':
            break

    return render_template("newyear.html", new_year=new_year, no_of_days_str1=no_of_days_str1, now=now)


@app.route("/members")

def members():
    members = db.execute("SELECT * FROM members").fetchall()
    return render_template("members.html", members=members)

@app.route("/memberdetails/<int:member_id>")

def memberdetails(member_id):
    member=db.execute("SELECT * from members where id = :member_id",
                            {"member_id": member_id}).fetchone()
    if member is None:
        return render_template("resopnse.html", message="No Such Member.")

    return render_template("memberdetails.html", member=member)


@app.route("/newmember")
def newmember():
    return render_template("registermember.html")


@app.route("/registermember",methods=["post","GET"])
def registermember():
    fname=request.form.get("memberfname")
    lname=request.form.get("memberlname")
    dob=request.form.get("memberdob")

    db.execute("INSERT INTO members (firstname, lastname, dob) VALUES (:fname, :lname, :dob)",
               {"fname": fname, "lname": lname, "dob": dob})
    try:
        db.commit()
    except psycopg2.Error as e:
        message = "Database error: " + e + "/n SQL: " + s
        return render_template("response.html", message=message)

    member = db.execute("SELECT id from members where firstname = :fname",
                        {"fname": fname}).fetchone()
    if member is None:
        return render_template("resopnse.html", message="No Such Member.")
    mid=member.id
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            ff=f"d:/cs50/flask/static/uploads/{filename}"
            dd=f"D:/cs50/flask/static/uploads/{mid}.jpg"
            os.rename(ff,dd)
    return render_template("registersuccess.html")
