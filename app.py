from flask import Flask,render_template,Response,request,session,redirect,url_for
import sqlite3
import os
from os import urandom
from passlib.hash import argon2


app = Flask(__name__)
app.secret_key = os.urandom(24)
dbname = ['users.db']


def getconn(dbname):
	conn = sqlite3.connect(dbname)
	return conn


@app.route('/')
@app.route('/index')
def index():
	if 'username' in session:
		return render_template("index.html",username=session['username'])
	else:
		return render_template("index.html")


@app.route('/login',methods=['GET', 'POST'])
def login():
	if request.method=="GET":
		if 'username' in session:
			return redirect(url_for("index"))
		else:
			return  render_template("login.html")
	if request.method=="POST":
		name = request.form['name']
		passwd = request.form['pwd']
		conn = getconn(dbname[0])
		cur = conn.cursor()
		cur.execute("""select * from users where emorph='%s'"""%(name));
		row = cur.fetchone()
		if row==None:
			return render_template("login.html",name=name, error="Email or Phone does not exist")
		if row[2]==name:
			if argon2.verify(passwd,row[2]):
				session['username'] = row[0]
				return redirect(url_for("index"))
			else:
				return render_template("login.html",name=name, error="Incorrect password")
		else:
			return render_template("login.html",name=name, error="Email or Phone does not exist")
		conn.close()
		

@app.route('/signup',methods=['GET', 'POST'])
def signup():
	if request.method=="GET":
		return render_template("signup.html")
	if request.method=="POST":
		fname = request.form['firstname']
		lname = request.form['lastname']
		passwd = request.form['pwd']
		emorph = request.form['emailorphone']
		conn = getconn(dbname[0])
		cur = conn.cursor()
		cur.execute("""select * from users where emorph = '%s'"""%(emorph))
		row  = cur.fetchone()
		if row is not None:
			return render_template("signup.html",error="Mail Id or phone number already registered",
				firstname = fname, lastname = lname,emorph= emorph)
		else:
			encpwd = argon2.using(rounds=10000).hash(passwd)
			cur.execute("""insert into users values('%s','%s','%s','%s')"""%(fname,lname,emorph,encpwd))
			session['username'] = fname
			return redirect(url_for("index"))
		conn.commit()
		conn.close()

@app.route('/logout')
def logout():
	session.pop('username',None)
	return redirect(url_for('index'))


if __name__ == '__main__':
 	app.run()