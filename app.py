# -*- coding: utf-8 -*-
import re
from optparse import OptionParser
from flask import Flask, request
from flask import render_template
from models.repo_chart import RepoChart
from models.misc.repo_backup import RepoBackup

repo_backup = RepoBackup()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'
print('Waiting...')


@app.route('/repochart', methods=["GET", "POST"])
def index():
    repo_name = request.args.get('repo')
    if repo_name:
        return render_template(
            'index.html',
            repo=repo_name,
        )
    else:
        return render_template(
            'index.html',
            repo='Uahh/RepoChart'
        )


@app.route('/repochart/start', methods=["GET", "POST"])
def start():
    repo_name = request.args.get('repo')
    if repo_name == 'undefined':
        repo_name = 'Uahh/RepoChart'
    if not re.match(".+/.+", repo_name):
        return 'Without'

    repo_status = repo_backup.check_repo(repo_name)
    if repo_status == False:
        repo_name_split = repo_name.split('/')
        # if repo_name not in repo_backup.repo_list:
        repo_backup.add_repo(repo_name)
        repo = RepoChart(repo_name_split[0], repo_name_split[1], server=True)
        if repo == 'Network failed':
            repo_backup.del_repo(repo_name)
            return 'Network failed'
        if repo.chart_status == False:
            repo.output()
        if repo.existence_flag == False:
            repo_backup.add_repo(repo_name, type='Without')
            return 'Without'
        elif repo.large_flag == True:
            repo_backup.add_repo(repo_name, type='Large')
            return 'Large'
        elif repo.star_flag == True:
            repo_backup.add_repo(repo_name, type='Normal')
            return 'Star'
        repo_backup.add_repo(repo_name, type='Normal')
        return 'OK'
    elif repo_status == 'Without':
        return 'Without'
    elif repo_status == 'Large':
        return 'Large'
    else:
        if not RepoChart.check_output('', repo_name):
            return 'Started'
        return 'OK'


@app.route('/repochart/check', methods=["POST"])
def check():
    repo_name = request.form.get('repo')
    if not re.match(".+/.+", repo_name):
        return 'Without'
    status = RepoChart.check_output('', repo_name)
    if status == True:
        return {'status': 'True'}
    return {'status': 'False'}


@app.route('/repochart/chartdata', methods=["POST"])
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
    elif type == 'active_line':
        return RepoChart.open_all_charts('', 'active_line', repo_name)
    elif type == 'star_line':
        return RepoChart.open_all_charts('', 'star_line', repo_name)
    elif type == 'code_of_lines':
        return RepoChart.open_all_charts('', 'code_of_lines', repo_name)
    return 'error'


@app.route('/repochart/error')
def error():
    return '404 not found'


app.run(host='0.0.0.0', debug=False, port=52173)  # 52inami