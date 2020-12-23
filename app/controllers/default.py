from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user
from flask import request
from app import app, db, login_manager
from app.models.forms import LoginForm
from app.models.tables import User



@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/inicial")
def inicial():
    return render_template('inicial.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            #flash("Usuario Logado")
            return redirect (url_for("inicial"))
        else:
            flash("Login Invalido")
    return render_template('login.html', form=form)


@app.route("/cadastro")
def cadastro():
    return render_template('cadastro.html')


@app.route("/cadastrar", methods=["GET","POST"])
def cadastrar():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        email = request.form.get("email")

        if username and  password and name and email:
            p = User (username, password, name, email)
            db.session.add(p)
            db.session.commit()

    return redirect (url_for("index"))




@app.route("/lista")
def lista():
    pessoas = User.query.all()
    return render_template("lista.html", pessoas=pessoas)


@app.route("/excluir/<int:id>")
def excluir(id):
    pessoa = User.query.filter_by(id=id).first()
    db.session.delete(pessoa)
    db.session.commit()
    pessoas = User.query.all()
    return render_template("lista.html", pessoas=pessoas)



@app.route("/atualizar/<int:id>", methods=["GET","POST"])
def atualizar(id):
    pessoa = User.query.filter_by(id=id).first()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        email = request.form.get("email")

        if username and  password and name and email:
            pessoa.username = username
            pessoa.password = password
            pessoa.name = name
            pessoa.email = email

            db.session.commit()
            return redirect(url_for('lista'))
    return render_template("atualizar.html", pessoa=pessoa)




@app.route("/logout")
def logout():
    logout_user()
    #flash("Usuario Saiu")
    return redirect (url_for("index"))

