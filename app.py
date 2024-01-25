from flask import Flask,render_template,request,session,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json

with open('config.json','r') as c:
    params=json.load(c)["params"]

local_server=True

app = Flask(__name__)

app.secret_key="super-secret-key"

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)

mail=Mail(app)

if(local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']
db = SQLAlchemy(app)

class Contact(db.Model):
    name=db.Column(db.String(80),primary_key=True,unique=True,nullable=False)
    email=db.Column(db.String(80),unique=True,nullable=False)
    message=db.Column(db.String(80),unique=True,nullable=False)
    telephone=db.Column(db.String(80),unique=True,nullable=False)
    address=db.Column(db.String(80),unique=True,nullable=False)

class Checkout(db.Model):
    fname=db.Column(db.String(80),primary_key=True,unique=True,nullable=False)
    lname=db.Column(db.String(80),primary_key=True,unique=True,nullable=False)
    email=db.Column(db.String(80),unique=True,nullable=False)
    company=db.Column(db.String(80),unique=True,nullable=False)
    city=db.Column(db.String(80),unique=True,nullable=False)
    text=db.Column(db.String(80),unique=True,nullable=False)
    address=db.Column(db.String(80),unique=True,nullable=False)
    country=db.Column(db.String(80),unique=True,nullable=False)
    postcode=db.Column(db.String(80),unique=True,nullable=False)
    mobile=db.Column(db.String(80),primary_key=True,unique=True,nullable=False)

class Shop_detail(db.Model):
    uname=db.Column(db.String(80),primary_key=True,unique=True,nullable=False)
    email=db.Column(db.String(80),unique=True,nullable=False)
    review=db.Column(db.String(80),unique=True,nullable=False)

class Table(db.Model):
    name=db.Column(db.String(80),primary_key=True,unique=True,nullable=False)
    price=db.Column(db.String(80),unique=True,nullable=False)
    quantity=db.Column(db.String(80),unique=True,nullable=False)
    discount=db.Column(db.String(80),unique=True,nullable=False)
    free=db.Column(db.String(80),unique=True,nullable=False)
    percentage=db.Column(db.String(80),unique=True,nullable=False)
    buy=db.Column(db.String(80),unique=True,nullable=False)  



@app.route('/abbas',methods=['GET','POST'])
def index():
    return render_template('index.html',params=params)
    

@app.route('/abbas1',methods=['GET','POST'])
def contact():
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        message=request.form.get('message')
        address=request.form.get('address')
        telephone=request.form.get('telephone')
        entry=Contact(name=name,email=email,message=message,telephone=telephone,address=address)
        db.session.add(entry)
        db.session.commit()
        mail.send_message(
            'New Message From' + name,
            sender=email,
            recipients=[params['gmail-user']],
            body=message
            )
    return render_template("contact.html",params=params)

@app.route('/abbas7',methods=['GET','POST'])
def chackout():
    if request.method=='POST':
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")   
        company = request.form.get("company")
        city = request.form.get("city")
        country = request.form.get("country")
        postcode = request.form.get("postcode")
        mobile = request.form.get("mobile")
        text = request.form.get("text")
        address = request.form.get("address")
        checkout= Checkout(fname=fname,lname=lname,email=email,text=text,city=city,company=company,address=address,mobile=mobile,postcode=postcode,country=country)
        db.session.add(checkout)
        db.session.commit()
        mail.send_message(
            'New Message From' + fname,
            sender=email,
            recipients=[params['gmail-user']],
            body=text
            )
    return render_template("chackout.html",params=params)  

@app.route('/abbas2')
def shop():
    return render_template('shop.html',params=params) 


@app.route('/abbas3',methods=['GET','POST'])
def shop_detail():
    if(request.method=='POST'):
        uname=request.form.get('uname')
        email=request.form.get('email')
        review=request.form.get('review')
        shop_detail=Shop_detail(uname=uname,email=email,review=review)
        db.session.add(shop_detail)
        db.session.commit()
        mail.send_message(
            'New Message From' + uname,
            sender=email,
            recipients=[params['gmail-user']],
            body=review
            )
        return redirect(url_for('abbas6'))
    return render_template('shop-detail.html',params=params) 

@app.route('/abbas4')
def testimonial():
    return render_template('testimonial.html',params=params) 

@app.route('/abbas5')
def hello():
    return render_template('404.html',params=params) 

@app.route('/abbas6', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        # coupon_code = request.form.get('coupon_code')
        productsname = request.form.get('productsname')
        price = request.form.get('price')
        total = request.form.get('total')
        quantity = request.form.get('quantity')
        entry=Cart(productsname=productsname,price=price,total=total,quantity=quantity)
        cart=Cart.query.all()
        db.session.add(entry)
        db.session.commit()
    return render_template('cart.html',params=params) 


@app.route('/abbas0')
def apple():
    return render_template('apple.html',params=params) 

@app.route('/orange0')
def orange():
    return render_template('orange.html',params=params) 


@app.route('/banana0')
def banana():
    return render_template('banana.html',params=params) 


@app.route('/strawbery0')
def strawbery():
    return render_template('strawbery.html',params=params) 


@app.route('/brocoli0')
def brocoli():
    return render_template('brocoli.html',params=params) 

@app.route('/layout')
def layout():
    return render_template('layout.html',params=params) 

@app.route('/table',methods=['GET', 'POST'])
def table():
    if(request.method=='POST'):
        name=request.form.get('name')
        price=request.form.get('price')
        quantity=request.form.get('quantity')
        discount=request.form.get('discount')
        free=request.form.get('free')
        percentage=request.form.get('percentage')
        buy=request.form.get('buy')
        entry=Table(name=name,price=price,quantity=quantity,discount=discount,free=free,percentage=percentage,buy=buy)
        db.session.add(entry)
        db.session.commit()
    return render_template('table.html',params=params) 

@app.route('/view')
def view():
    return render_template('view.html',params=params)

if __name__ == '__main__':
    app.run(debug=True,port=5000)