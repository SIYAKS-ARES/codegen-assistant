from s4e.config import *
from s4e.task import Task

class Job(Task):
    def run(self):
        self.output['detail'] = []
        self.output['compact'] = []
        self.output['video'] = []

    def calculate_score(self):
        self.score = self.param['max_score'] 