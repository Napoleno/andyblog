import os
from dotenv import load_dotenv

from bluelog import create_app

dotenv_path = os.path.join(os.path.dirname(__file__), 'bluelog/.env')
# print(dotenv_path)
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# 应用的入口程序
app = create_app('development')

# 测试使用python-dotenv导入系统环境变量
# print(os.getenv('MAIL_SERVER'))
# print(os.getenv('MAIL_USERNAME'))
# print(os.getenv('MAIL_PASSWORD'))
# print(os.getenv('BLUELOG_EMAIL'))
