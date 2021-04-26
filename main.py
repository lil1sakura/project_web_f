from flask import Flask, url_for, request, render_template, redirect, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from bd import flash, get_db
from FDataBase import FDataBase
from flask_login import LoginManager, login_user, login_required
from UserLogin import UserLogin
import os
from flask_mail import Mail
import config
from send_email import sendMessage



database = '/tmp/bd.db'
debug = True
app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = config.email
app.config['MAIL_PASSWORD'] = config.psw
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
app.debug = True
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'



app.config.update(dict(database=os.path.join(app.root_path, 'bd.db')))
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return UserLogin().create(user_id)



@app.route('/')
@app.route('/home')
def main():
    return render_template('index.html', title='Tim pizza')


@app.route('/contact')
def contact():

    return render_template('contact.html', title='Контакты')


@app.route('/aboutus')
def about_us():
    return render_template('about.html', title='О нас')




@app.route('/talktous', methods=["POST", "GET"])
def talk_to_us():
    if request.method == 'POST':
        result = {}
        result['first_name'] = request.form['first_name']
        result['last_name'] = request.form['last_name']
        result['phone'] = request.form['phone']
        result['email'] = request.form['email'].replace(' ', '').lower()
        result['message'] = request.form['message']
        msg = sendMessage(result)
        mail.send(msg)
        return redirect(url_for('main'))
    return render_template('talktous.html', title='Написать письмо')


@app.route('/shipinfo', methods=["POST", "GET"])
def shipinfo():
    if request.method == 'POST':
        result = {}
        result['first_name'] = request.form['first_name']
        result['last_name'] = request.form['last_name']
        result['phone'] = request.form['phone']
        result['email'] = request.form['email'].replace(' ', '').lower()
        result['address'] = request.form['address']
        result['message'] = request.form['message']
        msg = sendMessage(result)
        mail.send(msg)
        return redirect(url_for('main'))
    return render_template('shipinfo.html', title='Оплата')


@app.route('/login', methods=["POST", "GET"])
def login():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('main'))
        flash("Неверный логин или пароль", "error")
    return render_template('login.html', title='Авторизация')


@app.route('/register', methods=["POST", "GET"])
def register():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if len(request.form['email']) > 4 \
                and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['email'], hash)
            if res:
                flash("Вы успешно зарегестрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")
    return render_template('register.html', title='Регистрация')


if __name__ == '__main__':
    app.run(port=8085, host='127.0.0.1')
    app.run(debug=True)
