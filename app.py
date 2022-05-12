# -*- coding: utf-8 -*-
import os
import json
from flask import Flask, request
from flask import render_template

from models.git_local.git_command import GitCommand
from models.git_local.git_data import ConvertDict

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
convert_dict = ConvertDict()

repo = GitCommand("seladb", "StarTrack-js")
# repo.clone()
repo.git_data.get_git_path()
repo.numstat()
convert_dict.git_data = repo.git_data
convert_dict.get_path_dict()
json_path = os.path.join('output', repo.owner)
json_name = repo.repo_name
convert_dict.output_dict(json_path, json_name)