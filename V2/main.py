from googleapiclient.discovery import build
import re
import time

# Вставьте ваш API-ключ
api_key = 'None'
youtube = build('youtube', 'v3', developerKey=api_key)


def extract_channel_id(channel_url):
    # Регулярное выражение для извлечения идентификатора канала из URL
    match = re.search(r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:@|channel\/|user\/)?([a-zA-Z0-9_-]+)', channel_url)
    if match:
        return match.group(1)
    return channel_url  # Возвращаем как есть, если это идентификатор канала


def get_channel_id(channel_url):
    channel_id = extract_channel_id(channel_url)
    if channel_id.startswith('UC'):
        return channel_id

    # Если это URL канала или имя пользователя, получаем ID канала
    request = youtube.channels().list(
        part="id",
        forHandle=channel_id
    )
    response = request.execute()
    if 'items' in response and response['items']:
        return response['items'][0]['id']

    # Если ни одно из вышеуказанных условий не сработало
    raise ValueError(f"[ОШИБКА]: Айди или имя канала '{channel_id}' не найдено!\n----------\n")


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


def main():
    # Собираем из папки "youtubers.txt" все имена пользователей через @
    with open("youtubers.txt", "r", encoding="UTF-8") as file:
        lines = [line.strip() for line in file]

    with open('videos.txt', 'w', encoding='UTF-8') as write_file:
        for channel_url in lines:
            try:
                print("----------")
                print(channel_url)
                channel_id = get_channel_id(channel_url)
                channel_name = get_channel_name(channel_id)
                video_id = get_latest_video_id(channel_id)
                video_details = get_video_details(video_id)
                text = '-------------------------------------------------------\n' + f'Канал: {channel_name} | https://www.youtube.com/{channel_url}\n' + f'Видео: {video_details} | https://youtu.be/{video_id}\n' + '-------------------------------------------------------\n\n'
                print("[ГОТОВО]")
                print("----------\n")

                write_file.write(text)

                time.sleep(1)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()
