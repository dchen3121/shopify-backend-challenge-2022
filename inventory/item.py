import csv
from io import StringIO
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.wrappers import Response

from inventory.db import get_db

bp = Blueprint('item', __name__)


@bp.route('/')
def index():
    db = get_db()
    items = db.execute(
        'SELECT id, name, num_in_stock, description'
        ' FROM item ORDER BY id ASC'
    ).fetchall()
    return render_template('item/index.html', items=items)


@bp.route('/new', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form.get('name', None)
        num_in_stock = request.form.get('num_in_stock')
        description = request.form.get('description')

        error = None
        if not name:
            error = 'Item name is required.'
        if not num_in_stock:
            num_in_stock = 0
        elif not num_in_stock.isdigit():
            error = 'Number of items in stock must be a non-negative integer'


        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO item (name, num_in_stock, description)'
                ' VALUES (?, ?, ?)',
                (name, num_in_stock, description)
            )
            db.commit()
            return redirect(url_for('item.index'))

    return render_template('item/create.html')


@bp.route('/<int:id>', methods=('GET', 'POST'))
def update(id):
    item = get_db().execute(
        'SELECT id, name, num_in_stock, description'
        ' FROM item WHERE id = ?',
        (id,)
    ).fetchone()

    if item is None:
        abort(404, f"Item with id {id} doesn't exist.")

    if request.method == 'POST':
        num_in_stock = request.form.get('num_in_stock')
        description = request.form.get('description')

        error = None
        if not num_in_stock:
            num_in_stock = 0
        elif not num_in_stock.isdigit():
            error = 'Number of items in stock must be a non-negative integer'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE item SET num_in_stock = ?, description = ?'
                ' WHERE id = ?',
                (num_in_stock, description, id)
            )
            db.commit()
            return redirect(url_for('item.index'))

    return render_template('item/update.html', item=item)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    db = get_db()
    db.execute('DELETE FROM item WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('item.index'))


@bp.route('/export')
def export():
    db = get_db()
    items = db.execute(
        'SELECT name, num_in_stock, description'
        ' FROM item ORDER BY id ASC'
    ).fetchall()

    def generate():
        data = StringIO()
        w = csv.writer(data)

        w.writerow(('name', 'number in stock', 'description'))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        for item in items:
            w.writerow((item[0], item[1], item[2]))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    response = Response(generate(), mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename="inventory.csv")
    return response
