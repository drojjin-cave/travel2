from flask import Flask, render_template, url_for, flash, redirect, request, abort
from data import db_session
from data.users import User
from data.news import News
from datetime import datetime
from forms.user import RegisterForm, LoginForm
from forms.news import NewsForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_uploads import configure_uploads, patch_request_class


app = Flask(__name__)
app.config.from_object('data.config')
login_manager = LoginManager()
login_manager.init_app(app)
configure_uploads(app, NewsForm.photos)
patch_request_class(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)



@app.route('/')
@app.route('/home')
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    users = db_sess.query(User)
    count_news = len(news.all())
    return render_template("index.html",title='Главная', news=news, users=users, count_news=count_news, User=User)


@app.route('/archiv')
def archiv():
    db_sess = db_session.create_session()
    news = db_sess.query(News)
    count_news = len(news.all())
    return render_template("archiv.html", title='Блог', news=news, count_news=count_news)


@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        try:
            filename = NewsForm.photos.save(form.photo.data)
        except:
            filename = None

        news.title = form.title.data
        news.content = form.content.data
        if filename:
            news.img = filename
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')


    return render_template('news.html', title='Добавление новости', form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        users = db_sess.query(User)

        rol = users.filter(User.id == current_user.id).first().role

        if rol == 'admin':
            news = db_sess.query(News).filter(News.id == id).first()
        else:
            news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()
        file = news.img

        if news:
            form.title.data = news.title
            form.content.data = news.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        users = db_sess.query(User)
        rol = users.filter(User.id == current_user.id).first().role
        if rol == 'admin':
            news = db_sess.query(News).filter(News.id == id).first()
        else:
            news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()


        try:
            filename = NewsForm.photos.save(form.photo.data)
        except:
            filename = None

        if news:
            if form.validate_on_submit():
                news.img = None
            if filename:
                news.img = filename

            news.title = form.title.data
            news.content = form.content.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html', title='Редактирование новости', form=form, file=file)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    users = db_sess.query(User)

    rol = users.filter(User.id == current_user.id).first().role
    if rol == 'admin':
        news = db_sess.query(News).filter(News.id == id).first()
    else:
        news = db_sess.query(News).filter(News.id == id, News.user == current_user).first()

    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена")

@app.route('/archiv_not')
def archiv_not():
    return render_template('archiv_not.html', title="Архив не найден")

@app.route("/register", methods = ['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            flash('Пароли не совпадают', category='error')
            return redirect(url_for('register'))

        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data).first():
            flash('Такой пользователь уже существует', category='error')
            return redirect(url_for('register'))


        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        flash('Вы зарегестрированы!', category='success')
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods = ['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if not user:
            flash('Такого пользователя не существует', category='error')
            return redirect(url_for('login'))
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect("/")
        flash('Неправильный логин или пароль', category='error')
        return redirect(url_for('login'))

    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")




def main():
    db_session.global_init("db/data.db")
    app.run()


if __name__ == '__main__':
    main()
