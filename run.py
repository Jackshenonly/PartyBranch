# -*- coding: utf-8 -*-
from __future__ import with_statement
from config import load_config #绝对导入
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
import time

 
#初始化环境


app = Flask(__name__)
config = load_config()
app.config.from_object(config)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


#初始化数据库
def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():

    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db
@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()
@app.route('/')
def _index():
    return redirect('login')


@app.route('/show_lists')
def show_lists():
    if session.get("username"):
            db = get_db()
            cur = db.cursor()
            cur.execute('select major,name,sex,depart,status,average from communists')
            lists = cur.fetchall()
            return render_template('show_lists.html', lists=lists)
    return redirect(url_for('/login'))



@app.route('/add_comments/<cname>', methods=['POST'])
def add_comments(cname):
    if not session['username']:
        return render_template('/login',error = "Please Log in!")
    if (int(request.form.get('score'))) > 100 or (int(request.form.get('score')))<0:
        return render_template('show_comments.html',cname =cname, error = u'请在0~100之间输入！')
    mytime = time.strftime("%Y-%m-%d %H:%M:%S")
    db = get_db()
    db.execute('insert into comments (name,cname,score,date,text) values (?, ?, ?, ?, ?)',
                [ session['username'], cname,request.form.get('score'), mytime, request.form.get('text') ])
    db.execute('update communists set score=score + ?,count = count +1 where name = ?',
               [request.form.get('score'),  cname  ])
    db.commit()
    db.execute('update communists set average = score / count where name = ?',[ cname ])
    db.commit()
    flash(u'您的宝贵意见和建议，我们督促支部成员积极有则改之无则加勉！')
    return redirect(url_for('show_comments',cname= cname ))


@app.route('/show_comments/<cname>')
def show_comments(cname):
    if session['username'] :
        db = get_db()
        cur = db.execute('select name,score,date,text from comments where cname = ?',[cname])
        comments = cur.fetchall()
        return render_template('show_comments.html',cname = cname,comments = comments)
    return render_template('login.html',error='Please LOG IN!')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    err = ''
    if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            db = get_db()
            cur = db.cursor()
            cur.execute('select password from user where no =?',[username])
            user = cur.fetchone()
            if  (user) and (password == str(user[0])):
               session["username"] = username
               flash("Welcome!")
               return redirect(url_for('show_lists'))
            err = "Something Wrong!"
    error = err +"  Please LOG IN!"       
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session['username']=None
    flash('LOG OUT')
    return redirect(url_for('login'))


@app.route('/branch_profile')
def branch_profile():
    return render_template('branch_profile.html')

@app.route('/performance',methods=["POST","GET"])
def performance():
    if  session['username']:
        db = get_db()
        cur = db.cursor()
        cur.execute('select avg(mm1),avg(mm2),avg(mm3),avg(mm4),avg(mm5) from performance')
        datas = cur.fetchall()
        
        total = sum(datas[0])
        return render_template('performance.html', datas = datas[0],total = total)
    return render_template('login.html')

@app.route('/add_perf',methods=['POST','GET'])
def add_perf():
    if session['username']:
        if request.method == 'POST':
            mm1 = request.form['mm1']
            mm2 = request.form['mm2']
            mm3 = request.form['mm3']
            mm4 = request.form['mm4']
            mm5 = request.form['mm5']
            db = get_db()
            cur = db.cursor()
            cur.execute('insert into performance(mm1,mm2,mm3,mm4,mm5) values (?, ?, ?, ?, ?)',
                [mm1,mm2,mm3,mm4,mm5])
            db.commit()

            return  redirect(url_for('performance'))
    return render_template('login.html')

if __name__ == '__main__':
    #app.debug = True
    app.run('0.0.0.0',9000)
