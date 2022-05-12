import imp
import os
import sys
import git
import shutil

sys.path.append(sys.path[0] + '/..')
from models.common.run_command import run_command
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
            print('Already existing Directory, will delete...')
            shutil.rmtree(self.repo_dir, onerror=self.onerror)
            print('delete succeed!')

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
    
    def numstat(self):
        for i in range(0 ,len(self.git_data.path_list)):
            file_name = ''
            for dir in self.git_data.path_list[i].split('/')[3:]:
                file_name = os.path.join(file_name, dir)
            file_name = file_name.replace('\\', '/')
            self.git_data.path_list[i] = '/' + file_name + '/'
            # cmd = "cd {} && git log --numstat {}".format(self.repo_dir, file_name)
            # commit_log = run_command(cmd)
            commit_log = git.Git(self.repo_dir).log('--numstat', file_name)
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

    # Error handler for shutil.rmtree().
    def onerror(self, func, path, exc_info):
        import stat
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise("shutil.rmtree failed, maybe the file is in opened")
