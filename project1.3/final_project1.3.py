#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Project 1.3
author: XIAOYU WANG & YUHAO PAN
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, url_for, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "postgresql://xw2419:8555@w4111vm.eastus.cloudapp.azure.com/w4111"

engine = create_engine(DATABASEURI)

userInfo = dict()
usrName = "Guests"

@app.before_request
def before_request():
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def index():
  print request.args
  return render_template("front1.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
  render_template('login.html')
  try: 
    cursor = g.conn.execute("SELECT Usr,Pass FROM Customer")
  except Exception, e:
    pass  
  temp = cursor.fetchall()
  for row in temp:
    userInfo[row[0]] = row[1];
  cursor.close()
  error = None
  global usrName
  if request.method == 'POST':
    username = request.form['username'] 
    if username not in userInfo.keys():
      error = "Sorry, this user name does not exist!"
    elif request.form['password'] != userInfo.get(username): 
      error = "Sorry, incorrect password! Please try again."
    else:
      usrName = username
      return redirect('/front')
  return render_template('login.html', error=error)


@app.route('/front')
def front():
  return render_template("front2.html")


##### part2 search
##search 
@app.route('/searchdestination',  methods=['GET', 'POST'])
def searchdestination():
  error = None
  global usrName
  try:
    cursor = g.conn.execute("SELECT Distinct destination FROM tour_attraction")
  except Exception, e:
    pass
  des_names = []
  for result in cursor:
    des_names.append(result['destination'])
  cursor.close()

##search engine  
  if request.method == 'POST':
    query_des_names = request.form['name']
    if query_des_names not in des_names:
      error = "Invalid destination."
    else:
        return redirect(url_for('tourpackage',dest = query_des_names))
  return render_template("searchdestination.html", usr = usrName, tour_attraction = des_names, error=error)

#package info
@app.route('/tourpackage/<dest>',  methods=['GET', 'POST'])
def tourpackage(dest):
  global usrName
  if usrName == 'Guests':
   return render_template("reject.html")
  rec = g.conn.execute("SELECT * FROM tour_package P, tour_company C, tour_attraction A WHERE P.tcid = C.tcid AND P.tid = A.tid AND A.destination = %s", (dest,))
  tourID = []
  tourPrice = []
  tourRate = []
  comID = []
  comName = []
  comRate = []
  comLoca = []
  comPhone = []
  for res in rec:
    tourID.append(res['tid'])
    tourPrice.append(res['price'])
    tourRate.append(res['prate']) 
    comID.append(res['tcid'])
    comName.append(res['tcname'])
    comRate.append(res['crate'])
    comLoca.append(res['state'])
    comPhone.append(res['phone'])
  rec.close()

  groupName = []
  cap = []
  groupID = []

  for x in tourID:
    rec = g.conn.execute("SELECT * FROM groups G WHERE G.tid = %s", (x,))
    for res in rec: 
      groupName.append(res['gname'])
      cap.append(res['capacity'])
      groupID.append(res['gid'])
    rec.close()

  return render_template("tourpackage.html", tourID = tourID, tourPrice = tourPrice, tourRate=tourRate, comID = comID, comName = comName, comRate = comRate, comLoca = comLoca, comPhone = comPhone, groupName = groupName, capacity = cap, groupID = groupID)



##part 3
##Looking for local tour company

@app.route('/searchlocalcompany',  methods=['GET', 'POST'])
def searchlocalcompany():
  error = None
  global usrName
  try:
    cursor = g.conn.execute("SELECT Distinct state FROM tour_company")
  except Exception, e:
    pass
  state_names = []
  for result in cursor:
    state_names.append(result['state'])
  cursor.close()

  if request.method == 'POST':
    query_state_names = request.form['name']
    if query_state_names not in state_names:
      error = "Invalid Location."
    else:
        return redirect(url_for('localcompany',state = query_state_names))
  return render_template("searchlocalcompany.html", usr = usrName, com_location = state_names, error=error)

@app.route('/localcompany/<state>',  methods=['GET', 'POST'])
def localcompany(state):
  global usrName
  if usrName == 'Guests':
    return render_template("reject.html")
  rec = g.conn.execute("SELECT * FROM tour_company C WHERE C.state = %s", (state,))
  comID = []
  comName = []
  comRate = []
  comLoca = []
  comPhone = []
  for res in rec:
    comID.append(res['tcid'])
    comName.append(res['tcname'])
    comRate.append(res['crate'])
    comLoca.append(res['state'])
    comPhone.append(res['phone'])

  rec.close()
  return render_template("localcompany.html", comID = comID, comName = comName, comRate = comRate, comLoca = comLoca, comPhone = comPhone)


##part 4
##Looking for tour guide
@app.route('/searchtourguide',  methods=['GET', 'POST'])
def searchtourguide():
  error = None
  global usrName
  try:
    cursor = g.conn.execute("SELECT Distinct tlname FROM language_speak")
  except Exception, e:
    pass
  lan_names = []
  for result in cursor:
    lan_names.append(result['tlname'])
  cursor.close()

  if request.method == 'POST':
    query_lan_names = request.form['name']
    if query_lan_names not in lan_names:
      error = "Invalid Languages."
    else:
        return redirect(url_for('tourguide', languages = query_lan_names))
  return render_template("searchtourguide.html", usr = usrName, languages = lan_names, error=error)

@app.route('/tourguide/<languages>',  methods=['GET', 'POST'])
def tourguide(languages):
  global usrName
  if usrName == 'Guests':
   return render_template("reject.html")

  rec = g.conn.execute("SELECT * FROM tour_company C, tour_guide G, language_speak S WHERE S.tgid = G.tgid AND C.tcid = G.tcid AND S.tlname = %s", (languages,))
  guideName = []
  guideID = []
  guideGender = []
  guideRate = []
  guideExp = []
  guideLanguage = []
  comID = []
  comName = []
  comRate = []
  comLoca = []
  comPhone = []

  for res in rec:
    guideName.append(res['tgname'])
    guideID.append(res['tgid'])
    guideGender.append(res['gender'])
    guideRate.append(res['rate'])
    guideExp.append(res['exp'])
    guideLanguage.append(res['tlname'])
    comID.append(res['tcid'])
    comName.append(res['tcname'])
    comRate.append(res['crate'])
    comLoca.append(res['state'])
    comPhone.append(res['phone'])

  rec.close()
  return render_template("tourguide.html", guideName= guideName, guideID= guideID, guideGender= guideGender, guideRate= guideRate, guideExp = guideExp, guideLanguage = guideLanguage, comID = comID, comName = comName, comRate = comRate, comLoca = comLoca, 
                         comPhone = comPhone)


##new member 5
@app.route('/newmember',methods= ['GET','POST'] )
def newmember():
  error = None
  global usrName
  if usrName != 'Guests':
    return redirect('/login')  
  if request.method == 'POST':
    input_cname = request.form['cname']
    input_age = request.form['age']
    input_gender = request.form['gender']
    input_usr = request.form['usr']
    input_pas = request.form['pas']
    
    cursor = g.conn.execute("SELECT C.usr FROM Customer C")
    username = [] 
    for x in cursor:
      username.append(x['usr'])

    if input_usr in username:
     error = "Sorry, user name already exists!"     

    elif input_cname == '' or input_age == '' or input_gender == '' or input_usr == '' or input_pas =='':
      error = "Sorry, input can not be blank!"  
    
    else:
      rec = g.conn.execute('SELECT max(c.cid) from customer C')
      for res in rec:
        cid = res['max']
        cid = int(cid) + 1
     
      g.conn.execute('INSERT INTO customer(cid,cname,age,gender,usr,pass) VALUES (%s, %s, %s, %s, %s, %s)', (str(cid),str(input_cname),input_age,str(input_gender),str(input_usr),str(input_pas)))
      return redirect('/login')
  return render_template("newmember.html", cur_usr = usrName, error = error)

#member profile
@app.route('/memberprofile',methods= ['GET','POST'] )
def memberprofile():
  error = None
  global usrName
  if usrName == 'Guests':
    return render_template("reject.html")
 
  rec = g.conn.execute("SELECT * FROM customer C WHERE C.usr = %s", (usrName,))
  cid = []
  usr = []
  cname = []
  gender = []
  age = []   
  for res in rec:
    cid.append(res['cid'])
    usr.append(res['usr'])
    cname.append(res['cname'])
    gender.append(res['gender'])
    age.append(res['age'])  
  rec.close()
   
  rec3 = g.conn.execute("SELECT * FROM customer C, groups G, joins J WHERE C.cid = J.cid AND J.gid = G.gid AND C.cid = %s", (cid,))
  groupID = []
  groupname = []
  jdate = []
  capacity = []
  tid = []  
  for res3 in rec3:
    groupID.append(res3['gid'])
    groupname.append(res3['gname'])
    jdate.append(res3['jdate'])
    capacity.append(res3['capacity'])
    tid.append(res3['tid'])    
  rec3.close()  
  return render_template("memberprofile.html", cid = cid, usr = usr, cname = cname, gender = gender, age = age,gid = groupID, gname = groupname, jdate = jdate, capacity = capacity, tid = tid)

###### end 6
@app.route('/logout')
def logout():
  global usrName
  usrName = 'Guests'
  return redirect('/')

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using
        python server.py
    Show the help text using
        python server.py --help
    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
