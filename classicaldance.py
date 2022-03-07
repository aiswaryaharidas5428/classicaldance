from flask import Flask, render_template, request, session

from dbconnection import Db


app = Flask(__name__)
app.secret_key = "hi"

static_path="C:\\Users\\M G HARIDAS\\PycharmProjects\\classicaldance\\static\\"
@app.route('/hi')
def hello_world():
    return 'Hello World!'



@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_post',methods=['post'])
def login_post():
    username=request.form['textfield']
    password=request.form['textfield2']
    q="select * from login where uname='"+username+"'and password='"+password+"'"
    d=Db()
    res=d.selectOne(q)
    if res !=None:
        session['lid']=res['logid']
        type=res['type']
        if res["type"]=="admin":
            return '''<script>alert('successs');window.location='/adminhome'</script>'''
        elif res["type"]=="user":
            return '''<script>alert('successs');window.location='/usrhome'</script>'''
        else:
            return '''<script>alert('invalid');window.location='/login'</script>'''
    else:
        return '''<script>alert('invalid');window.location='/login'</script>'''


@app.route('/add')
def add():
    return render_template('admin/add.html')

@app.route('/add_post',methods=['post'])
def add_post():
    name=request.form['textfield']
    image=request.files['fileField']
    description=request.form['textarea']

    image.save(static_path+'dance/'+image.filename)
    path="/static/dance/"+image.filename

    db=Db()
    qry="insert into dance(dname,dimage,ddescrip)values('"+name+"','"+path+"','"+description+"')"
    res=db.insert(qry)

    return 'ok'


@app.route('/view_dance')
def view_dance():
    db=Db()
    qry="select * from dance"
    res=db.select(qry)

    return render_template('admin/view.html',data=res)

@app.route('/delete_dance/<id>')
def delete_dance(id):
    db=Db()
    qry="delete from dance where did='"+id+"'"
    res=db.delete(qry)
    return '''<script>alert('deleted');window.location='/view_dance'</script>'''
@app.route('/edit_dance/<id>')
def edit_dance(id):
    db=Db()
    qry="select * from dance where did='"+id+"'"
    res=db.selectOne(qry)
    return render_template('admin/edit_dance.html',data=res)

@app.route('/edit_dance_post',methods=['post'])
def edit_dance_post():
    d_id=request.form['d_id']
    name=request.form['textfield']
    description=request.form['textarea']


    if 'fileField' in request.files:
        dimage = request.files['fileField']
        if dimage.filename!='':
            db=Db()

            dimage.save(static_path + 'dance/' + dimage.filename)
            path = "/static/dance/" + dimage.filename
            qry="update dance set dname='"+name+"',dimage='"+path+"',ddescrip='"+description+"' where did='"+d_id+"'"
            res=db.update(qry)
            return '''<script>alert('updated');window.location='/view_dance'</script>'''
        else:
            db = Db()
            qry = "update dance set dname='" + name + "',ddescrip='" + description + "' where did='" + d_id + "'"
            res = db.update(qry)
            return '''<script>alert('updated');window.location='/view_dance'</script>'''
    else:
         db=Db()
         qry="update dance set dname='"+name+"',ddescrip='"+description+"' where did='"+d_id+"'"
         res=db.update(qry)
         return '''<script>alert('updated');window.location='/view_dance'</script>'''




@app.route('/view_postdance',methods=['post'])
def view_postdance():
    danceview=request.form['textfield']

    db = Db()
    qry = "select * from dance where dname like '%"+danceview+"%'"


    res = db.select(qry)

    return render_template('admin/view.html', data=res)



@app.route('/VIEWUSERS')
def VIEWUSERS():
    db=Db()
    qry="select * from user"
    res = db.select(qry)

    return render_template('admin/VIEWUSERS.html',data=res)

@app.route('/view_postuser',methods=['post'])
def view_postuser():
    userview=request.form['textfield']

    db = Db()
    qry = "select * from user where uname like '%"+userview+"%'"


    res = db.select(qry)

    return render_template('admin/VIEWUSERS.html', data=res)








@app.route('/VIEWUSERS_POST',methods=['post'])
def VIEWUSERS_POST():
    username=request.form['textfield']

    return 'user found'







@app.route('/adminhome')
def adminhome():
    return render_template('admin/adminhome.html')
#
# ----------------------------------USER-----------------------------







@app.route('/change_password')
def change_password():
    return render_template('user/passwdreset.html')
@app.route('/change_password_post',methods=['post'])
def change_password_post():
    cu_pass=request.form['textfield']
    nw_pass=request.form['textfield2']
    re_type=request.form['textfield3']
    db = Db()
    qry = "select * from login where password='"+cu_pass+"'"
    res=db.selectOne(qry)
    if(nw_pass==re_type):
        qry1="update login set password='"+nw_pass+"' where logid='"+str(session['lid'])+"'"
        res2=db.update(qry1)
        return '''<script>alert('password changed');window.location='/login'</script>'''
    else:
        return '''<script>alert('password not changed');window.location='/change_password'</script>'''





@app.route('/userreg')
def userreg():
    return render_template('user/regform.html')
@app.route('/user_reg_post',methods=['post'])
def user_reg_post():
    fname=request.form['textfield']
    dob=request.form['textfield2']
    phone=request.form['textfield4']
    imageup=request.files['fileField2']
    password=request.form['textfield68']
    imageup.save(static_path + 'user/' + imageup.filename)
    path = "/static/user/" + imageup.filename

    emailid = request.form['textfield3']
    db=Db()
    qry="insert into login(uname,password,type)values('"+emailid+"','"+password+"','user')"

    res=db.insert(qry)
    qry2="insert into user(ulogid,uname,udob,uphone,uimage,uemail)values('"+str(res)+"','"+fname+"','"+dob+"','"+phone+"','"+path+"','"+emailid+"')"
    print(qry2)
    res2=db.insert(qry2)
    return render_template('login.html',data=res2)



@app.route('/view_profile')
def view_profile():
    d=Db()
    qry="select * from user where ulogid='"+str(session['lid'])+"'"
    res=d.selectOne(qry)
    return render_template('user/userdetails.html',data=res)


@app.route('/usrhome')
def usrhome():
    return render_template('user/usrhome.html')

if __name__ == '__main__':
    app.run(debug=True)
