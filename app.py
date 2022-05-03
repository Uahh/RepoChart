# -*- coding: utf-8 -*-
import json
from flask import Flask, request
from flask import render_template

app = Flask(__name__, template_folder='templates', static_folder='static')
print('Waiting......')

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    pass


@app.route('/error')
def error():
    return '404 not found'


app.run(host='0.0.0.0', debug=False, port=173)  # inami