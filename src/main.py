import yaml
from send_mail import send_email

def load_config():
    """加载 YAML 配置文件"""
    with open("resources/config.yaml", "r") as file:
        return yaml.safe_load(file)

def main():
    # 加载配置
    config = load_config()

    # 发送邮件
    send_email(config)

if __name__ == "__main__":
    main()