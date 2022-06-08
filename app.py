# -*- coding: utf-8 -*-
import re
import os
import json
import time
from pprint import pprint
import requests
from flask import Flask, request
from flask import render_template
from models.repo_chart import RepoChart


app = Flask(__name__, template_folder='templates', static_folder='static')
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'
print('Waiting......')


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    repo_name = request.args.get('repo')
    if repo_name:
        return render_template(
            'index.html',
            repo=repo_name
        )
    else:
        return render_template(
            'index.html',
            repo='Uahh/RepoChart'
        )


@app.route('/start', methods=["GET", "POST"])
def start():
    repo_name = request.args.get('repo')
    if repo_name == 'undefined':
        repo_name = 'Uahh/RepoChart'
    if not re.match(".+/.+", repo_name):
        return 'Not existence'
    repo_name = repo_name.split('/')
    repo = RepoChart(repo_name[0], repo_name[1], server=True)
    if repo.existence_flag == False:
        return 'Not existence'
    elif repo.large_flag == True:
        return 'Large'
    elif repo.chart_status == False:
        repo.output()
    return 'OK'


@app.route('/check', methods=["POST"])
def check():
    repo_name = request.form.get('repo')
    if not re.match(".+/.+", repo_name):
        return 'Not existence'
    status = RepoChart.check_output('', repo_name)
    if status == True:
        return {'status': 'True'}
    return {'status': 'False'}


@app.route('/chartdata', methods=["POST"])
def chart_data():
    type = request.form.get('type')
    repo_name = request.form.get('repo')
    if type == 'circle':
        return RepoChart.open_all_charts('', 'circle', repo_name)
    elif type == 'square':
        return RepoChart.open_all_charts('', 'square', repo_name)
    elif type == 'commit_pie':
        return RepoChart.open_all_charts('', 'commit_pie', repo_name)
    elif type == 'commit_line':
        return RepoChart.open_all_charts('', 'commit_line', repo_name)
    elif type == 'star_line':
        return RepoChart.open_all_charts('', 'star_line', repo_name)
    return 'error'


@app.route('/error')
def error():
    return '404 not found'


app.run(host='0.0.0.0', debug=False, port=173)  # inami

# start = time.time()

# repo = RepoChart('Uahh', 'RepoChart', True)
# repo.output()

# end = time.time() - start
# print (str(end))
