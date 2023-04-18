from app import app
from flask import render_template, request
from models import Heroes, Comics
from flask_paginate import get_page_parameter


@app.route('/')
def hello_world():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    print(page)
    heroes = Heroes.query
    pages = heroes.paginate(page=page, per_page=24)
    return render_template('index.html', pages=pages)


@app.route('/hero/<int:hero_id>/')
def hero(hero_id):
    page = request.args.get(get_page_parameter(), type=int, default=1)
    print(page)
    hero = Heroes.query.filter_by(hero_id=hero_id).first()
    pages = hero.comics.paginate(page=page, per_page=24)
    # pages = comics.paginate(page=page_id, per_page=24)

    return render_template('hero.html', hero=hero, pages=pages)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
