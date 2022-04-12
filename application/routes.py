import time

from loguru import logger

from application.UserLogin import UserLogin as uslg
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from application import *

@app.route("/")
def index():
    # try:

    user = models.getUser(current_user.get_id())["username"]
    return render_template("index.html", username=user, elements=models.GetItems())
    # except Exception as ex: return ex

@login_manager.user_loader
def load_user(user_id):
    return uslg().from_db(user_id)

@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        if request.method == "POST":


            username = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            confirmPassword = request.form.get("confirmPassword")


            if password == confirmPassword:

                user = models.getUserByUsername(username)
                user2 = models.getUserByEmail(email)



                if user["username"] == False and user2["username"] == False:
                    user = models.Users(username=username, password=password, email=email, ip=request.remote_addr)
                    db.session.add(user)
                    db.session.commit()

                    user = models.getUserByUsername(username)

                    userLogin = uslg().create(user)
                    login_user(userLogin)
                    user = models.getUser(current_user.get_id())["username"]
                    return render_template("index.html", username=user)
                else:
                    flash("error")
                    user = models.getUser(current_user.get_id())["username"]
                    return render_template("register.html", username=user)

            else:
                flash("error")
                user = models.getUser(current_user.get_id())["username"]
                return render_template("register.html", username=user)


        user = models.getUser(current_user.get_id())["username"]
        return render_template("register.html", username=user)
    except: return "404"

@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":


            username = request.form.get("name")
            password = request.form.get("name1")


            user = models.getUserByUsername(username)

            usernamee = user["username"]

            if usernamee == False:
                flash("error")
                return  render_template("login.html")

            else:

                if user["password"] == password:

                    userLogin = uslg().create(user)
                    login_user(userLogin)

                    return redirect(url_for('index'))

                else:
                    flash("error")
                    return render_template("login.html")



        user = models.getUser(current_user.get_id())["username"]
        return render_template("login.html", username=user)
    except: return "404"

@app.route("/profile")
@login_required
def profile():
    try:
        user = models.getUser(current_user.get_id())
        return render_template("profile.html", username=user["username"], amount=user["balance"], date=user["date"], email=user["email"])
    except: return "404"

@app.route("/add-item", methods=["GET", "POST"])
@login_required
def AddItem():
    try:
        if request.method == "POST":
            contact = request.form.get("telegram")
            title = request.form.get("name")
            price = request.form.get("price")
            description = request.form.get("description")
            img = request.form.get("img")

            user = models.getUser(current_user.get_id())
            models.AddItemToBase(title=title, description=description, price=price, contact=contact, user_id=user["id"], img=img)

        else:
            user = models.getUser(current_user.get_id())
            return render_template("tracking-order.html", username=user["username"])

        user = models.getUser(current_user.get_id())
        return render_template("tracking-order.html", username=user["username"])
    except: return "404"

@app.route("/item/<string:item_id>")
def ViewItem(item_id):
    try:
        item = models.GetItemById(item_id)
        user = models.getUser(current_user.get_id())

        return render_template("single-product.html", username=user["username"], img=item["img"], title=item["title"], price=item["price"], description=item["description"], )
    except: return "404"

# @login_required - только для зарегистрированных