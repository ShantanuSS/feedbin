from flask import Flask,flash,redirect,render_template,request,session,abort
import os
import mysql.connector
app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('homie.html')
        #return "Hello! Again <a href='/logout'> Logout </a>"

@app.route('/login',methods = ['POST'])
def do_login():
    if request.form['password']=='admin' and request.form['username']=='admin':
        session['logged_in'] = True
    else:
        flash("Wrong Password")
    return home()
#    chkuser = str(request.form['username'])
 #   chkpass = str(request.form['password'])
  #  Session = sessionmaker(bind=engine)
   # s = Session()
    #result = query.()
    #if result:
     #   session['logged_in'] = True
   # else:
    #    flash("Wrong Password or Username")
     #   return home()
@app.route('/userHome')
def userHome():
    if session.get('logged_in'):
        return render_template('homie.html')
    else:
        return render_template('quithere.html',error = 'Unauthorized Access')


@app.route("/logout")
def logout():
    session['logged_in']=False
    return home()

@app.route('/showText')
def showText():
    return render_template('addfeed.html')

@app.route('/addText',methods=['POST'])
def addText():
    try:
        
        if session.get('logged_in'):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            db = mysql.connector.connect(user='root', password='', database='')  #type your username if different from 'root' and then type password and name of database you are working on
            cursor = db.cursor(buffered=True)
            cursor.callproc('sp_GetWish',(_title,_description))
            data=cursor.fetchall()
            if len(data) is 0:
                db.commit()
                return redirect('/login')
            else:
                return render_template('quithere.html',error='Something went wrong...Please try again')
        else:
            return render_template('quithere.html',error='Wrong address')
    except Exception as e:
        return render_template('quithere.html', error=str(e))
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    app.secret_key=os.urandom(12)
    app.run()
