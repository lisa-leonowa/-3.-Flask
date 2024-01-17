# Создать форму для регистрации пользователей на сайте. Форма должна содержать поля "Имя", "Фамилия",
# "Email", "Пароль" и кнопку "Зарегистрироваться". При отправке формы данные должны сохраняться в базе
# данных, а пароль должен быть зашифрован.


from flask import Flask, render_template
from data.users import User
from data import db_session
from flask_login import LoginManager
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    last_name = StringField('Фамилия пользователя', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


@login_manager.user_loader
def load_user(user_id):
    sessions = db_session.create_session()
    return sessions.query(User).get(user_id)


@app.route('/', methods=['POST', 'GET'])
def base():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            session = db_session.create_session()

            user = User(name=form.name.data, last_name=form.last_name.data, email=form.email.data)
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            return render_template('index.html', form=form, message='Пользователь был зарегистрирован!')
        except:
            return render_template('index.html', form=form, message='Пользователя не удалось зарегистрировать!')
    return render_template('index.html', form=form, message='')


if __name__ == '__main__':
    db_session.global_init("db/users.sqlite")
    app.run(port=8080, host='127.0.0.1')
