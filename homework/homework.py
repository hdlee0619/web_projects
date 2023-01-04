from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from dotenv import load_dotenv
import os

# load .env
load_dotenv()
mongoDB = os.environ.get('mongoDB_URL')

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient(mongoDB, tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/homework", methods=["POST"])
def homework_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    doc = {
        'name': name_receive,
        'comment': comment_receive
    }
    db.pan_pages.insert_one(doc)

    return jsonify({'msg': '응원달기 완료!'})


@app.route("/homework", methods=["GET"])
def homework_get():
    comments_list = list(db.pan_pages.find({}, {'_id': False}))
    return jsonify({'comments': comments_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
