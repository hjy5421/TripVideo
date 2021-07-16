from googleapiclient.discovery import build
from pymongo import MongoClient

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyAlgG1vbXRaP5Oeqx3YgewDA1MizWcoW3A"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

client = MongoClient('localhost', 27017)
db = client.dbsparta

def youtube_search(country):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=country, #검색할 내용
    part="id,snippet",
    type="video"
  ).execute()

  for search_result in search_response.get("items", []):
    title=search_result["snippet"]["title"];
    url="www.youtube.com/watch?v="+search_result["id"]["videoId"];
    img_url=search_result["snippet"]["thumbnails"]["default"]["url"];
    desc=search_result["snippet"]["description"]
    # print(title+' '+url+' '+img_url+' '+desc)

    doc = {
      'title': title,
      'desc' : desc,
      'img_url': img_url,
      'url': url
    }

    db.tripvideo.insert_one(doc)
    print('완료!', title)

def tour_country():
  countries=["일본 여행","대만 여행","중국 여행","미국 여행","영국 여행","프랑스 여행"]
  for country in countries:
    print(country)
    youtube_search(country)

#실행
tour_country()