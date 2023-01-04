from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from dotenv import load_dotenv
import os

# load .env
load_dotenv()

from pymongo import MongoClient
import certifi

mongoDB = os.environ.get('mongoDB_URL')
ca = certifi.where()
client = MongoClient(mongoDB,
                     tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    # 목록들을 카운트 하기 위해서 모든 목록을 불러온 후 count한 뒤 +1을 한 값을 DB에 저장
    bucket_list = list(db.buckets.find({}, {'_id': False}))
    count = len(bucket_list) + 1

    doc = {
        'num': count,
        'bucket': bucket_receive,
        'done': 0
    }
    db.buckets.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.buckets.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '버킷 완료!'})


@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.buckets.find({}, {'_id': False}))
    return jsonify({'buckets': bucket_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
