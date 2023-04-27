import os
from app import login_manager
from app import app, db
from flask import render_template, request, redirect, abort
from models import Heroes, Comics, User, UserComics
from flask_paginate import get_page_parameter
from forms import FilterForm, RegisterForm, LoginForm, EditProfile
from flask_login import current_user, login_required, login_user, logout_user


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    q = request.args.get('q')
    form = FilterForm()
    if q is None:
        q = ''

    if not q:
        heroes = Heroes.query
        pages = heroes.paginate(page=page, per_page=24)
    else:
        heroes = Heroes.query.filter(Heroes.name.contains(q))
        pages = heroes.paginate(page=page, per_page=24)

    if form.validate_on_submit():
        if not form.submit1.raw_data:
            name_of_hero = form.name.data
            heroes = Heroes.query.filter(Heroes.name.contains(name_of_hero))
            pages = heroes.paginate(page=1, per_page=24)
            q = name_of_hero
        else:
            q = ''
            pages = Heroes.query.paginate(page=1, per_page=24)
            form.name.data = ''
    form.name.data = q
    return render_template('index.html', pages=pages, form=form, q=q)


@app.route('/hero/<int:hero_id>/')
def hero(hero_id):
    page = request.args.get(get_page_parameter(), type=int, default=1)
    hero = Heroes.query.filter_by(hero_id=hero_id).first()
    if hero:
        pages = hero.comics.paginate(page=page, per_page=24)
    else:
        abort(404)

    return render_template('hero.html', hero=hero, pages=pages)


@app.route('/comics/<int:comics_id>/')
def comics(comics_id):
    page = request.args.get(get_page_parameter(), type=int, default=1)
    comics = Comics.query.filter_by(comics_id=comics_id).first()
    if comics:
        pages = comics.heroes.paginate(page=page, per_page=24)

    return render_template('comics.html', comics=comics, pages=pages)


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.submit.data:
        f = request.files.get('fileUpload[]').read()

        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")

        if User.query.filter_by(email=form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            user_name=form.name.data,
            email=form.email.data,
            hashed_password=form.password.data,
        )
        user.hash_password()
        db.session.add(user)
        db.session.commit()
        login_user(user)
        if f:
            with open(f'static/img/img_{user.id}.png', 'wb') as file:
                file.write(f)

        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    error = False
    action = request.args.get('action', default='future')
    print(action)
    if action == 'future':
        future = UserComics.query.filter_by(user_id=current_user.id, action='В планах').with_entities(UserComics.comics_id).all()
        future = [i[0] for i in future]
        lst = Comics.query.filter(Comics.comics_id.in_(future))
    elif action == 'now':
        future = UserComics.query.filter_by(user_id=current_user.id, action='Читаю').with_entities(
            UserComics.comics_id).all()
        future = [i[0] for i in future]
        lst = Comics.query.filter(Comics.comics_id.in_(future))
    elif action == 'past':
        future = UserComics.query.filter_by(user_id=current_user.id, action='Прочитано').with_entities(
            UserComics.comics_id).all()
        future = [i[0] for i in future]
        lst = Comics.query.filter(Comics.comics_id.in_(future))
    else:
        abort(404)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pages = lst.paginate(page=page, per_page=24)
    try:
        with open(f'static/img/img_{current_user.id}.png') as f:
            pass
    except FileNotFoundError:
        error = True

    return render_template('profile.html', pages=pages, action=action, error=error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/comics/<int:comics_id>/<action>')
@login_required
def add_comics_to_user(comics_id, action):
    u = UserComics.query.filter_by(comics_id=comics_id, user_id=current_user.id)
    if u:
        u.delete()
    if action == 'future':
        new = UserComics(user_id=current_user.id, comics_id=comics_id, action='В планах')
    elif action == 'now':
        new = UserComics(user_id=current_user.id, comics_id=comics_id, action='Читаю')
    elif action == 'past':
        new = UserComics(user_id=current_user.id, comics_id=comics_id, action='Прочитано')
    else:
        abort(404)

    db.session.add(new)
    db.session.commit()
    return redirect(f'/comics/{comics_id}/')


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    error = False
    form = EditProfile()
    user = User.query.filter_by(id=current_user.id).first()
    if request.method == "GET":
        try:
            with open(f'static/img/img_{current_user.id}.png') as f:
                pass
        except FileNotFoundError:
            error = True
        if user:
            form.name.data = user.user_name
        else:
            abort(404)

    if form.submit.data:
        user.user_name = form.name.data
        f = request.files.get('fileUpload[]').read()
        if f:
            with open(f'static/img/img_{user.id}.png', 'wb') as file:
                file.write(f)

        db.session.commit()
        return redirect('/profile')

    return render_template('edit_profile.html', form=form, error=error)


@app.route('/delete_comics/<int:comics_id>')
@login_required
def delete_comics(comics_id):
    art = UserComics.query.filter_by(user_id=current_user.id, comics_id=comics_id).first()
    if art:
        db.session.delete(art)
        db.session.commit()
    else:
        abort(404)
    return '<script>document.location.href = document.referrer</script>'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    main()

