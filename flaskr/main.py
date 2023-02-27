from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, img, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('main/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        img = request.form['img']
        error = None

        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, img, author_id)'
                'VALUES (?,?,?,?)',
                (title, body, img, g.user['id'])
            )
            db.commit()
            return redirect(url_for('main.index'))

    return render_template('main/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, img, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id =?',
        (id, )
    ).fetchone()

    if post is None:
        abort(404, f"Post {id} doesn't exist")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@ bp.route('/<int:id>/update', methods=('GET', 'POST'))
@ login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        img = request.form['img']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title =?, body =?, img=?'
                'WHERE id =?',
                (title, body, img, id)
            )
            db.commit()
            return redirect(url_for('main.index'))

    return render_template('main/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id =?', (id, ))
    db.commit()
    return redirect(url_for('main.index'))


@bp.route('/about', methods=('get', 'POST'))
def about():
    return render_template('main/about.html')
