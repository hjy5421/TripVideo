from flask import Flask, render_template, jsonify, request
from googleapiclient.discovery import build
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/video', methods=['POST'])
def write_videos():
    title_receive = request.form['title_give']

    db.tripvideo.drop();
    ##youtube 검색
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=title_receive,  # 검색할 내용
        part="id,snippet",
        type="video"
    ).execute()

    for search_result in search_response.get("items", []):
        title = search_result["snippet"]["title"];
        url = "https://www.youtube.com/watch?v=" + search_result["id"]["videoId"];
        img_url = search_result["snippet"]["thumbnails"]["high"]["url"];
        desc = search_result["snippet"]["description"]
        # print(title+' '+url+' '+img_url+' '+desc)

        doc = {
            'title': title,
            'desc': desc,
            'img_url': img_url,
            'url': url
        }

        db.tripvideo.insert_one(doc)

    return jsonify({'msg': '저장 완료'})


@app.route('/video', methods=['GET'])
def read_videos():
    videos = list(db.tripvideo.find({}, {'_id': False}))
    return jsonify({'all_videos': videos})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
