from flask import Flask,render_template,Response
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def start():
    return render_template("index.html")

@app.route('/login')
def login():
	return  render_template("login.html")

@app.route('/signup')
def signup():
	return render_template("signup.html")

@app.route('/logout')
def logout():
	return "logout"

if __name__ == '__main__':
 	app.run()