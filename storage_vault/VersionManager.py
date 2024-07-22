# git manager for vaults directory
import git
class VersionManager:
    def __init__(self,folder):
        self.folder = folder
        self.repo = git.Repo(folder)
        self.repo.git.add(all=True)
    
    def commit(self,message):
        self.repo.git.commit('-m',message)
    
    def viewCommits(self):
        for commit in self.repo.iter_commits():
            print("Commit Hash:",commit.hexsha)
            print("Commit Messages:",commit.message)
            print(" ")

    def revertCommit(self,hash):
        curr_repo = git.Repo(self.folder)
        curr_repo.git.add(all=True)
        curr_repo.git.reset(hash,hard=True)

