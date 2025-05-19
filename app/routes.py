from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.models import User
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, timedelta

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы зарегистрированы!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            now = datetime.utcnow()
            if user.is_locked_until and user.is_locked_until > now:
                flash(f'Слишком много попыток. Попробуйте позже: {user.is_locked_until.strftime("%H:%M:%S")}', 'danger')
            elif bcrypt.check_password_hash(user.password, form.password.data):
                user.login_attempts = 0
                user.is_locked_until = None
                db.session.commit()
                login_user(user)
                return redirect(url_for('index'))
            else:
                user.login_attempts += 1
                user.last_attempt = now
                if user.login_attempts >= 5:
                    user.is_locked_until = now + timedelta(minutes=5)
                db.session.commit()
                flash('Неверное имя пользователя или пароль', 'danger')
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/click')
@login_required
def click():
    current_user.clicks += 1
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/reset')
@login_required
def reset():
    current_user.clicks = 0
    db.session.commit()
    flash('Счётчик сброшен!', 'success')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return "Внутренняя ошибка сервера", 500