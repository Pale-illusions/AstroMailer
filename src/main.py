import schedule
import time
import os
from send_mail import send_email
import yaml

def load_config():
    """加载 YAML 配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), "resources/config.yaml")
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def job():
    """发送邮件任务"""
    config = load_config()
    send_email(config)
    print("早安邮件已发送!")

def main():
    # 每天早上 8 点执行任务
    schedule.every().day.at("08:00").do(job)

    print("定时任务已启动，等待发送早安邮件...")
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次

if __name__ == "__main__":
    main()