import os
import sys
import git
import shutil

sys.path.append(sys.path[0] + '/..')

from common.run_command import run_command

class GitCommand():
    def __init__(self, owner, repo) -> None:
        self.owner = owner
        self.repo = repo

    def clone(self):
        git_url = "https://github.com/{}/{}.git".format(self.owner, self.repo)
        user_dir = "repo_cache/{}".format(self.owner)

        if not os.path.exists(user_dir):
            os.mkdir(user_dir)

        repo_dir = os.path.join(user_dir, self.repo)
        if os.path.exists(repo_dir):
            print('Already existing Directory, will delete...')
            shutil.rmtree(repo_dir, onerror=self.onerror)

        fail_count = 3
        while(fail_count):
            try:
                git.Git(user_dir).clone(git_url)
            except:
                fail_count -= 1
                print("Failed to clone, try again...")
            break

        if not fail_count:
            raise('Failed to clone 3 times, g')
        print('clone successed!')

    # Error handler for shutil.rmtree().
    def onerror(self, func, path, exc_info):
        import stat
        # Is the error an access error?
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise

git_command = GitCommand('Uahh', 'Fyzhq')
git_command.clone()