from flask import Flask, jsonify, request
import json
from datetime import datetime
from mongodb_connector.mongodb import MongoDBConnector


app = Flask(__name__)
mongo = MongoDBConnector()


@app.route('/webhook', methods=['POST'])
def receive_webhook():
    data = request.json
    action = data['action']
    timestamp = datetime.now().strftime('%d %B %Y - %I:%M %p UTC')

    if action == 'push':
        payload = {
            'author': data['pusher']['name'],
            'to_branch': data['ref'].split('/')[-1],
            'timestamp': timestamp
        }
        mongo.insert_push_event(payload)
    elif action == 'pull_request':
        payload = {
            'author': data['sender']['login'],
            'from_branch': data['pull_request']['head']['ref'],
            'to_branch': data['pull_request']['base']['ref'],
            'timestamp': timestamp
        }
        mongo.insert_pull_request_event(payload)
    elif action == 'merge':
        payload = {
            'author': data['sender']['login'],
            'from_branch': data['pull_request']['head']['ref'],
            'to_branch': data['pull_request']['base']['ref'],
            'timestamp': timestamp
        }
        mongo.insert_merge_event(payload)

    return 'Webhook received successfully'


@app.route('/get_events', methods=['GET'])
def get_events():
    events = mongo.get_all_events()
    return jsonify(events)


if __name__ == '__main__':
    app.run(debug=True)
