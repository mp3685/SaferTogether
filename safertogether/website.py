# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 01:15:15 2019

@author: mp368
"""

#!/usr/bin/python
import psycopg2
from waitress import serve
from psycopg2 import sql
from flask import Flask, render_template, session, request, url_for, redirect, app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, or_, and_, ForeignKey, Integer, types
from sqlalchemy.orm import mapper, sessionmaker, clear_mappers, relationship
from datetime import datetime
import webbrowser
import hashlib
import sys
import time
from httplib2 import Http
from oauth2client import file, client, tools
from flask_apscheduler import APScheduler
#from flask.ext.socketio import SocketIO

#thread = Thread()
#thread_stop_event = Event()
'''class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()
    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        while not thread_stop_event.isSet():
            number = round(random()*10, 3)
            sleep(self.delay)
    def run(self):
        self.randomNumberGenerator()
'''

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'mydb',
    'host': 'localhost',
    'port': '5432',
}

#engine = SQLAlchemy.create_engine('postgresql+psycopg2://scott:tiger@localhost/mydatabase')
#DATABASE_URI = 'postgres+psycopg2://postgres:1234@localhost:5432/mydb'
#engine = create_engine(DATABASE_URI)
#Session = sessionmaker(bind=engine)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "random string"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres+psycopg2://postgres:1234@localhost:5432/mydb'
db = SQLAlchemy(app)
COUNT = 30
#scheduler = APScheduler()
#scheduler.init_app(app)
#scheduler.start()
#socketio = SocketIO(app)

class Users(db.Model):
    __tablename__ = "users"
    username = db.Column("username", db.String(100), primary_key = True)
    password = db.Column(db.String(200))
    fname = db.Column(db.String(100)) 
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    #img = db.Column(db.LargeBinary)
    
    
    #def __init__(self, username, password, fname,lname, email, phone, description, img):
    def __init__(self, username, password, fname,lname, email, phone, description):
        self.username = username
        self.password = password
        self.fname = fname
        self.lname = lname
        self.email = email
        self.phone = phone
        self.description = description
        #self.img = img
        

    def __repr__(self):
        return '<User %r>' % self.username

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100))
    receiver = db.Column(db.String(100))
    message = db.Column(db.String(1000))
    
    def __init__(self, sender, receiver, message, id):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.id = id
       

    def __repr__(self):
        return '<User %r>' % self.sender
    
class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.String(100), db.ForeignKey(Users.username))
    user2 = db.Column(db.String(100))
    start = db.Column(db.String(500))
    end = db.Column(db.String(500))
    
    join = relationship(Users, primaryjoin=(Users.username==user1))
    
    def __init__(self, user1, user2, start, end, id):
        self.user1 = user1
        self.user2 = user2
        self.start = start
        self.end = end
        self.id = id

    def __repr__(self):
        return '<User %r>' % self.user1

class Trip(db.Model):
    username = db.Column(db.String(100), primary_key = True)
    phone=db.Column(db.String(100))
    email=db.Column(db.String(100))
    mode=db.Column(db.ARRAY(db.String(100))) #list
    start = db.Column(db.String(100))
    end = db.Column(db.String(100))
    id = db.Column(db.Integer, primary_key=True)

    
    def __init__(self, username, phone, email, mode, start, end, id):
        self.username = username
        self.phone = phone
        self.email = email
        self.mode = mode
        self.start = start
        self.end = end
        self.id = id
       

    def __repr__(self):
        return '<User %r>' % self.username
    
    
   
#app.debug = True

'''
class users(db.Models):
    username = db.Column(db.String(100), primary_key = True)
    password = db.Column(db.String(200))
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))

    def __init__(self, usern, passw, fn, ln):
        self.

conn = None
try:
    conn_string = "host='localhost' dbname='mydb' user='postgres' password='1234'"
 
	# print the connection string we will use to connect
    print("Connecting to database\n	->%s" % (conn_string))
 
	# get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # create a cursor
    cur = conn.cursor()
    
 # execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')
 
    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)
   
 # close the communication with the PostgreSQL
    #cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
    exit()
'''

#def users(object):
#    pass

'''def loadSession():
    """"""    
    engine = create_engine(DATABASE_URI, echo=True)
     
    metadata = MetaData(engine)
    db_users = Table('users', metadata, autoload=True)
    mapper(Users, db_users)
     
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
'''


@app.route('/sw.js', methods=['GET'])
def sw():
    return app.send_static_file('sw.js')

@app.route('/manifest.json', methods=['GET'])
def manifest():
    return app.send_static_file('manifest.json')


#Start Screen
@app.route("/")
def index():
    
    return render_template('start.html')

#@socketio.on('connect', namespace='/test')

#Part 1 - Login
@app.route('/login')
def login():
    return render_template('login.html')

#Part 1 - Login AUTH
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    usern = request.form['username']
    passw = request.form['password']

    my_data = request.form

    for key in my_data:
        print('form key '+key+" "+my_data[key], file=sys.stderr)
        print('form key '+key+" "+my_data[key], file=sys.stdout)
        app.logger.warning('testing warning log')
        app.logger.error('testing error log')
        app.logger.info('testing info log')
        
    h = hashlib.md5(passw.encode('utf-8')).hexdigest()

    data = Users.query.filter_by(username=usern, password=h).first()
    
    #cursor = conn.cursor()

    #query = 'SELECT * FROM users WHERE username = %s and password = %s'
    #db.execute(query, (username, h))

    #data = cursor.fetchone()

    #cursor.close()
    #data=None
    if(data):
        session['username'] = usern
        session['myname'] = data.fname

        #return redirect(url_for('home'))
        return render_template('homepage.html', username=session['myname'])

    else:
        error = 'Invalid login credentials'
        return render_template('login.html', error=error)

#Part 1 - Register
@app.route('/register')
def register():
    print('This is error output', file=sys.stderr)
    print('This is standard output', file=sys.stdout)
    return render_template('register.html')

#Part 1 - Register AUTH
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    print('This is error output', file=sys.stderr)
    print('This is standard output', file=sys.stdout)
    usern = request.form['username']
    passw = request.form['password']
    first_name = request.form['first name']
    last_name = request.form['last name']
    email = request.form['email']
    phone = request.form['phone']
    description = request.form['description']
    img=None
    bin_file=None
    try:
        img = request.files['img']
        bin_file = io.StringIO(img.read())
    except:
        img=bin(0)
        bin_file=bin(0)
    my_data = request.form

    for key in my_data:
        print('form key '+key+" "+my_data[key], file=sys.stderr)
        print('form key '+key+" "+my_data[key], file=sys.stdout)
        app.logger.warning('testing warning log')
        app.logger.error('testing error log')
        app.logger.info('testing info log')

    h = hashlib.md5(passw.encode('utf-8')).hexdigest()

    #cursor = conn.cursor()
    
    print('This is error output'+ usern, file=sys.stderr)
    print('This is standard output'+usern, file=sys.stdout)
    
    #query = "SELECT * FROM {0} WHERE username={1};"
    #cursor.execute(sql.SQL(query).format(
    #        sql.Identifier('users'),
    #        sql.Identifier(username)))

    #data = cursor.fetchone()
    
    data = Users.query.filter_by(username=usern).first()

    if(data):
        error = "This user already exists"
        #cursor.close()
        return render_template('register.html', error=error)
    else:
        #ins = 'INSERT INTO users VALUES(%s, %s, %s, %s)'
        #cursor.execute(ins, (username, h, first_name, last_name))

        #conn.commit()
        #cursor.close()
        #return render_template("error.html", error=img)
        #user = Users(usern, h, first_name, last_name, email, phone, description, bin_file)
        user = Users(usern, h, first_name, last_name, email, phone, description)
        db.session.add(user)
        db.session.commit()
        return render_template('login.html')
    
    
def calcMatches():
    data = Trip.query.all()
    lst=[]
    for trip1 in data:
        for trip2 in data:
            data2 = Match.query.filter(or_(Match.user1==session['username'], Match.user2==session['username'])).all()
            if (trip1.start!=trip2.start or trip1.end!=trip2.end):
                continue
            if trip1.username!=trip2.username:
                test=True
                for match in data2:
                    if match.user1==trip1.username and match.user2==trip2.username and match.start==trip1.start and match.end==trip2.end:
                        if trip1.start=='there' and trip2.start=='there' and trip1.end=='there' and trip2.end=='there':
                            lst.append(["CALLED1", test, trip1.username, trip1.start, trip1.end, trip2.username, trip2.start, trip2.end])

                        test=False
                        break
                    if match.user1==trip2.username and match.user2==trip1.username and match.start==trip1.start and match.end==trip2.end:
                        if trip1.start=='there' and trip2.start=='there' and trip1.end=='there' and trip2.end=='there':
                            lst.append(["CALLED2", test, trip1.username, trip1.start, trip1.end, trip2.username, trip2.start, trip2.end])

                        test=False
                        break
                if test:
                    temp = Match(trip1.username, trip2.username, trip1.start, trip1.end, None)
                    app.logger.info(temp.id)
                    db.session.add(temp)
                    db.session.commit()
                    time.sleep(0.1)
            if trip1.start=='there' and trip2.start=='there' and trip1.end=='there' and trip2.end=='there':
                lst.append([test, trip1.username, trip1.start, trip1.end, trip2.username, trip2.start, trip2.end])

    return lst
    
@app.route('/tripAUTH', methods=['GET', 'POST'])
def tripAUTH():
    usern = request.form['entry.843186678']
    email = request.form['entry.1031446364']
    phone = request.form['entry.1245160261']
    mode = request.form.getlist('entry.389858736')
    start = request.form['entry.949029367']
    end = request.form['entry.524814834']
    
    trip=Trip(usern, email, phone, mode, start, end, None)
    app.logger.info(trip.id)
    db.session.add(trip)
    db.session.commit()
        
    calcMatches()
    return render_template('homepage.html', usename=session['myname'])

    #return render_template('work.html', name=data.username, email=data.email, phone=data.phone)
    #return render_template('homepage.html', username=session['myname'])

@app.route('/messages')
def messages():
    '''
    data = Match.query.filter(or_(Match.user1==session['username'], Match.user2==session['username'])).all()
    
    #data = Match.query.filter_by(user1=session['username']).all()
    
    
    SPREADSHEET_ID = "1k1jYzlZI4IiVwI8eLWbc6ptemjCg0Uu4Jw098slY75U"
    RANGE_NAME = "Sheet1"
    
    scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    # Setup the Sheets API
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', scopes)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    gsheet = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = gsheet.get('values', [])[3:]
    values = values[31:]
    total=[]
    for sml in data:
        total.append([sml.user1, sml.user2, sml.start, sml.end])
    count=len(total)
    for trip1 in values:
        if trip1==[]:
            continue
        for trip2 in values:
            if trip2==[]:
                continue
            test=True
            if not (Users.query.filter_by(username=trip1[1]).first() and Users.query.filter_by(username=trip2[1]).first()):
                test = False
                continue
            for match in range(count):
                if trip1[5]==trip2[5] or trip1[6]==trip2[6]:
                    if (total[match][0]==trip1[1] and total[match][1]==trip2[1] and total[match][2]==trip1[5] and total[match][3]==trip1[6]) or (total[match][0]==trip2[1] and total[match][0]==trip1[1] and total[match][2]==trip1[5] and total[match][3]==trip1[6]):
                        test=False
                        continue
            if str(trip1[1])==str(trip2[1]):
                    #return render_template("error.html", error=str(trip1[1])+str(trip2[1]))
                    test=False
                    continue
            if trip1[5]!=trip2[5] or trip1[6]!=trip2[6]:
                    test=False
                    continue
            if test and Users.query.filter_by(username=trip1[1]).first() and Users.query.filter_by(username=trip2[1]).first():
                #return render_template("error.html", error=str(trip1[1])+str(trip2[1]))
                temp = Match(trip1[1], trip2[1], trip1[5], trip1[6], None)
                #temp = Match(trip1[1], trip2[1])
                total.append((trip1[1], trip2[1], trip1[5], trip1[6]))
                count+=1
                app.logger.info(temp.id)
                db.session.add(temp)
                
    db.session.commit()
    
    time.sleep(0.1)
    
    #data = db.session.query(Match).join(Users).filter(Match.user1==session['username']).all()
    '''

    #data = Trip.query.filter_by(username=session['username']).all()
    #count=0
    #for i in data:
    #    count+=1
    #return render_template('error.html', error=str(count))
    '''
    data2 = Match.query.filter(or_(Match.user1==session['username'], Match.user2==session['username'])).all()

    for trip1 in data:
        for trip2 in data:
            if (trip1.start!=trip2.start or trip1.end!=trip2.end):
                continue
            elif trip1.username!=trip2.username:
                test=True
                for match in data2:
                    if match.user1==trip1.username and match.user2==trip2.username:
                        test=False
                        break
                    elif match.user1==trip2.username and match.user2==trip1.username:
                        test=False
                        break
                if test:
                    temp = Match(trip1.username, trip2.username, trip1.start, trip1.end, None)
                    app.logger.info(temp.id)
                    db.session.add(temp)
    db.session.commit()
   ''' 
    er=calcMatches()
    #return render_template('error.html', error="HERE:"+str(er))
    data2 = Match.query.filter(or_(Match.user1==session['username'], Match.user2==session['username'])).all()
    #data2 = Match.query.filter(Match.user1==session['username']).all()
    lst=[]
    for i in data2:
        data3=None
        if i.user1==session['username']:
            data3 = Users.query.filter_by(username=i.user2).first()
        else:
            data3 = Users.query.filter_by(username=i.user1).first()
        lst.append([data3.fname+' '+data3.lname, data3.username, i.start+' to '+i.end, data3.description])
    #err=""
    #if not data:
    #    err="FUCK"
    #else:
    #    err="HUH"
    
    return render_template("messages.html", posts=lst)
    #return render_template("messages.html", posts=data3, error=str(data))

@app.route('/chat1/<string:user2>')
def chat1(user2):
    if user2==None:
        user2=session['otheruser']
    data = Messages.query.filter(or_(and_(Messages.sender==session['username'], Messages.receiver==user2),and_(Messages.sender==user2, Messages.receiver==session['username']))).order_by(Messages.id.asc()).all()
    data2 = Users.query.filter(Users.username==str(user2)).first()
    
    return render_template("chat.html", mess=data2.fname+' '+data2.lname, posts=data, err=user2)

@app.route('/chat')
def chat():
    user2=session['otheruser']
    data = Messages.query.filter(or_(and_(Messages.sender==session['username'], Messages.receiver==user2),and_(Messages.sender==user2, Messages.receiver==session['username']))).order_by(Messages.id.asc()).all()
    data2 = Users.query.filter(Users.username==str(user2)).first()
    
    return render_template("chat.html", mess=data2.fname+' '+data2.lname, posts=data, err=user2)

@app.route('/chatAUTH', methods=['GET', 'POST'])
def chatAUTH():
    mess = request.form['message']
    rec = request.form['rec']
    temp = Messages(session['username'], rec, mess, None)
    app.logger.info(temp.id)
    db.session.add(temp)
    db.session.commit()
    session['otheruser'] = rec
    return redirect(url_for('chat'))

@app.route('/match')
def match():
    data = Users.query.filter_by(username=session['username']).first()
    return render_template('work.html', name=data.username, email=data.email, phone=data.phone)

@app.route('/edit')
def edit():
    #alter table user
    return render_template('edit.html')

@app.route('/editAUTH', methods=['GET', 'POST'])
def editAUTH():
    passw = request.form['password']
    confirm_passw = request.form['confirm password']
    first_name = request.form['first name']
    last_name = request.form['last name']
    email = request.form['email']
    phone = request.form['phone']
    description = request.form['description']
    img = request.files['img']
    bin_file = io.StringIO(img.read())
    
    data = Users.query.filter_by(username=session['username']).first()
    
    if (data and (passw==confirm_passw)):
        if passw:
            h = hashlib.md5(passw.encode('utf-8')).hexdigest()
            data.password = h
        if first_name:
            data.fname = first_name
            session['myname']=first_name
        if last_name:
            data.lname = last_name
        if email:
            data.email = email
        if phone:
            data.phone = phone
        if description:
            data.description = description
        if bin_file:
            data.img = bin_file
        
        db.session.commit()
        
        return render_template('homepage.html', username=session['myname'])
    else:
        error = "The passwords did not match"
        #cursor.close()
        return render_template('edit.html', error=error, username=session['myname'])
    
def matching():
    SPREADSHEET_ID = "1k1jYzlZI4IiVwI8eLWbc6ptemjCg0Uu4Jw098slY75U"
    RANGE_NAME = "Sheet1"
    
    scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    # Setup the Sheets API
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', scopes)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    gsheet = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = gsheet.get('values', [])[3:]
    #values = values[count:]
    if values!=[]:
        usr = Users.query.filter_by(username=session['username']).first()
        #trip = Trip(usr.username, values[count][0], values[count][4], values[count][9], values[count][10])
        #db.session.add(trip)
        #db.session.commit()
        #COUNT+=1
    
    data = Trip.query.filter_by().all()
    
    for user in data:
        usern = user.username
        mode = user.mode
        st = user.start
        e = user.end
        
        #data2 = select query on trip table where start=st and end=e and username != usern .all()
        data2 = Trip.query.filter_by(username != usern, start=st, end=e, mode=mode).all()
        for match in data2:
            #data3 = select query on match where user1 = usern and user2 = match.username
            #or user1 = match.username and user2 = usern
            data3 = Match.query.filter_by(or_(and_(user1=usern, user2=match.username), and_(user1=match.username, user2=usern))).all()
            if not (data3):
                temp = Match(usern, match.username)
                temp2 = Match(match.username, usern)
                db.session.add(temp)
                db.session.add(temp2)
                db.session.commit()
                
    time.sleep(0.1)

@app.route('/homepage')
def homepage():
    return render_template("homepage.html", username = session['myname'])



if __name__ == '__main__':
    #clear_mappers()
    #session = loadSession()
    #res = Users.query.filter_by().all()
    #print("HERE:", res)
    #db.create_all()
    #app.run("localhost", 5006, debug = True, threaded=True)
    app.run("0.0.0.0", threaded=True)
    #serve(app, host="127.127.0.1", port=5003)
    #socketio.run(app)
