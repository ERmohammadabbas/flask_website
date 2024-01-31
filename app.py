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

class Tables(db.Model):
    sn=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),unique=True,nullable=False)
    price=db.Column(db.String(80),unique=True,nullable=False)
    discount=db.Column(db.String(80),unique=True,nullable=False)
    free=db.Column(db.String(80),unique=True,nullable=False)
    percentage=db.Column(db.String(80),unique=True,nullable=False)
    buy=db.Column(db.String(80),unique=True,nullable=False)  

# class Index(db.Model):
#     tag=db.Column(db.String(80),primary_key=True)





@app.route('/abbas',methods=['GET','POST'])
def index():
    # if request.method=='POST' and 'tag' in request.form:
    #     tag = request.form.get('tag')
    #     search="%{}%".format(tag)
    #     tables=Tables.query.filter(Tables.uname.like(search)).products(per_products=products,error_out=False)
    #     return render_template('shop-detail.html',params=params,tag=tag) 
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
    pages=6
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
        # if request.method=='POST' and 'tag' in request.form:
        #     tag = request.form["tag"]
        #     search="%{}%".format(tag)
        #     shop_detail=Shop_detail.query.filter(Shop_detail.uname.like(search)).products(per_products=products,error_out=False)
        #     return render_template('shop-detail.html',params=params,tag=tag) 
        # if request.method=='POST':
        #     tag=request.form['tag']
        #     print(tag)
    return render_template('shop-detail.html',params=params) 

@app.route('/abbas4')
def testimonial():
    return render_template('testimonial.html',params=params) 

@app.route('/abbas5')
def hello():
    return render_template('404.html',params=params) 

@app.route('/abbas6')
def cart():
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

@app.route('/layout',methods=['GET', 'POST'])
def layout(): 
    search_keyword = request.form.get("search_box")
    results =  db.engine.execute("SELECT * FROM post "
                           "WHERE title = search_box ")
    return render_template('layout.html',params=params) 

@app.route('/table',methods=['GET', 'POST'])
def table():
    if(request.method=='POST'):
        sn=request.form.get('sn')
        name=request.form.get('name')
        price=request.form.get('price')
        discount=request.form.get('discount')
        free=request.form.get('free')
        percentage=request.form.get('percentage')
        buy=request.form.get('buy')
        entry=Tables(sn=sn,name=name,price=price,discount=discount,free=free,percentage=percentage,buy=buy)
        db.session.add(entry)
        db.session.commit()
        tables=Tables.query.all()
        return render_template('cart.html',params=params,tables=tables)  
    return render_template('table.html',params=params) 

@app.route('/view')
def view():
    return render_template('view.html',params=params)

@app.route('/delete/<string:sn>',methods=['GET','POST'])
def delete(sn):
    table=Tables.query.filter_by(sn=sn).first()
    db.session.delete(table)
    db.session.commit()
    return redirect('/abbas')


@app.route('/edit/<string:sn>',methods=['GET','POST'])
def edit(sn):
        if request.method=='POST':
            sn=request.form.get('sn')
            name=request.form.get('name')
            price=request.form.get('price')
            discount=request.form.get('discount')
            free=request.form.get('free')
            percentage=request.form.get('percentage')
            buy=request.form.get('buy')
            if sn=='0':
                entry=Tables(sn=sn,name=name,price=price,discount=discount,free=free,percentage=percentage,buy=buy)
                db.session.add(entry)
                db.session.commit()
            else:
                tables=Tables.query.filter_by(sn=sn).first()
                table.name=name
                table.price=price
                table.discount=discount
                table.free=free
                table.percentage=percentage
                table.buy=buy
                return redirect('/abbas/'+sn)
        table=Tables.query.filter_by(sn=sn).first()
        return render_template("edit.html",params=params,tables=tables)

if __name__ == '__main__':
    app.run(debug=True,port=5000)