import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from flask import Flask, flash, redirect, render_template, request, session, abort

engine= create_engine("postgresql://postgres:Cyber123@localhost:5432/postgres")
db=scoped_session(sessionmaker(bind=engine))
def main():
    #flights=db.execute("select origin, destination, duration, name from flights join passengers on passengers.flight_id=flights.id;").fetchall()
    #for flight in flights:
    #    print(f"The flight from {(flight.origin).capitalize()} to {(flight.destination).capitalize()} for {flight.duration} having {(flight.name).capitalize()}.")


    #f=open("flights.csv")
    #reader=csv.reader(f)

    #for origin, destination, duration in reader:
    #    db.execute("insert into flights(origin, destination, duration) values (:origin, :destination, :duration)",
    #    {"origin":origin, "destination":destination, "duration":duration })
    #    print(f"Added flight from {origin} to {destination} for {duration}")
    #    db.commit()
    #flights=db.execute("select id, origin, destination, duration from flights")
    #for flight in flights:
    #    print(f"{flight.id}. {flight.origin} to {flight.destination} for duration {flight.duration} mins.")
    #flight_id=int(input("Flight Id : "))
    #flight=db.execute("select * from flights where id = :id",{"id":flight_id}).fetchone()

    #if flight is None:
    #    print("Error: No Such Flight..")
     #   return
    #print()
    #print("Passengers:")

   # passengers=db.execute("select name from passengers where flight_id = :flight_id",{"flight_id":flight_id}).fetchall()
   # for passenger in passengers:
    #    print(f"{passenger.name}")
    #if len(passengers)==0:
    #    print("No Passengers")

    uname="yad"
    psd="123"
    #uname = request.form.get("username")
    #psd = request.form.get("password")

    result = db.execute("SELECT * FROM users where username=  :username",{'username':uname}).fetchone()
                       # "SELECT * FROM flights WHERE id = :id", {"id": flight_id}
    if result is None :
        print(f"None ")
        #return render_template('login.html')
    elif result.password==psd:
        print(f"elif {result.username}")
        #return render_template('welcome.html')
    else:
        print(f"else {result.username}")
       #return render_template('login.html')


if __name__=="__main__":
    main()
