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
        msg["From"] = "苍镜月"
        msg["To"] = ", ".join(config["email"]["recipients"])
        msg["Subject"] = "🌅 你有一份来自 NASA 的浪漫早安，请查收~"

        # 添加早安文案和图片描述
        body = f"""
            <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            margin: 0;
                            padding: 20px;
                            background-color: #f4f4f9;
                            color: #333;
                        }}
                        h1 {{
                            color: #2e6c80;
                        }}
                        p {{
                            margin: 10px 0;
                        }}
                        .container {{
                            background: #fff;
                            border-radius: 8px;
                            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                            padding: 20px;
                            margin: 20px auto;
                            max-width: 700px;
                        }}
                        .image-container {{
                            text-align: center;
                            margin-top: 20px;
                        }}
                        .image-container img {{
                            max-width: 100%;
                            border-radius: 8px;
                            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
                        }}
                        .note {{
                            font-style: italic;
                            color: #555;
                            margin-top: 10px;
                        }}
                        .highlight {{
                            font-weight: bold;
                            color: #1f5f8b;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>{config['morning_message']}</h1>
                        <p class="highlight">🌌 NASA Astronomy Picture of the Day:</p>
                        <p><b>Title:</b> {apod_data["title"]}</p>
                        
                        <div class="note">
                            <p>{note_en}</p>
                            <p>{note_ch}</p>
                        </div>
                        
                        <p><b>Description (English):</b></p>
                        <p>{apod_data["explanation"]}</p>
                        
                        <p><b>Description (中文):</b></p>
                        <p>{translated_description}</p>

                        <div class="image-container">
                            <img src="{apod_data['url']}" alt="NASA Astronomy Picture of the Day">
                        </div>
                    </div>
                </body>
            </html>
        """
        msg.attach(MIMEText(body, "html"))

        # 添加图片
        # if "url" in apod_data and apod_data["url"].endswith((".jpg", ".png")):
        #     response = requests.get(apod_data["url"])
        #     img = MIMEImage(response.content)
        #     img.add_header("Content-Disposition", "attachment", filename="apod.jpg")
        #     msg.attach(img)

        # 添加缓存，有效期 12 小时
        cache.set(cache_key, msg, expire=12 * 60 * 60)

    # 发送邮件
    with smtplib.SMTP(config["email"]["smtp_server"], config["email"]["smtp_port"]) as server:
        server.starttls()
        server.login(config["email"]["sender"], config["email"]["password"])
        server.sendmail(config["email"]["sender"], config["email"]["recipients"], msg.as_string())
    print("邮件发送成功!")