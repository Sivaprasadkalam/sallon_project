import os.path
from msilib.schema import MIME
from flask import *
from email.mime.text import MIMEText
import smtplib
import DBClass
from DBClass import *
import random
import json
import uuid

app = Flask(__name__)
app.secret_key="siva@1506"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif','webp','avif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

@app.route('/')
def urstyle():
    return render_template("urstyle.html")

@app.route('/loginurstyle')
def loginurstyle():
    return render_template("loginurstyle.html")

@app.route('/menhair')
def menhair():
    return render_template("menhair.html")

@app.route('/womenhair')
def womenhair():
    return render_template("womenhair.html")

@app.route('/admin',methods = ["POST","GET"])
def admin():
    if (request.method=="POST"):
        Aname = request.form["Aname"]
        password = request.form["password"]
        if (Aname == "SIVA PRASAD" and password=="Siva@15062002"):
            return render_template("adminmain.html")
    msg = ('Invalid Admin name and password')
    return render_template("admin.html",msg =msg)

@app.route('/register',methods=["POST","GET"])
def registerpage():
    if(request.method=="POST"):
        name = request.form['name']
        email = request.form['email']
        phoneno = request.form['phoneno']
        uname = request.form['uname']
        password = request.form['password']
        sql = ("INSERT INTO project.register(name,email,phoneno,username,password) VALUES ('%s','%s','%s','%s','%s')")%(name,email,phoneno,uname,password)
        DBClass.executeUpdate(sql)
    return render_template("registerpage.html")

@app.route('/customerdetail')
def customerdetail():
        sql = "select * from register"
        data = DBClass.fetchAll(sql)
        return render_template("customerdetail.html",data = data)


@app.route('/login',methods=["POST","GET"])
def login():
    msg=""
    try:
        if(request.method=="POST"):
            uname = request.form['uname']
            password = request.form['password']
            sql = "select * from register where username like '%s' and password like '%s'"%(uname,password)
            conn = getConn()
            cursor = conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            if(data):
                msg = "login success"
                session['uname'] = uname
                session['name'] = data[1]
                session['id'] = data[0]
                return render_template("usermain.html",msg = msg)
            else:
                flash("Login not Success")
                msg = "Invalid username or password"
                return render_template("login.html",msg=msg)
        else:
            return render_template("login.html", msg=msg)
    except Exception as e:
        return render_template("login.html", msg=e)


@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()

    # Redirect to the login page (you can change the URL as needed)
    return redirect(url_for('urstyle'))

@app.route('/forgot')
def forgot():

    return render_template("forgot.html")

@app.route("/changepwd", methods=["POST","GET"])
def changepwd():
    try:
        password = request.form['password']
        email=session['email']
        sql="Update register set password = '%s' where email = '%s'" % (password, email)
        print("Sql : ", sql)
        conn = getConn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        msg="Password Changes Success"
        return render_template("login.html", msg=msg)
    except Exception as e:
        return render_template("login.html",msg=e)

@app.route("/checkotp", methods=["POST", "GET"])
def checkotp():
    try:
        sentotp = request.form['otp']
        savedotp = session['otp']
        email = session['email']
        print("Saved Otp : ", savedotp, " Sent Otp : ", sentotp)
        if (int(sentotp) == int(savedotp)):
            return render_template("passwordchange.html", email=email)
        else:
            return render_template("enterotp.html", email=email, msg='Incorrect OTP')
    except Exception as e:
        return render_template("login.html", msg=e)

@app.route("/checkemail", methods=["POST", "GET"])
def checkemail():
    try:
        email = request.form['email']
        sql = "Select * from  register where email like '%s'" % (email)
        print("Sql : ", sql)
        conn = getConn()
        cursor = conn.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        if (row):
            session['email'] = email
            subject = "OTP to reset the password"
            otp = random.randint(1000, 9999)
            session['otp'] = otp
            body = "Thank you for changing the Password, your OTP is : " + str(otp)
            sender = "sivaprasadstr@gmail.com"
            recipients = [email]
            password = "srurikgbkachxcng"
            send_email(subject, body, sender, recipients, password)
            return render_template("enterotp.html", email=email)
        else:
            flash("Login Not Success")
            msg = 'Invalid EmailId'
            return render_template("forgot.html", msg=msg)
    except Exception as e:
        return render_template("login.html", msg=e)


