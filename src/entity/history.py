class History:
    def __init__(self, commit_id, time):
        self.commit_id = commit_id
        self.time = time

    def get_time(self):
        return self.time

    def get_commit_id(self):
        return self.commit_id
