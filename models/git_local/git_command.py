import os
import sys
import git
import copy
import requests
from threading import Thread
from multiprocessing import cpu_count

sys.path.append(sys.path[0] + '/..')
from models.common.run_command import run_command
from models.git_local.git_data import GitData


class GitCommand():
    def __init__(self, git_data) -> None:
        self.git_data = git_data
        self.repo_name = self.git_data.owner + '/' + self.git_data.repo_name

    def clone(self):
        git_url = "https://github.com/{}/{}.git".format(self.git_data.owner, self.git_data.repo_name)

        if not os.path.exists('repo_cache'):
            os.mkdir('repo_cache')
        if not os.path.exists(self.git_data.user_dir):
            os.mkdir(self.git_data.user_dir)

        if os.path.exists(self.git_data.repo_dir):
            print('Already existing Directory, Nice!')
            return
            # print('Already existing Directory, will delete...')
            # shutil.rmtree(self.repo_dir, onerror=self.onerror)
            # print('delete succeed!')

        fail_count = 10
        while(fail_count):
            try:
                print("trying clone...")
                git.Git(self.git_data.user_dir).clone(git_url)
                break
            except:
                fail_count -= 1
                print("Failed to clone, try again...")

        if not fail_count:
            raise('Failed to clone 10 times, g')
        print('clone successed!')
        self.git_data.get_git_path()
    
    def get_file_commits_info(self):
        print('Start looking at the number of commits each file...')
        for i in range(0 ,len(self.git_data.path_list)):
            file_name = ''
            for dir in self.git_data.path_list[i].split('/')[3:]:
                file_name = os.path.join(file_name, dir)
            file_name = file_name.replace('\\', '/')
            self.git_data.path_list[i] = '/' + file_name + '/'
            # cmd = "cd {} && git log --numstat {}".format(self.repo_dir, file_name)
            # commit_log = run_command(cmd)
            commit_log = git.Git(self.git_data.repo_dir).log('--numstat', '--shortstat', '--date=format:\"%Y-%m-%d\"', file_name)
            commit_sha = ''
            commit_conut = 0
            lines_conut = 0
            for line in commit_log.splitlines():
                if line:
                    if line[0:6] == 'commit':
                        commit_conut += 1
                        commit_sha = line.split(' ')[1].replace('\"', '')
                        if commit_sha not in self.git_data.commit_sha_dict.keys():
                            self.git_data.commit_sha_dict[commit_sha] = 0
                    if line[0:5] == 'Author':
                        pass
                    if line[0:4] == 'Date':
                        if self.git_data.commit_sha_dict[commit_sha] == 0:
                            date = line.split('   ')[1].replace('\"', '')
                            self.git_data.commit_date_dict[date] = 1
                            self.git_data.commit_sha_dict[commit_sha] = -1
                        else:
                            self.git_data.commit_date_dict[date] += 1
                    if line[0].isdigit():
                        lines_conut += int(line.split('\t')[0]) + int(line.split('\t')[1])
            self.git_data.commits_list.append(commit_conut)
            self.git_data.lines_list.append(lines_conut)

    def get_file_size_from_every_commit(self):
        # git rev-list HEAD -- data\language.json
        print('Start looking at the file size of each commit...')
        self.commit_list = git.Git(self.git_data.repo_dir).rev_list('HEAD').split('\n')
        self.commit_list.reverse()
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
            commit_log = git.Git(self.git_data.repo_dir).ls_tree('-r', '-l', self.commit_list[i]).split('\n')
            temp_file_suffix = copy.deepcopy(self.git_data.file_suffix)
            for log in commit_log:
                inc = log.split('\t')[0].split(' ')[-1]
                if not inc.isdigit():
                    continue
                file_name = log.split('\t')[-1]
                file_suffix = '.' + file_name.split('.')[-1]

                if file_suffix in temp_file_suffix:
                    temp_file_suffix[file_suffix] += int(inc)
                else:
                    continue
            for suffix in self.git_data.file_suffix.keys():
                if temp_file_suffix[suffix] - self.git_data.file_suffix[suffix] != 0:
                    self.git_data.file_suffix[suffix] = temp_file_suffix[suffix] - self.git_data.file_suffix[suffix]

            for line in self.git_data.commit_line_list:
                    inc = self.git_data.file_suffix[line['name']]
                    line['data'].append(inc)

            if i == len(self.commit_list) - 1:
                for line in self.git_data.commit_line_list:
                    temp = copy.deepcopy(self.git_data.first_commit_template)
                    temp['value'] = line['data'][-1]
                    temp['name'] = line['name']
                    temp['itemStyle']['color'] = self.git_data.get_color(line['name'][1:])
                    self.git_data.first_commit_size.append(temp)

    def get_active_line(self):
        for date in self.git_data.commit_date_dict.keys():
            self.git_data.active_chart_list.append([date,  self.git_data.commit_date_dict[date]])

    def get_all_chart_data(self):
        self.clone()
        self.git_data.get_git_path()
        self.get_file_commits_info()
        self.get_file_size_from_every_commit()
        self.get_active_line()

    # Error handler for shutil.rmtree().
    def onerror(self, func, path, exc_info):
        import stat
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise("shutil.rmtree() failed, maybe the file is in opened")
