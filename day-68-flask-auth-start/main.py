from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SomeSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD FOLDER'] = "./static/files/"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
#Line below only required once, when creating DB. 
# db.create_all()

## CREATE USER LOGIN FORM
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    logged_in = False
    if current_user.is_authenticated:
        logged_in = True
    return render_template("index.html", logged_in=logged_in)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_to_save = User(
            name = request.form.get("name"),
            email = request.form.get("email"),
            password = generate_password_hash(password=request.form.get("password"), method="pbkdf2:sha256", salt_length=8)
        )
        error = None
        check_user = User.query.filter_by(email=user_to_save.email).first()
        if check_user:
            flash("That email already registered. Please Login.")
            return redirect(url_for("login"))
        else:
            db.session.add(user_to_save)
            db.session.commit()
            login_user(user_to_save)
            return redirect(url_for("secrets", user_name=user_to_save.name))

        # match = check_password_hash(pwhash=user_to_save.password, password="register")
        # return f"{user_to_save.password}\n{match}"
    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            user_to_login = User.query.filter_by(email=email).first()
            if check_password_hash(pwhash=user_to_login.password, password=password):
                login_user(user_to_login)
                # flash('You were successfully logged in')
                return redirect(url_for("secrets", user_name=user_to_login.name))
            else:
                flash("Password incorrect, please try again.")
                return redirect(url_for("login"))
        except:
            flash("That email doesn't exist, please try again.")
            return redirect(url_for("login"))
    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/secrets')
@login_required
def secrets():
    user_name = request.args.get("user_name")
    return render_template("secrets.html", user_name=user_name, logged_in = True)


@app.route('/download')
def download():
    return send_from_directory(app.config["UPLOAD FOLDER"], filename="cheat_sheet.pdf", as_attachment=True)


@app.route("/delete")
def delete():
    # manually delete the first user id
    user_id_to_delete = db.session.query(User).get(1)
    db.session.delete(user_id_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
