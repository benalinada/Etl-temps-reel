from flask import Flask, render_template, jsonify
from bson import json_util
import json
from pymongo import MongoClient
mongo_host = 'host.docker.internal'
mongo_port = 27017

app = Flask(__name__)
client = MongoClient(f'mongodb://{mongo_host}:{mongo_port}', serverSelectionTimeoutMS=5000)
db = client.Sentiment
collection = db.Tweet_Content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    data = list(collection.find())
    # Convert ObjectId to string
    for item in data:
        item['_id'] = str(item['_id'])
    # Serialize data to JSON
    return json.dumps(data, default=json_util.default)

@app.route('/project_architecture')
def project_architecture():
    return render_template('project_architecture.html')

if __name__ == '__main__':
    app.run(debug=True)
