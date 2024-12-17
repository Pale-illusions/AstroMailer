import hashlib
import requests
import yaml


def translate_to_chinese(text: str, BAIDU_TRANSLATE_APPID: str, BAIDU_TRANSLATE_SECRET_KEY: str) -> str:
    """
    使用百度翻译 API 将英文翻译为中文
    """
    url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    salt = "12345"  # 随机数
    sign = hashlib.md5(f"{BAIDU_TRANSLATE_APPID}{text}{salt}{BAIDU_TRANSLATE_SECRET_KEY}".encode()).hexdigest()

    params = {
        "q": text,
        "from": "en",
        "to": "zh",
        "appid": BAIDU_TRANSLATE_APPID,
        "salt": salt,
        "sign": sign
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        result = response.json()
        if "trans_result" in result:
            return result["trans_result"][0]["dst"]  # 返回翻译结果
        else:
            raise Exception(f"Error in translation response: {result}")
    else:
        raise Exception(f"Error in API call: {response.status_code} {response.text}")