from enum import unique
from itertools import permutations
import re
from flask import Flask, render_template, session, request, flash
#from werkzeug.wrappers import request
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import camel_to_snake_case
from sqlalchemy.orm import backref, query
from sqlalchemy.sql.schema import ForeignKey
from werkzeug.utils import redirect, secure_filename
import os
from flask_mail import Mail, Message
from flask_paginate import Pagination, get_page_parameter
import uuid
from datetime import date, timedelta
from sqlalchemy.sql import func



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost/nibo"
#app.config['SQLALCHEMY_DATABASE_URI'] = 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'mkv', 'mpg', 'mov'])
app.config['POSTER_UPLOAD'] = "static\\products"

app.config['MAIL_USERNAME'] = "watchwhistle@gmail.com"
app.config['MAIL_PASSWORD'] = "aamir0007"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



db = SQLAlchemy(app)

class Product(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    productid = db.Column(db.String, unique=True, nullable=False)
    productname = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    subcategory = db.Column(db.String(30), nullable=False)
    colour = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    top = db.Column(db.String(10), nullable=True)
    picture1 = db.Column(db.String(300), nullable=True)
    picture2 = db.Column(db.String(300), nullable=True)
    picture3 = db.Column(db.String(300), nullable=True)
    picture4 = db.Column(db.String(300), nullable=True)
    prod = db.relationship('Cart', backref='prod')

    def _repr_(self) -> str:
      return f"{self.productid} - {self.productname} - {self.category} - {self.subcategory} - {self.colour} - {self.quantity} - {self.price} - {self.picture1} - {self.picture2} - {self.picture3} - {self.picture4}"

class Users(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customerid = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(200), nullable=False)
    address = db.Column(db.Integer, nullable=False)
    password = db.Column(db.Integer, nullable=False)
    

    def _repr_(self) -> str:
      return f"{self.sno} - {self.name} - {self.category} - {self.firstname} - {self.lastname} - {self.email} - {self.phone} - {self.address} - {self.password}"

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.String(30), ForeignKey('product.productid'), nullable=False)
    product_name = db.Column(db.String(30), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.String(30), ForeignKey('users.customerid'), nullable=False)
    customer_name = db.Column(db.String(30), nullable=False)
    order_date = db.Column(db.String(30), nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)
    product_price = db.Column(db.Integer, nullable=False)

    def _repr_(self) -> str:
      return f"{self.id} - {self.product_id} - {self.product_name} - {self.customer_id} - {self.customer_name} - {self.order_date} - {self.subtotal} - {self.product_price}"
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(30), nullable=False, unique=True)
    
    def _repr_(self) -> str:
      return f"{self.id} - {self.category}"

class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(30), nullable=False,)
    subcategory = db.Column(db.String(30), unique=True, nullable=False,)
    
    def _repr_(self) -> str:
      return f"{self.id} - {self.category} - {self.subcategory}"


