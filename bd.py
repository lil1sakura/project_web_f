import os
import sqlite3
from flask import Flask, render_template, request, g, flash, abort
from FDataBase import FDataBase

database = '/tmp/bd.db'
debug = True
secret_key = 'yandexlyceum_secret_key'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(database=os.path.join(app.root_path, 'bd.db')))


def connect_bd():
    conn = sqlite3.connect(app.config['database'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_bd()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'bd.db'):
        g.bd_db = connect_bd()
    return g.bd_db





