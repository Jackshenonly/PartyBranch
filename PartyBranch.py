# -*- coding: utf-8 -*-
from __future__ import with_statement
from config import load_config #绝对导入
from sqlite3 import dbapi2 as sqlite3
import MySQLdb

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
import time

 
#初始化环境


app = Flask(__name__)
config = load_config()
app.config.from_object(config)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)



def get_db():
    db = MySQLdb.connect(host=app.config['HOST'],
        user=app.config['USER'],
        passwd=app.config['PASSWD'],
        db=app.config['DB'],
        charset=app.config['CHARSET']
        )
    return db

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
    return render_template('login.html',head = u"信息学院学生支部党员民主测评系统")


@app.route('/download')
def download():
    if session['username']:
        #data is from db
        data = ['jike12A','jackshen','man']
        f = open('./static/各支部成员成绩.xls','wb')
        for x in data:
            f.write(x+"\t")
        f.close()
        return redirect(url_for('static',filename='各支部成员成绩.xls'))
    return redirect(url_for('login'))

@app.route('/add_admin',methods=['GET','POST'])
def add_admin():
    if session['sadmin']:
        no = request.form['no']
        db = get_db()
        db.cursor().execute("update user set admin = 1 where no = %s",[no])
        db.commit()
        flash(u"添加成功!")
        return redirect(url_for('show_admin'))
    return render_template('login.html',error = u"您不是管理员")    

@app.route('/show_admin')
def show_admin():
    if session['sadmin']:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select no,name,nickname from user where admin = 1")
        admins = cursor.fetchall()
        return render_template("show_admin.html",admins = admins,head=u"管理员")
    return render_template('login.html',error = u'您不是管理员!')    


@app.route('/announce_detail/<title>',methods=['GET','POST'])
def announce_detail(title):
    if session['username']:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('select title,author,date,text from announcement where title = %s',[title])
        details = cursor.fetchone()
        return render_template('announce_detail.html',details = details)
    return redirect(url_for('login'))
@app.route('/publish',methods=['GET','POST'])
def publish():
    if session['admin']:
        title = request.form['title']
        author = session['username']
        text = request.form['text']
        date = time.strftime("%Y-%m-%d %H:%M:%S")
        db = get_db()
        db.cursor().execute("insert into announcement(title,author,date,text) values(%s,%s,%s,%s)",[title,author,date,text])
        db.commit()

        return redirect(url_for('announce_lists'))

    return redirect(url_forp('login'))    



@app.route('/publish_edit')
def publish_edit():  
    return render_template('publish_edit.html',head=u'发布公告')




@app.route('/announce_lists',methods=['GET','POST'])
def announce_lists():
    if session['username']:
        db = get_db()  
        cursor = db.cursor()
        cursor.execute("select title,author,date from announcement order by date desc")
        datas = cursor.fetchall() 
        return render_template('announce_lists.html',head=u"公告",datas = datas)
    return redirect(url_for('login'))



@app.route('/personal_modify/<username>',methods=['GET','POST'])
def personal_modify(username):
    if session.get('username'):
        password = request.form['password']
        NickName = request.form['NickName']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("update user set password = %s,nickname = %s where no = %s",[password,NickName,username])
        db.commit()
        flash(u"Modify Successfully!")
        return redirect(url_for('personal_info',username=username))
    return redirect(url_for('login'))

@app.route('/personal_info/<username>',methods=['POST','GET'])
def personal_info(username):
    if session.get("username"):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("select * from user where no = %s",[username])
        info = cursor.fetchone()
        return render_template('personal_info.html',info = info,head=u"个人设置")
    
    return redirect(url_for('login'))    




@app.route('/show_lists/<depart>',methods=['GET','POST'])
def show_lists(depart):
    if session.get("username"):
            session['depart'] = depart
            db = get_db()
            cur = db.cursor()
            cur.execute('select major,name,sex,depart,status,average from communists where depart = %s',[depart])
            lists = cur.fetchall()
            return render_template('show_lists.html', lists=lists,head  = depart)
    return redirect(url_for('login'))

@app.route('/show_departs')
def show_departs():
    if session.get("username"):
        db = get_db()
        cur = db.cursor()
        cur.execute("select distinct depart from communists")
        departs = cur.fetchall()
        return render_template('show_departs.html',departs = departs,head = u"支部列表")
    return redirect(url_for('login'))

@app.route('/add_comments/<cname>', methods=['POST','GET'])
def add_comments(cname):
    if not session['username']:
        return render_template('login.html',error = "Please Log in!")
    if (int(request.form.get('score'))) > 100 or (int(request.form.get('score')))<0:
        return render_template('show_comments.html',cname =cname, error = u'请在0~100之间输入！')
    mytime = time.strftime("%Y-%m-%d %H:%M:%S")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select nickname from user where no = %s",[session['username']])
    nickname = cursor.fetchone()[0]
    cursor.execute('insert into comments (name,nickname,cname,score,date,text) values (%s, %s, %s, %s, %s, %s)',
                [ session['username'], nickname,cname,request.form.get('score'), mytime, request.form.get('text') ])
    cursor.execute('update communists set score=score + %s,count = count +1 where name = %s',
               [request.form.get('score'),  cname  ])
    db.commit()
    cursor.execute('update communists set average = score / count where name = %s',[ cname ])
    db.commit()
    flash(u'您的宝贵意见和建议，我们督促支部成员积极有则改之无则加勉！')
    return redirect(url_for('show_comments',cname= cname ))


@app.route('/show_comments/<cname>')
def show_comments(cname):
    if session['username'] :
        db = get_db()
        cursor = db.cursor()
        cursor.execute('select nickname,score,date,text from comments where cname = %s',[cname])
        comments = cursor.fetchall()
        return render_template('show_comments.html',cname = cname,comments = comments,head = u'党员评价')
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
            cur.execute('select password,admin,sadmin from user where no =%s',[username])
            user = cur.fetchone()

            if  (user) and (password == str(user[0])):
               session["username"] = username

               if int(user[1])==1:
                    session['admin']=True
        
                    if int(user[2])==1:
                        session['sadmin']=True

               flash("Welcome!")
               return redirect(url_for('show_departs'))
            err = "Something Wrong!"
    error = err +"  Please LOG IN!"       
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session['username']=None
    session['admin']=None
    session['sadmin']=None
    flash('LOG OUT')
    return render_template('login.html',head = u"信息学院学生支部民主评议系统")


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
            cur.execute('insert into performance(mm1,mm2,mm3,mm4,mm5) values (%s, %s, %s, %s, %s)',
                [mm1,mm2,mm3,mm4,mm5])
            db.commit()

            return  redirect(url_for('performance'))
    return render_template('login.html')

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',9000)
