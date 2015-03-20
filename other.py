from flask import Flask, request, session, g, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
	name = request.args.get('name')
	#like   ?name=jack&password=1212   required request.args.get('name')
	return str(name)+ "welcome!"

@app.route('/login/<name>')
#via      http://12.12.12.12:9000/login/jack
#  the response  is   "jack"
# to use    url_for('login',name='jack')
def login(name):
	return name
if __name__=='__main__':
	app.debug = True
	app.run('0.0.0.0',9000)

