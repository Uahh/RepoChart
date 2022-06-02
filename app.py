# -*- coding: utf-8 -*-
import os
import json
import time
from pprint import pprint
import requests
from flask import Flask, request
from flask import render_template

from models.repo_chart import RepoChart

app = Flask(__name__, template_folder='templates', static_folder='static')
print('Waiting......')

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    return render_template(
        'index.html'
    )


@app.route('/error')
def error():
    return '404 not found'


# app.run(host='0.0.0.0', debug=False, port=173)  # inami

start = time.time()

repo = RepoChart('Uahh', 'Fyzhq')
repo.output()

end = time.time() - start
print (str(end))