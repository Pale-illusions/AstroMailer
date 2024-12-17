import requests

def get_ciba():
    """调用词霸 API 获取每日金句"""

    url = "https://open.iciba.com/dsapi/"
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    note_en = data["content"] # 英文
    note_ch = data["note"] # 中文

    return note_ch, note_en


