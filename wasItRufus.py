import sys
import git
from git import Repo
from datetime import timezone, datetime


def main(git_dir):

    #check if argument has been entered
    if(len(git_dir) != 2) :
        print("Please pass repo directory as an argument!")
        exit(1)

    #check if local directory path is valid
    if(is_valid_dir(git_dir[1])==False):
        print("Invalid directory!")
        exit(1)

    #check if this directory is a git repository
    if(is_valid_git_repo(git_dir[1]) == False):
        print("Invalid Git Respository!")
        exit(1)

    repo = Repo(git_dir[1])
    active_branch = get_active_branch(repo)
    local_changes = is_local_changes(repo)
    recent_commit = is_recent_commit(repo)
    blame_Rufus = is_blame_rufus(repo)

    print("active branch: " + active_branch)
    print("local changes: " + str(local_changes))
    print("recent commit: " + str(recent_commit))
    print("blame Rufus: " + str(blame_Rufus))

    exit(0)

#return the name of the current active branch
def get_active_branch(repo):
    return repo.active_branch.name

#checks for untracked files and returns True if repository has been changed locally
def is_local_changes(repo):
    if(repo.untracked_files):
        return True
    else:
        return False

#checks if any changes have been made locally in the past 7 days
def is_recent_commit(repo):
    headcommit = repo.head.commit
    latest_commit_datetime = headcommit.committed_datetime
    current_datetime = datetime.now(timezone.utc)
    difference = (current_datetime.date()) - (latest_commit_datetime.date())
    if((difference.days) < 7):
        return True
    else:
        return False

#checks if latest commit has been made by username 'Rufus'
def is_blame_rufus(repo):
    if(repo.head.commit.author.name == 'Rufus'):
        return True
    else:
        return False

#helper function to check if git repositiry is valid
def is_valid_git_repo(path):
    try:
        _ = Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False

#helper function to check valid local path 
def is_valid_dir(path):
    try:
        _ = Repo(path).git_dir
        return True
    except git.exc.NoSuchPathError:
        return False

if __name__ == '__main__':
    main(sys.argv)

