import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, render_template, request, session
from tensorflow.python.keras.models import load_model

from dbconnection import Db


app = Flask(__name__)
app.secret_key = "hi"

static_path="C:\\Final\\classicaldance\\classicaldance\\static\\"

@app.route('/hi')
def hello_world():
    return 'Hello World!'




@app.route('/')
def launching():
    return render_template('launching_index.html')

@app.route('/user_ind')
def user_ind():
    return render_template('user/usrhome.html')




@app.route('/login')
def login():
    return render_template('index.html')


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
            return '''<script>alert('successs');window.location='/user_ind'</script>'''
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

    return "<script>alert('successfully added');window.location='/add'</script>"


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





@app.route('/admin_change_password')
def admin_change_password():
    return render_template('admin/user_change_password.html')

@app.route('/admin_change_password_post',methods=['post'])
def admin_change_password_post():
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

@app.route('/admintemp')
def admintemp():
    return render_template('admin/index.html')





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
    # print(qry2)
    res2=db.insert(qry2)

    return render_template('index.html',data=res2)





@app.route('/view_profile')
def view_profile():
    d=Db()
    qry="select * from user where ulogid='"+str(session['lid'])+"'"
    res=d.selectOne(qry)
    return render_template('user/userdetails.html',data=res)


@app.route('/usrhome')
def usrhome():
    return render_template('user/usrhome.html')

@app.route('/upload')
def upload():
    return render_template('user/upload.html')



@app.route("/uploadpostnew",methods=['post'])
def a():
    human_string=""
    import tensorflow as tf
    import sys
    import os
    import cv2
    files = request.files["fileField"]
    files.save("C:\\Final\\classicaldance\\classicaldance\\static\\2.jpg")
    # Disable tensorflow compilation warnings
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    import tensorflow as tf
    # image_path = sys.argv[1]
    # image_path="C:\\Users\\ELCOT-Lenovo\\Documents\\images\\sign_dataset\\test\\A\\color_0_0016"
    # Read the image_data
    image_data = tf.gfile.FastGFile(r"C:\\Final\\classicaldance\\classicaldance\\static\\2.jpg",'rb').read()
    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("C:\\Final\\classicaldance\\classicaldance\\logs\\output_labels.txt")]

    with tf.gfile.FastGFile("C:\\Final\\classicaldance\\classicaldance\\logs\\output_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                               {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            # print('%s (score = %.5f)' % (human_string, score))
            break



    db=Db()
    qry="select * from dance where dname='"+human_string+"'"
    # print(qry)
    res=db.selectOne(qry)
    if res is  None:
        return render_template('user/upload.html',status="no", res="Other")
    else:
        return render_template("user/upload.html",status='ok',res="A",dname=res['dname'],dimage=res['dimage'],ddescrip=res['ddescrip'])



@app.route("/uploadpost",methods=['post'])
def uploadpost():
    import cv2
    files= request.files["fileField"]
    files.save("C:\\Final\\classicaldance\\classicaldance\\static\\2.jpg")

    import numpy as np
    # import pandas as pd
    # import matplotlib.pyplot as plt
    # import seaborn as sns
    # import tensorflow as tf
    # from tensorflow import keras
    # import os
    # import random
    # from shutil import copyfile
    #
    # from tensorflow.keras import layers, models, optimizers, callbacks, Sequential
    #
    # from tensorflow.keras.layers import Flatten, Dense, BatchNormalization, Activation, Dropout, Conv2D, \
    #     GlobalAveragePooling2D
    from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input, InceptionResNetV2
    #
    # import cv2
    # # from tensorflow_core.python.keras.models import load_model
    #
    # lrs = [0.0001, 0.00001]
    # batch_sizes = [40, 50, 64]
    # freeze_layers = [10, 20, 30, 40, 50]

    # lr = lrs[0]
    #
    # base_model = InceptionResNetV2(include_top=False, weights='imagenet',
    #                                pooling='avg', input_shape=(256, 256, 3))
    # #
    # model = Sequential()
    # model.add(base_model)
    # model.add(Flatten())
    # model.add(Dense(1024, activation=('relu'), input_dim=512))
    # model.add(Dense(512, activation=('relu')))
    # model.add(Dropout(.3))
    # model.add(Dense(256, activation=('relu')))
    # model.add(Dropout(.3))
    # model.add(Dense(128, activation=('relu')))
    # model.add(Dropout(.2))
    # model.add(Dense(8, activation=('softmax')))
    #
    # model.compile(loss="categorical_crossentropy",
    #               optimizer=optimizers.Adam(lr=lr),
    #               metrics=['accuracy'])

    # from  tensorflow.keras.models import  load_model
    model = load_model('C:\\Final\\classicaldance\\classicaldance\\a.h5')

    image = cv2.resize(cv2.imread("C:\\Final\\classicaldance\\classicaldance\\static\\2.jpg"),(256, 256))
    image = preprocess_input(image)
    k = []
    image = np.expand_dims(image, axis=0)
    k.append(image)
    import numpy as np
    aaa = model.predict(image)

    danceform = ["bharatanatyam", "kathak", "kathakali", "kuchipudi", "manipuri", "mohiniyattam", "odissi", "sattriya"]
    a = np.argmax(aaa)

    # print("final result", danceform[a])

    return render_template('user/upload.html',res= danceform[a])

@app.route('/forget')
def forget():
    return render_template('forgetpass.html')

@app.route('/forgetpass_post',methods=['post'])
def forgetpass_post():


    emailid = request.form['textfield']
    db=Db()
    qry="select * from login where uname='"+emailid+"'"
    r=db.select(qry)
    if r is not None:

        import  random

        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("aiswaryaharidas5428@gmail.com", "Aiswarya@5428")
        msg = MIMEMultipart()  # create a message.........."
        message = "Messege from password change request"
        msg['From'] = "aiswaryaharidas5428@gmail.com"
        msg['To'] = emailid
        msg['Subject'] = "Your Password for classicaldance"

        k= str(random.randint(10000,1000000))
        body = "Your new password is : " +k
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)

        db=Db()
        db.update("update login set password='"+k+"' where uname='"+emailid+"' ")
        return "<script>alert('Password changed successfully');window.location='/'</script>"
    else:
        return "<script>alert('Invalid email');window.location='/'</script>"






@app.route("/temp")
def temp():
    return render_template("tables.html")





if __name__ == '__main__':
    app.run(debug=True,threaded=False)
