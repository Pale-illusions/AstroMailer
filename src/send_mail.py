import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import requests
from translate import translate_to_chinese
from fetch_nasa import fetch_nasa_apod
import os
from diskcache import Cache
from ci_ba import get_ciba


CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
cache = Cache(CACHE_DIR)
cache_key = "mail"

def get_cached_info():
    """获取缓存的今日邮件信息"""
    
    if cache_key in cache:
        print("使用缓存邮件信息")
        return cache[cache_key]
    # 不存在缓存则返回 None
    return None


def send_email(config):
    """发送邮件，附带 NASA 图片和描述"""    

    msg = get_cached_info()

    if not msg:
        # 获取 NASA 数据
        apod_data = fetch_nasa_apod(api_key=config["api_key"]["nasa"])   

        # 调用百度翻译 API 翻译 APOD 描述
        BAIDU_TRANSLATE_APPID = config["api_key"]["baidu_translate"]["appid"]
        BAIDU_TRANSLATE_SECRET_KEY = config["api_key"]["baidu_translate"]["secret_key"]
        translated_description = translate_to_chinese(apod_data["explanation"], BAIDU_TRANSLATE_APPID, BAIDU_TRANSLATE_SECRET_KEY)

        # 调用词霸 API 获取每日金句
        note_ch, note_en = get_ciba()

        # 构建邮件内容
        msg = MIMEMultipart()
        msg["From"] = config["email"]["sender"]
        msg["To"] = ", ".join(config["email"]["recipients"])
        msg["Subject"] = "🌅 NASA Astronomy Picture of the Day"

        # 添加早安文案和图片描述
        body = f"""
        {config['morning_message']}
        <br><br>
        <b>NASA Astronomy Picture of the Day:</b><br>
        <b>Title:</b> {apod_data["title"]}<br>
        <b>{note_en}<br>
        <b>{note_ch}<br>
        <b>Description (English):</b> {apod_data["explanation"]}<br>
        <b>Description (中文):</b> {translated_description}<br>
        """
        msg.attach(MIMEText(body, "html"))

        # 添加图片
        if "url" in apod_data and apod_data["url"].endswith((".jpg", ".png")):
            response = requests.get(apod_data["url"])
            img = MIMEImage(response.content)
            img.add_header("Content-Disposition", "attachment", filename="apod.jpg")
            msg.attach(img)

        # 添加缓存，有效期 12 小时
        cache.set(cache_key, msg, expire=12 * 60 * 60)

    # 发送邮件
    with smtplib.SMTP(config["email"]["smtp_server"], config["email"]["smtp_port"]) as server:
        server.starttls()
        server.login(config["email"]["sender"], config["email"]["password"])
        server.sendmail(config["email"]["sender"], config["email"]["recipients"], msg.as_string())
    print("邮件发送成功!")