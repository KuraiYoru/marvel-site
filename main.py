from app import login_manager

from app import app
from flask import render_template, request, redirect
from models import Heroes, Comics, User
from flask_paginate import get_page_parameter
from forms import FilterForm, RegisterForm


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
    pages = hero.comics.paginate(page=page, per_page=24)
    # pages = comics.paginate(page=page_id, per_page=24)

    return render_template('hero.html', hero=hero, pages=pages)


@app.route('/comics/<int:comics_id>/')
def comics(comics_id):
    page = request.args.get(get_page_parameter(), type=int, default=1)
    comics = Comics.query.filter_by(comics_id=comics_id).first()
    pages = comics.heroes.paginate(page=page, per_page=24)
    return render_template('comics.html', comics=comics, pages=pages)


def main():
    app.run(debug=True)


@login_manager.user_loader
def load_user(user_id):
    return User


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegisterForm()
    if form.submit.data:
        print(form.submit.data)
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")

        # if db_sess.query(User).filter(User.email == form.email.data).first():
        #     return render_template('register.html', title='Регистрация',
        #                            form=form,
        #                            message="Такой пользователь уже есть")
        # user = User(
        #     name=form.name.data,
        #     email=form.email.data,
        #     about=form.about.data
        # )
        # user.set_password(form.password.data)
        # db_sess.add(user)
        # db_sess.commit()
        # return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)




if __name__ == '__main__':
    main()

