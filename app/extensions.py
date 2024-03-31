from pymongo import MongoClient


class MongoDBConnector:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['github_events']
        self.push_events = self.db['push_events']
        self.pull_request_events = self.db['pull_request_events']
        self.merge_events = self.db['merge_events']

    def insert_push_event(self, data):
        self.push_events.insert_one(data)

    def insert_pull_request_event(self, data):
        self.pull_request_events.insert_one(data)

    def insert_merge_event(self, data):
        self.merge_events.insert_one(data)
