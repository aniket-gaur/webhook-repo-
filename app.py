from flask import Flask, request, jsonify, render_template
from datetime import datetime
from db import events_collection
import pytz


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')



@app.route('/webhook', methods=['POST'])
def webhook():
    event_type = request.headers.get('X-GitHub-Event')
    data = request.json
    ist = pytz.timezone('Asia/Kolkata')
    timestamp = datetime.now(ist)
    formatted_time = timestamp.strftime('%d %B %Y - %I:%M %p IST')

    doc = {
    'timestamp': timestamp
    }


     



    if event_type == 'push':
        doc.update({
            'type': 'push',
            'author': data['pusher']['name'],
            'to_branch': data['ref'].split('/')[-1]
        })

    elif event_type == 'pull_request':
        action = data['action']
        pr = data['pull_request']
        if action == 'opened':
            doc.update({
                'type': 'pull_request',
                'author': pr['user']['login'],
                'from_branch': pr['head']['ref'],
                'to_branch': pr['base']['ref']
            })
        elif action == 'closed' and pr.get('merged'):
            doc.update({
                'type': 'merge',
                'author': pr['user']['login'],
                'from_branch': pr['head']['ref'],
                'to_branch': pr['base']['ref']
            })
        else:
            return '', 204

    else:
        return '', 204

    events_collection.insert_one(doc)
    print(doc)
    return jsonify({"status": "received"}), 200

@app.route('/events', methods=['GET'])
def get_events():
    events = list(events_collection.find().sort('timestamp', -1).limit(10))
    for e in events:
        e['_id'] = str(e['_id'])
        e['timestamp'] = e['timestamp']

    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)
