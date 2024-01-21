from flask import Flask,render_template,request,session,url_for
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

class Cart(db.Model):
    productID =db.Column(db.Integer,primary_key=True)
    userID=db.Column(db.Integer,unique=True,nullable=False)
    quantity=db.Column(db.Integer,unique=True,nullable=False)



@app.route('/abbas',methods=['GET','POST'])
def index():
    productID = request.form.get("productID")
    isInCart = Cart.query.get(productID)
    # userID = session['userID']
    userID = 'userID'
    if isInCart is None:
        c = Cart(userID=userID, productID=productID, quantity="1")
        db.session.add(c)
        db.session.commit()
    else:
        q = Cart.query.filter_by(userID=userID, productID=productID).first()
        oldQ = q.Quantity
        newQuantity = Cart.query.filter_by(userID=userID, productID=productID).update(dict(quantity= oldQ + 1))
        db.session.commit() 
    return render_template('index.html',params=params)

@app.route('/abbas1',methods=['GET','POST'])
def contact():
    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        message=request.form.get('message')
        entry=Contact(name=name,email=email,message=message)
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
        coupon_code = request.form.get('coupon_code')
        prodcts = request.form.get('prodcts')
        name = request.form.get('name')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        total = request.form.get('total')
        entry=Cart(coupon_code=coupon_code,prodcts=prodcts,name=name,price=price,quantity=quantity,total=total)
        db.session.add(entry)
        db.session.commit()
        # subtotal = 96.00
        # shipping_cost = 3.00
        # total = subtotal + shipping_cost
        # return render_template('cart.html',params=params,total=total)
    return render_template('cart.html',params=params) 



if __name__ == '__main__':
    app.run(debug=True,port=5000)