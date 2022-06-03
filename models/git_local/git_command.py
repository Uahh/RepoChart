import os
import sys
import git
import copy
import shutil
from threading import Thread
from multiprocessing import cpu_count

sys.path.append(sys.path[0] + '/..')
from models.common.run_command import run_command
from models.github.github_api import GithubStarApi
from models.git_local.git_data import GitData

class GitCommand():
    def __init__(self, owner, repo_name) -> None:
        self.owner = owner
        self.repo_name = repo_name
        self.user_dir = os.path.join('repo_cache', self.owner)
        self.repo_dir = os.path.join(self.user_dir, self.repo_name)
        self.git_data = GitData(self.repo_dir)
        self.git_data.repo_name = owner + '/' + repo_name

    def clone(self):
        git_url = "https://github.com/{}/{}.git".format(self.owner, self.repo_name)

        if not os.path.exists(self.user_dir):
            os.mkdir(self.user_dir)

        if os.path.exists(self.repo_dir):
            print('Already existing Directory! Nice!')
            return
            # print('Already existing Directory, will delete...')
            # shutil.rmtree(self.repo_dir, onerror=self.onerror)
            # print('delete succeed!')

        fail_count = 3
        while(fail_count):
            try:
                git.Git(self.user_dir).clone(git_url)
            except:
                fail_count -= 1
                print("Failed to clone, try again...")
            break

        if not fail_count:
            raise('Failed to clone 3 times, g')
        print('clone successed!')
        self.git_data.get_git_path()
    
    def get_file_commits_info(self):
        for i in range(0 ,len(self.git_data.path_list)):
            file_name = ''
            for dir in self.git_data.path_list[i].split('/')[3:]:
                file_name = os.path.join(file_name, dir)
            file_name = file_name.replace('\\', '/')
            self.git_data.path_list[i] = '/' + file_name + '/'
            # cmd = "cd {} && git log --numstat {}".format(self.repo_dir, file_name)
            # commit_log = run_command(cmd)
            commit_log = git.Git(self.repo_dir).log('--numstat', '--shortstat', file_name)
            commit_conut = 0
            lines_conut = 0
            for line in commit_log.splitlines():
                if line:
                    if line[0:6] == 'commit':
                        commit_conut += 1
                    if line[0:5] == 'Author':
                        pass
                    if line[0].isdigit():
                        lines_conut += int(line.split('\t')[0]) + int(line.split('\t')[1])
            self.git_data.commits_list.append(commit_conut)
            self.git_data.lines_list.append(lines_conut)

    def get_file_size_from_every_commit(self):
        # git rev-list HEAD -- data\language.json
        self.commit_list = git.Git(self.repo_dir).rev_list('HEAD').split('\n')
    #     core_count = cpu_count() * 2
    #     thread_num = len(self.commit_list) // core_count
    #     index = 0
    #     thread_list = []
    #     for i in range(0, core_count):
    #         temp_thread = Thread(target=self.thread_ls_tree, args=(index, index + thread_num))
    #         index += thread_num
    #         thread_list.append(temp_thread)

    #     for i in range(0, core_count):
    #         thread_list[i].start()

    #     for i in range(0, core_count):
    #         thread_list[i].join()

    # def thread_ls_tree(self, begin, end):
        for i in range(0, len(self.commit_list)):
            commit_log = git.Git(self.repo_dir).ls_tree('-r', '-l', self.commit_list[i]).split('\n')
            for log in commit_log:
                inc = log.split('\t')[0].split(' ')[-1]
                if not inc.isdigit():
                    continue
                current_size = int(inc)
                file_name = log.split('\t')[-1]
                file_suffix = '.' + file_name.split('.')[-1]

                if file_suffix in self.git_data.file_suffix.keys():
                    self.git_data.file_suffix[file_suffix] = current_size

            for line in self.git_data.commit_line_list:
                    inc = self.git_data.file_suffix[line['name']]
                    line['data'].append(inc)

            if i == 0:
                for line in self.git_data.commit_line_list:
                    temp = copy.deepcopy(self.git_data.first_commit_template)
                    temp['value'] = line['data'][0]
                    temp['name'] = line['name']
                    temp['itemStyle']['color'] = self.git_data.get_color(line['name'][1:])
                    self.git_data.first_commit_size.append(temp)
        # for line in self.git_data.commit_line_list:
        #     line['data'].reverse()

    def get_all_chart_data(self):
        self.clone()
        self.git_data.get_git_path()
        self.get_file_commits_info()
        self.get_file_size_from_every_commit()

    # Error handler for shutil.rmtree().
    def onerror(self, func, path, exc_info):
        import stat
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise("shutil.rmtree() failed, maybe the file is in opened")