@app.route('/booking',methods=["POST","GET"])
def booking():
    uname = request.form.get('uname')
    email = request.form.get('email')
    phone = request.form.get('phone')
    gender = request.form.get('Gender*')
    date = request.form.get('date')
    time = request.form.get('time')
    address = request.form.get('address')
    sql = "insert into booking (uname,email,phone,gender,bookingdate,btime,address) values('%s','%s','%s','%s','%s','%s','%s')" % (
    uname, email, phone, gender, date, time, address)
    executeUpdate(sql)
    return render_template("booking.html")


@app.route('/viewbooking')
def viewbooking():
    sql = "select * from booking"
    data = DBClass.fetchAll(sql)
    return render_template("viewbooking.html",data=data)


@app.route('/addproduct',methods = ['POST','GET'])
def addproduct():
    if request.method == 'POST':
        print("request",request)
        if 'file' not in request.files:
            flash('No File Part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            id = str( random.randint(1000,9999))
            filename = "Img" + str(id) + '.jpg'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            pname = request.form['pname']
            ptype = request.form['ptype']
            quantity = request.form['quantity']
            price = request.form['price']
            conn = getConn()
            cursor = conn.cursor()
            sql= "insert into product(productname,producttype,quantity,price,image) values ('%s','%s','%s','%s','%s')"%(pname,ptype,quantity,price,filename)
            print("SQL:",sql)
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            msg= 'Product Add successfully'
            return render_template("addproduct.html",msg = msg)
        else:
            msg='Product not inserted success'
            return render_template("addproduct.html",msg = msg)
    else:
        msg =''
        return render_template('addproduct.html',msg= msg)

@app.route('/viewproduct')
def viewproduct():
    rows = []
    cols = []
    try:
        conn = getConn()
        sql = "select * from product"
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        sql = 'desc product'
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()

        for x in data:
            cols.append(x[0])
    except Exception as e:
        return render_template("viewproduct.html",msg = e)

    return render_template("viewproduct.html",msg = "",rows = rows,cols = cols)

@app.route("/userviewproduct")
def userviewproduct():
        sql = "select * from product"
        data = DBClass.fetchAll(sql)
        return render_template("userviewproduct.html",data = data)

@app.route("/deleteproduct",methods = ["POST","GET"])
def deleteproduct():
    args = request.args
    id = args['id']
    sql = "delete from carttable where productid  =" + str(id)
    print(sql)
    conn = getConn()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    sql = "delete from product where productid =" + str(id)
    print(sql)
    conn = getConn()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    return redirect(url_for("viewproduct"))


@app.route("/addtocart", methods=["POST","GET"])
def addtocart():
    if(request.method=="POST"):
        pid=request.form['pid']
        pname=request.form['pname']
        ptype = request.form['ptype']
        qty = request.form['rqty']
        price = request.form['price']
        total = request.form['total']
        id=session['id']
        sql="Insert into CartTable(ProductId, ProductName, " \
            "ProductType, Quantity, Price, Total, " \
            "registerId) values(%s,'%s','%s',%s,%s,%s,%s)" \
            %(pid, pname, ptype, qty, price, total, id)
        print("Sql : ", sql)
        conn = getConn()
        cursor = conn.cursor()
        cursor.execute(sql)

        conn.commit()
        sql="Update Product set Quantity = Quantity - "+str(qty)+" where ProductId = "+str(pid)
        print("Sql : ", sql)
        conn = getConn()
        cursor = conn.cursor()
        cursor.execute(sql)

        conn.commit()
        cursor.close()
        conn.close()
        msg="Product Added to cart success"
        return redirect(url_for("customerviewcart",msg = msg))
    else:
        msg=''
        return render_template("customerselectproduct.html",msg=msg)

@app.route("/customerselectproduct")
def customerselectproduct():
    args=request.args
    id=args['id']

    sql="select * from product where productid = " +str(id)
    conn = getConn()
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()

    return  render_template("customerselectproduct.html",data=data)

@app.route("/customerviewcart")
def customerviewcart():
    rows=[]
    cols=[]
    try:
        conn = getConn()
        id=session['id']
        name=session['name']

        sql="select * from carttable where registerid  ="+str(id)
        cursor= conn.cursor()
        cursor.execute(sql)
        rows=cursor.fetchall()
        print(sql)


        sql="select * from carttable"
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        print(sql)

        for x in data:
            cols.append(x[0])
    except Exception as e:
        return render_template("customerviewcart.html", msg=e)
    return render_template("customerviewcart.html", msg='', rows=rows,cols=cols,name=name)



if __name__ == '__main__':
    app.run(debug=True)