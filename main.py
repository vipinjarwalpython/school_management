from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///s_management.db"

db = SQLAlchemy(app)


class Student_Database(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    sname = db.Column(db.String(255), nullable=False)
    sage = db.Column(db.Integer, nullable=False)
    sphone = db.Column(db.Integer, nullable=False)
    semail = db.Column(db.String(255), nullable=False)
    sstatus = db.Column(db.Boolean, nullable=False)

    def __repr__(self) -> str:
        return f"{self.sid}:{self.sname}:"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        sname = request.form.get("name").upper()
        sage = request.form.get("age")
        sphone = request.form.get("phone")
        semail = request.form.get("email")
        sstatus = request.form.get("status")

        if sstatus == "on":
            sstatus = True
        else:
            sstatus = False

        student = Student_Database(
            sname=sname, sage=sage, sphone=sphone, semail=semail, sstatus=sstatus
        )
        db.session.add(student)
        db.session.commit()
    allstudent = Student_Database.query.all()
    return render_template("home.html", allstudent=allstudent)


@app.route("/update/<int:sid>", methods=["GET", "POST"])
def update_student(sid):
    if request.method == "POST":
        sname = request.form.get("name").upper()
        sage = request.form.get("age")
        sphone = request.form.get("phone")
        semail = request.form.get("email")
        sstatus = request.form.get("status")

        if sstatus == "on":
            sstatus = True
        else:
            sstatus = False

        student = Student_Database.query.filter_by(sid=sid).first()
        student.sname = sname
        student.sage = sage
        student.sphone = sphone
        student.semail = semail
        student.sstatus = sstatus

        db.session.add(student)
        db.session.commit()
        return redirect("/")

    student = Student_Database.query.get(sid)
    return render_template("update.html", student=student)


@app.route("/delete/<int:sid>")
def delete_student(sid):
    student = Student_Database.query.get(sid)

    db.session.delete(student)
    db.session.commit()

    return redirect("/")


@app.route("/about-us")
def about():
    return render_template("aboutus.html")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True, port=8080)
