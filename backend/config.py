import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'

    # 数据库配置
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or '43.134.117.111'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'zeppdb'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'Chjwudi008...'
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'zeppdb'

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }

    # 微信配置
    WECHAT_APPID = os.environ.get('WECHAT_APPID') or 'wx5ddf555eced7c5d5'
    WECHAT_APPSECRET = os.environ.get('WECHAT_APPSECRET') or '9f9a7adc3d1d6bafcc43531d010b08e8'
    WECHAT_CALLBACK_HOST = os.environ.get('WECHAT_CALLBACK_HOST') or 'https://bs.7777c.cn'

    # 微信支付配置
    WECHAT_PAY_MCHID = os.environ.get('WECHAT_PAY_MCHID') or '1615814219'
    WECHAT_PAY_API_KEY = os.environ.get('WECHAT_PAY_API_KEY') or '50f3ad7faed588ea7b951cb63267b630'
    WECHAT_PAY_CERT_PATH = os.environ.get('WECHAT_PAY_CERT_PATH') or 'certs/apiclient_cert.pem'
    WECHAT_PAY_KEY_PATH = os.environ.get('WECHAT_PAY_KEY_PATH') or 'certs/apiclient_key.pem'
    WECHAT_PAY_NOTIFY_URL = os.environ.get('WECHAT_PAY_NOTIFY_URL') or 'http://bs.7777c.cn/api/donation/payment-callback'

    # Zepp API配置
    ZEPP_API_URL = os.environ.get('ZEPP_API_URL') or 'https://run.233ka.xyz/zepp_step'
    ZEPP_BIND_CHECK_URL = os.environ.get('ZEPP_BIND_CHECK_URL') or 'https://weixin.amazfit.com/v1/info/users.json'

    # 系统配置
    FREE_TRIAL_DAYS = int(os.environ.get('FREE_TRIAL_DAYS') or 5)
    INVITE_REWARD_DAYS = int(os.environ.get('INVITE_REWARD_DAYS') or 3)
    MAX_STEPS = int(os.environ.get('MAX_STEPS') or 98800)
    MIN_STEPS = int(os.environ.get('MIN_STEPS') or 1)

    # 管理员OpenID列表
    ADMIN_OPENIDS = [
        'oANc3vuHflVjbW9RRKLhBpSdr62I'
    ]

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    WECHAT_CALLBACK_HOST = 'http://bs.7777c.cn'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    WECHAT_CALLBACK_HOST = 'http://bs.7777c.cn'

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}