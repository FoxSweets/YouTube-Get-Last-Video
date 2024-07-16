from googleapiclient.discovery import build
import re
import time

api_key = "YOUR-API"  # Вставьте ваш API-ключ
youtube = build('youtube', 'v3', developerKey=api_key)


def extract_channel_id(channel_url):
    match = re.search(r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:@|channel\/|user\/)?([a-zA-Z0-9_-]+)', channel_url)
    if match:
        return match.group(1)
    return channel_url


def get_channel_id(channel_url):
    channel_id = extract_channel_id(channel_url)
    if channel_id.startswith('UC'):
        return channel_id

    request = youtube.channels().list(
        part="id",
        forHandle=channel_id
    )
    response = request.execute()
    if 'items' in response and response['items']:
        return response['items'][0]['id']
    print(response)

    raise ValueError(f"Такого канала нету: '{channel_id}'")


def get_channel_name(channel_id):
    request = youtube.channels().list(
        part="snippet",
        id=channel_id
    )
    response = request.execute()
    return response['items'][0]['snippet']['title']


def get_latest_video_id(channel_id):
    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        maxResults=1,
        order="date"
    )
    response = request.execute()
    return response['items'][0]['id']['videoId']


def get_video_details(video_id):
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()
    return response['items'][0]['snippet']['title']


# https://www.youtube.com/channel/UCUw8qO5MuGBRbaZxlySRLAA
list_channel = ['@FoxSweets', '@alaskapine']  # ники или ссылки на ютюб канал
for channel_url in list_channel:
    try:
        print(channel_url)
        channel_id = get_channel_id(channel_url)
        channel_name = get_channel_name(channel_id)
        video_id = get_latest_video_id(channel_id)
        video_details = get_video_details(video_id)
        print(f"Название канала: {channel_name}")
        print(f"Видео: {video_details} | https://youtu.be/{video_id}")
        print("-------------------------------------------------------")
        time.sleep(1)
    except Exception as e:
        print(e)
