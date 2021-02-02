from flask import Flask, flash , session
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request
from flask import redirect
from passlib.hash import pbkdf2_sha256

import random
import time






app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bank.sqlite"
db = SQLAlchemy(app)

app.secret_key = '123riseagainst'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    fullname = db.Column(db.String,nullable=False)
    password = db.Column(db.String, nullable=False)
    account_number = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer)
    transactions = db.relationship("Transactions", backref='user', lazy=True)



class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transactions = db.Column(db.String, nullable=False)





#query = User.query.all()
#print(query)
#print(query[1].username)
#query[0].balance
#check_email = User.query.filter_by(email='h@').first()
#if check_email == None:
 #   print('Erik')
#elif check_email != None:
  #  print('something erik')


#def check_check():
 #   if 'user' not in session:
  #      print('not logged in')
   #     return redirect('/')




@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_query = User.query.filter_by(email=request.form['email']).first()     
        if email_query == None:
            print('error')
            return redirect('/')
        elif email_query != None:
            if email_query.password == request.form['password']:
                print('sucess')
                session['user'] = request.form['email']

                return redirect('/home')
            elif email_query.password != request.form['password']:
                print('error')
                
                return redirect('/')
    else:
        return render_template("login.html")



@app.route('/home', methods=['GET', 'POST'])
def home():
    
    if request.method == 'POST':
        pass
    else:
        if 'user' not in session:
            return redirect('/')
        else:
            welcome = session['user']
            get_user = User.query.filter_by(email= session['user']).first()
            print(get_user.transactions)
            localtime = time.asctime( time.localtime(time.time()) )
            
            return render_template("home.html", get_user=get_user, localtime=localtime)




@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if request.method == 'POST':
        pass
    else:
        if 'user' not in session:
            return redirect('/')
        else:
            get_info = User.query.filter_by(email = session['user']).first()
            localtime = time.asctime( time.localtime(time.time()) )

            return render_template("transactions.html", get_info=get_info, localtime=localtime)





@app.route('/sendit', methods=['GET', 'POST'])
def sendit():
    if request.method == 'POST':
       
        #query for user, check that amount is <= amount in account

        #if not enough flash not enough funds redirect back to sendit

        #if enough funds query for other account if found send/adjust balance 
        flash(f' Confirmation #{random.randint(3000,30000000)}...transfer pending if your not broke it will go through....lulz  ')
        
        return redirect('/sendit')
    else:
        if 'user' not in session:
            return redirect('/')
        else:
            localtime = time.asctime( time.localtime(time.time()) )
            
            return render_template("sendit.html", localtime=localtime)






@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        check_email = User.query.filter_by(email=request.form['email']).first()     
        if check_email == None:

            new_user = User(
                username = request.form['username'],
                email = request.form['email'],
                fullname = request.form['fullname'],
                password = request.form['password'],
                account_number = random.randint(300, 3000) * 3131,
                balance = 3000,
                
            )

            

            db.session.add(new_user)
            
            db.session.commit()
            
            return redirect('/')
        else:
            print('email already in use')
            return redirect('/signup')
    else:
        return render_template("signup.html")


@app.route('/logout')
def logout():
    session.pop('user')
    print("well done erased")
    return redirect('/')



if __name__ == '__main__':
    app.run()