class Inorder(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customerid = db.Column(db.String(30), nullable=False,)
    productid = db.Column(db.String(30), nullable=False,)
    productprice = db.Column(db.Integer, nullable=False,)
    orderdate = db.Column(db.String(30), nullable=False,)
    totalbill = db.Column(db.Integer, nullable=False,)
    address = db.Column(db.String(90), nullable=False,)
    qty = db.Column(db.Integer, nullable=False,)
    
    def _repr_(self) -> str:
      return f"{self.id} - {self.customerid} - {self.productid} - {self.productprice} - {self.orderdate} - {self.totalbill} - {self.qty}" 

class Inprogorder(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customerid = db.Column(db.String(30), nullable=False,)
    productid = db.Column(db.String(30), nullable=False,)
    productprice = db.Column(db.Integer, nullable=False,)
    orderdate = db.Column(db.String(30), nullable=False,)
    totalbill = db.Column(db.Integer, nullable=False,)
    address = db.Column(db.String(90), nullable=False,)
    qty = db.Column(db.Integer, nullable=False,)
    
    def _repr_(self) -> str:
      return f"{self.id} - {self.customerid} - {self.productid} - {self.productprice} - {self.orderdate} - {self.totalbill} - {self.qty}" 

class Comporder(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customerid = db.Column(db.String(30), nullable=False,)
    productid = db.Column(db.String(30), nullable=False,)
    productprice = db.Column(db.Integer, nullable=False,)
    orderdate = db.Column(db.String(30), nullable=False,)
    totalbill = db.Column(db.Integer, nullable=False,)
    address = db.Column(db.String(90), nullable=False,)
    qty = db.Column(db.Integer, nullable=False,)
    
    def _repr_(self) -> str:
      return f"{self.id} - {self.customerid} - {self.productid} - {self.productprice} - {self.orderdate} - {self.totalbill} - {self.qty}" 

class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(30), nullable=False,)
    e_date = db.Column(db.String(30), nullable=False,)
    
    def _repr_(self) -> str:
      return f"{self.id} - {self.email} - {self.e_date}"

class Contactus(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False,)
    email = db.Column(db.String(30), nullable=False,)
    phone = db.Column(db.String(30), nullable=False,)
    subject = db.Column(db.String(30), nullable=False,)
    message = db.Column(db.String(30), nullable=False,)
    
    def _repr_(self) -> str:
      return f"{self.id} - {self.email} - {self.email} - {self.subject} - {self.message} - {self.phone}"

adminname = "admin"
adminpassword = "abc123"


@app.route("/", methods=['GET', 'POST'])
def index():
    if 'username' in session:
        username = session['username']
        page = request.args.get('page', 1, type=int)
        products = Product.query.filter_by(top="top").paginate(page=page, per_page = 15)

        customer = Users.query.filter_by(name=username).first()
        incart = Cart.query.filter_by(customer_id=customer.customerid).all()
        countcart = Cart.query.filter_by(customer_id=customer.customerid).count()

        return render_template('index.html', products=products, username=username, incart=incart, countcart=countcart)

    if request.method == 'POST':
        username = request.form['login']
        userpass = request.form['password']
        record = Users.query.filter_by(name=username).filter_by(password=userpass).first()
        
        
        
        if record:
            session['loggedin'] = True
            session['username'] = username
            username = session['username']
            page = request.args.get('page', 1, type=int)
            products = Product.query.filter_by(top="top").paginate(page=page, per_page = 15)

            customer = Users.query.filter_by(name=username).first()
            incart = Cart.query.filter_by(customer_id=customer.customerid).all()
            countcart = Cart.query.filter_by(customer_id=customer.customerid).count()

            return render_template('index.html', products=products, username=username, incart=incart, countcart=countcart)
        
        else:
            flash("Incorrect Username or Password", "danger")

    return render_template('login.html',)



@app.route("/shop")
def shop():
    if 'username' in session:
        username = session['username']
        customer = Users.query.filter_by(name=username).first()
        incart = Cart.query.filter_by(customer_id=customer.customerid).all()
        countcart = Cart.query.filter_by(customer_id=customer.customerid).count()
        #incart = Cart.query.all()
        #cartprod = Product.query.filter_by(productid=incart.product_id)

        page = request.args.get('page', 1, type=int)
        products = Product.query.paginate(page=page, per_page = 15)
        return render_template('shop.html', products=products, username=username, incart=incart, countcart=countcart)
    else:
        return redirect("/")
    


@app.route("/about")
def about():
    if 'username' in session:
        username = session['username']
        return render_template('about-us.html', username=username)
    else:
        return redirect("/")
    


@app.route("/blog")
def blog():
    if 'username' in session:
        username = session['username']
        customer = Users.query.filter_by(name=username).first()
        incart = Cart.query.filter_by(customer_id=customer.customerid).all()
        countcart = Cart.query.filter_by(customer_id=customer.customerid).count()
        #incart = Cart.query.all()
        #cartprod = Product.query.filter_by(productid=incart.product_id)

        page = request.args.get('page', 1, type=int)
        products = Product.query.paginate(page=page, per_page = 15)
        return render_template('blog.html', products=products, username=username, incart=incart, countcart=countcart)
    else:
        return redirect("/")
    


@app.route("/cart")
def cart():
    if 'username' in session:
        username = session['username']
        customer = Users.query.filter_by(name=username).first()
        incart = Cart.query.filter_by(customer_id=customer.customerid).all()
        countcart = Cart.query.filter_by(customer_id=customer.customerid).count()
        if countcart >=1:
            subtotal = db.session.query(func.sum(Cart.subtotal)).filter(Cart.customer_id==customer.customerid).all()[0][0]
            if subtotal>=1500:
                shipping = int(0)
            else:
                shipping = int(200)
            finaltotal = subtotal+shipping

            page = request.args.get('page', 1, type=int)

            products = Product.query.paginate(page=page, per_page = 15)
            return render_template('cart.html', products=products, username=username, incart=incart, countcart=countcart, subtotal=subtotal, finaltotal=finaltotal)
        else:
            page = request.args.get('page', 1, type=int)
            subtotal=0
            finaltotal=0
            products = Product.query.paginate(page=page, per_page = 15)
            return render_template('cart.html', products=products, username=username, incart=incart, countcart=countcart, subtotal=subtotal, finaltotal=finaltotal)

    else:
        return redirect("/")
    


# @app.route("/checkout")
# def checkout():
#     if 'username' in session:
#         username = session['username']
#         customer = Users.query.filter_by(name=username).first()
#         incart = Cart.query.filter_by(customer_id=customer.customerid).all()
#         countcart = Cart.query.filter_by(customer_id=customer.customerid).count()
#         #incart = Cart.query.all()
#         #cartprod = Product.query.filter_by(productid=incart.product_id)

#         page = request.args.get('page', 1, type=int)
#         products = Product.query.paginate(page=page, per_page = 15)
#         return render_template('checkout.html', products=products, username=username, incart=incart, countcart=countcart)
#     else:
#         return redirect("/")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if 'username' in session:
        if (request.method == "POST"):
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            subject = request.form.get('subject')
            message = request.form.get('message')

            data = Contactus(name=name, email=email, phone=phone, subject=subject, message=message)
            db.session.add(data)
            db.session.commit()
            flash("The contact message is sent to Nibo", "success")

        username = session['username']
        customer = Users.query.filter_by(name=username).first()
        incart = Cart.query.filter_by(customer_id=customer.customerid).all()
        countcart = Cart.query.filter_by(customer_id=customer.customerid).count()
       
        page = request.args.get('page', 1, type=int)
        products = Product.query.paginate(page=page, per_page = 15)
        return render_template('contact.html', products=products, username=username, incart=incart, countcart=countcart)
    else:
        return redirect("/")
    


@app.route("/product/<string:id>" , methods = ['GET', 'POST'])
def product(id):
    
    username = session['username']
    data = Product.query.filter_by(sno=id).first()
    customer = Users.query.filter_by(name=username).first()
    incart = Cart.query.filter_by(customer_id=customer.customerid).all()
    countcart = Cart.query.filter_by(customer_id=customer.customerid).count()

    return render_template("product-page.html", data=data, username=username, incart=incart, countcart=countcart) 


@app.route("/delete/<string:id>", methods = ['GET', 'POST'])
def delete1(id):
    if "username" in session:

        username = session['username']

        customer = Users.query.filter_by(name=username).first()

        deldata = Cart.query.filter_by(id=id).filter_by(customer_id=customer.customerid).first()
        db.session.delete(deldata)
        db.session.commit()
        flash("The record is deleted succesfully", "success")
    return redirect('/shop') 


    

    


@app.route("/register", methods=['GET', 'POST'])
def register():
    if (request.method == "POST"):
        details = request.form
        name1 = details['name']
        firstname1 = details['firstname']
        lastname1 = details['lastname']
        email1 = details['email']
        phone1 = details['phone']
        address1 = details['address']
        password1 = details['password']
        password2 = details['cpassword']

        #for username
        recordname = Users.query.filter_by(name = name1).first()
    
        #for email id
        recordemail = Users.query.filter_by(email = email1).first()

        if recordname:
            flash("This username and email is already in user!", "danger")

        elif recordemail:
            flash("Email is already registerd!", "danger")
            
        else:
            if(password1==password2):
                msg = Message('Welcome to NIBO', sender = "watchwhistle@gmail.com", recipients = [email1])
                msg.body = name1 + '"We welcome you to join our community. Now you can buy our products."'
                msg.html = "<b> Hey"+ name1+"</b><br><p>We welcome you to join our community. Now you can buy our products.</p><br><br><a href='http://127.0.0.1:19000/forget'>Foget Password</a><br>If that was not you ignore this emial.<br><br><b>MoviesVerse</b>"
                mail.send(msg)
                flash("The mail is successfully send", "success")
                datainsert = Users(customerid=uuid.uuid1().hex[:8], name=name1, firstname=firstname1, lastname = lastname1, email=email1, phone=phone1, address=address1, password=password1)
                db.session.add(datainsert)
                db.session.commit()
                return redirect('/register')

            else:
                flash ("password is not matched", "danger")

    return render_template('register.html')

@app.route("/addtocart/<string:id>", methods=['GET', 'POST'])
def addtocart(id):
    
    if request.method == 'POST':
        size1 = request.form['size']
        qty1 = request.form['qty']
        qty2 = int(qty1)
        data = Product.query.filter_by(sno=id).first()
        customer = Users.query.filter_by(name=session['username']).first()
        cartalready = Cart.query.filter_by(product_id=data.productid).first()

        if cartalready:
            flash("The record already in cart", "warning")
        else:
            if qty2>data.quantity:
                flash('The quantity you select is high, we have only few items left', "danger")
            elif qty2<1:
                flash('The selected quantity is 0', "danger")
            else:
                datainsert = Cart(product_id=data.productid, product_name=data.productname, size=size1, qty=qty1, customer_id=customer.customerid, customer_name=customer.name, product_price=data.price, order_date=date.today(), subtotal=(data.price*qty2))
                db.session.add(datainsert)
                db.session.commit()

        return redirect('/shop')

    else:
        return redirect('/')

@app.route("/cartlist", methods=['GET', 'POST'])
def cartlist():
    if "username" in session:
        customer = Users.query.filter_by(name=session['username']).first()
        incart = Cart.query.filter_by(customer_id=customer.customerid).all()
        product = Cart.query.filter_by()
        
        return render_template("admin/cart.html", incart=incart, username="session['username']", total="100")

    return redirect("/adminindex", username=session['user'])

@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    if "username" in session:
        customer = Users.query.filter_by(name=session['username']).first()
        incart = Cart.query.filter_by(customer_id=customer.customerid).all()
        
        subtotal = db.session.query(func.sum(Cart.subtotal)).filter(Cart.customer_id==customer.customerid).all()[0][0]
        if subtotal>=1500:
            shipping = int(0)
        else:
            shipping = int(200)
        finaltotal = subtotal+shipping
        for data1 in incart:
            data = Inorder(customerid=data1.customer_id, productid=data1.product_id, productprice=data1.product_price,address=customer.address, orderdate=date.today(), totalbill=finaltotal, qty=data1.qty)
            db.session.add(data)
            db.session.commit()
            data2 = Cart.query.filter_by(customer_id=data1.customer_id).first()
            db.session.delete(data2)
            db.session.commit()
            page = request.args.get('page', 1, type=int)
            products = Product.query.paginate(page=page, per_page = 15)
        flash("The your order submitted succefuly", "success")
        return render_template("shop.html", incart=incart, username="session['username'], ",products=products)

    return redirect("/adminindex", username=session['user'])

@app.route("/newsletter", methods=['GET', 'POST'])
def newsletter():
    if "username" in session:
        if request.method=="POST":
            email = request.form.get('email') 
            e_date = date.today()
            data = Newsletter(email=email, e_date=e_date)
            db.session.add(data)
            db.session.commit()
            return render_template("blog.html")
        else:
            return render_template("blog.html")
        

    return redirect("/adminindex", username=session['user'])


@app.route("/logout")
def logout():
    session.pop('username')
    return redirect('/')

#admin panel working
@app.route("/adminindex", methods=['GET', 'POST'])
def adminindex():
    if "user" in session:
        productcount = Product.query.count()
        userscount = Users.query.count()
        return render_template("admin/index.html", username=session['user'], productcount=productcount, userscount=userscount)

    if request.method =="POST":
        name=request.form.get("adminname1")
        password= request.form.get("adminpassword1")

        if name == adminname and password == adminpassword:
            session['user'] = name
            productcount = Product.query.count()
            userscount = Users.query.count()
            return render_template("admin/index.html", username=session['user'], productcount=productcount, userscount=userscount)

    return redirect("/adminsignin")

@app.route("/adminsignin")
def adminsignin():
    if 'user' in session:
        return redirect('/adminindex', username=session['user'])
    else:
        return render_template("admin/adminsignin.html")

@app.route("/adminlogout")
def adminlogout():
    session.pop('user')
    return redirect('/adminsignin')

@app.route("/addproduct", methods=['GET', 'POST'])
def addproduct():
    if "user" in session:
        if request.method=="POST":
            productid1 = request.form.get('productid') 
            productname1 = request.form.get('productname')
            category1 = request.form.get('category')
            subcategory1 = request.form.get('subcategory')
            colour1 = request.form.get('colour')
            quantity1 = request.form.get('quantity')
            price1 = request.form.get('price')
            description = request.form.get('description')

            picture1 = request.files['picture1']
            picture1.filename = productid1 + "1" +  ".png"
            p1_filename = secure_filename(picture1.filename)
            p1 = p1_filename
            


            picture2 = request.files['picture2']
            picture2.filename = productid1 + "2" +  ".png"
            p2_filename = secure_filename(picture2.filename)
            p2 = p2_filename
            
            picture3 = request.files['picture3']
            picture3.filename = productid1 + "3" +  ".png"
            p3_filename = secure_filename(picture3.filename)
            p3 = p3_filename
            

            picture4 = request.files['picture4']
            picture4.filename = productid1 + "4" +  ".png"
            p4_filename = secure_filename(picture4.filename)
            p4 = p4_filename

            picture1.save(os.path.join(app.config['POSTER_UPLOAD'], secure_filename(picture1.filename)))
            picture2.save(os.path.join(app.config['POSTER_UPLOAD'], secure_filename(picture2.filename)))
            picture3.save(os.path.join(app.config['POSTER_UPLOAD'], secure_filename(picture3.filename)))
            picture4.save(os.path.join(app.config['POSTER_UPLOAD'], secure_filename(picture4.filename)))

            #productid1 = request.form.get('productid')
            #productid1 = request.form.get('productid')
            check = Product.query.filter_by(productid=productid1).first()
            if (check):
                flash("Product ID is already in use.", "danger")
            else:
                productadd = Product(productid=productid1, productname=productname1, category=category1, subcategory=subcategory1, colour=colour1, quantity=quantity1, price=price1, picture1=p1, picture2=p2, picture3=p3, picture4=p4, description=description )
                db.session.add(productadd)
                db.session.commit()
                flash("Product Addedd Successfully", "success")
            return redirect("/addproduct")
        else:    
            category = Category.query.all()
            subcategory = Subcategory.query.all()
            return render_template("admin/addproduct.html", category=category, subcategory=subcategory, username=session['user'])

    else:
        return redirect("/adminindex", username=session['user'])
    
@app.route("/productlist", methods=['GET', 'POST'])
def productlist():
    if "user" in session:
        product = Product.query.all()
        return render_template("admin/productlist.html", product=product, username=session['user'])

    return redirect("/adminindex", username=session['user'])

@app.route("/productdelete/<string:productid>", methods = ['GET', 'POST'])
def productdelete(productid):
    if "user" in session:
        deldata = Product.query.filter_by(productid=productid).first()
        db.session.delete(deldata)
        db.session.commit()
        flash("The record is deleted succesfully", "success")
        return redirect('/productlist')
    else:
        return redirect("/adminindex")

@app.route("/userslist", methods=['GET', 'POST'])
def userlist():
    if "user" in session:
        users = Users.query.all()
        return render_template("admin/userslist.html", users=users, username=session['user'])

    return redirect("/adminindex", username=session['user'])

@app.route("/userdelete/<string:customerid>", methods = ['GET', 'POST'])
def usersdelete(customerid):
    if "user" in session:
        deldata = Users.query.filter_by(customerid=customerid).first()
        db.session.delete(deldata)
        db.session.commit()
        flash("The record is deleted succesfully", "success")
        return redirect('/userslist')
    else:
        return redirect("/adminindex")


@app.route("/neworders")
def neworder():
    if "user" in session:
        order = Inorder.query.all()
        return render_template("admin/neworders.html", order=order)
    else:
        return redirect("/adminindex")

@app.route("/inprogorder")
def inprogorders():
    if "user" in session:
        order = Inprogorder.query.all()
        return render_template("admin/inprogorders.html", order=order)
    else:
        return redirect("/adminindex")

@app.route("/completeorder")
def completeorders():
    if "user" in session:
        order = Comporder.query.all()
        return render_template("admin/completeorders.html", order=order)
    else:
        return redirect("/adminindex")

@app.route("/inprogorders/<string:customerid>", methods = ['GET', 'POST'])
def inprogorder(customerid):
    if "user" in session:
        order = Inorder.query.filter_by(customerid=customerid).all()
        customer = Users.query.filter_by(customerid=customerid).first()
        for data in order:
            datainsert = Inprogorder(customerid=data.customerid, productid=data.productid, productprice=data.productprice, orderdate=data.orderdate, totalbill=data.totalbill, address=data.address, qty=data.qty)
            db.session.add(datainsert)
            db.session.commit()
            db.session.delete(data)
            db.session.commit()
        
        msg = Message('Order In Progress', sender = "watchwhistle@gmail.com", recipients = [customer.email])
        msg.body = customer.name + '"Thank You for buynig the product, Hope you would like it"'
        msg.html = "<b> Hey"+ customer.name+"</b><br><p>Thank You for buynig the product, Hope you would like it.</p><br><br>The order will be shortly on your doorsteps.<br><br><b>NIBO</b>"
        mail.send(msg)
        flash("The order is transfered to in-progress order","success")
        return render_template("admin/neworders.html", order=order)
    else:
        return redirect("/adminindex")

@app.route("/completeorders/<string:customerid>", methods = ['GET', 'POST'])
def completeorder(customerid):
    if "user" in session:
        order = Inprogorder.query.filter_by(customerid=customerid).all()
        customer = Users.query.filter_by(customerid=customerid).first()
        for data in order:
            datainsert = Comporder(customerid=data.customerid, productid=data.productid, productprice=data.productprice, orderdate=data.orderdate, totalbill=data.totalbill, address=data.address, qty=data.qty)
            db.session.add(datainsert)
            db.session.commit()
            db.session.delete(data)
            db.session.commit()
        
        msg = Message('Order Successfully Completed', sender = "watchwhistle@gmail.com", recipients = [customer.email])
        msg.body = customer.name + '" Thank You for buynig the product, Hope you would like it"'
        msg.html = "<b> Hey"+ customer.name+"</b><br><p>The order is on your address. Thank You for buynig the product, Hope you would like it.</p><br><br>Keep shoppping from NIBO.<br><br><b>NIBO</b>"
        mail.send(msg)
        flash("The order is completed and transfer to compelted order","success")
        return render_template("admin/inprogorders.html", order=order)
    else:
        return redirect("/adminindex")

@app.route("/deletecompleteorder/<string:customerid>", methods = ['GET', 'POST'])
def completeorderdel(customerid):
    if "user" in session:
        deldata = Comporder.query.filter_by(customerid=customerid).all()
        for data in deldata:
            db.session.delete(data)
            db.session.commit()
        flash("The record is deleted succesfully", "success")
        return redirect('/completeorder')
    else:
        return redirect("/adminindex")

@app.route("/deleteinprogorder/<string:customerid>/<string:productid>", methods = ['GET', 'POST'])
def inprogorderdel(customerid, productid):
    if "user" in session:
        data = Inprogorder.query.filter_by(customerid=customerid).filter_by(productid=productid).first()
        customer = Users.query.filter_by(customerid=customerid).first()
        product = Product.query.filter_by(productid=productid).first()
        db.session.delete(data)
        db.session.commit()
        msg = Message('Order Could not be completed', sender = "watchwhistle@gmail.com", recipients = [customer.email])
        msg.body = customer.name + '" Sorry for cancelation of order"'
        msg.html = "<b> Hey "+ customer.name+"</b><br><p> We have to sorry but the product your order is not available anymore.</p><br>"+ product.productname+"<br>Keep shoppping from NIBO.<br><br><b>NIBO</b>"
        mail.send(msg)
        flash("The record is deleted succesfully", "success")
        return redirect('/completeorder')
    else:
        return redirect("/adminindex")

@app.route("/deleteneworder/<string:customerid>/<string:productid>", methods = ['GET', 'POST'])
def neworderdel(customerid, productid):
    if "user" in session:
        data = Inorder.query.filter_by(customerid=customerid).filter_by(productid=productid).first()
        customer = Users.query.filter_by(customerid=customerid).first()
        product = Product.query.filter_by(productid=productid).first()
        db.session.delete(data)
        db.session.commit()
        msg = Message('Order Could not be completed', sender = "watchwhistle@gmail.com", recipients = [customer.email])
        msg.body = customer.name + '" Sorry for cancelation of order"'
        msg.html = "<b> Hey "+ customer.name+"</b><br><p> We have to sorry but the product your order is not available anymore.</p><br>"+ product.productname+"<br>Keep shoppping from NIBO.<br><br><b>NIBO</b>"
        mail.send(msg)
        flash("The record is deleted succesfully", "success")
        return redirect('/completeorder')
    else:
        return redirect("/adminindex")
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(port=98000)
