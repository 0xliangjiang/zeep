import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from config import config
from database import db

def create_app(config_name=None):
    """应用工厂函数"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    CORS(app, 
         supports_credentials=True,
         origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:7000", "http://127.0.0.1:7000", "http://bs.7777c.cn"],
         allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    # 注册蓝图
    from routes.auth import auth_bp
    from routes.steps import steps_bp
    from routes.invite import invite_bp
    from routes.card import card_bp
    from routes.admin import admin_bp
    from routes.zepp import zepp_bp
    from routes.donation import donation_bp
    from routes.zepp_manage import zepp_manage_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(steps_bp, url_prefix='/api/steps')
    app.register_blueprint(invite_bp, url_prefix='/api/invite')
    app.register_blueprint(card_bp, url_prefix='/api/card')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(zepp_bp, url_prefix='/api/zepp')
    app.register_blueprint(donation_bp, url_prefix='/api/donation')
    app.register_blueprint(zepp_manage_bp, url_prefix='/api/zepp-manage')

    # 微信验证文件路由
    @app.route('/MP_verify_i1nJ2GFvXOCnNMak.txt')
    def wechat_verification():
        return send_from_directory('static', 'MP_verify_i1nJ2GFvXOCnNMak.txt')

    # 健康检查
    @app.route('/health')
    def health_check():
        return {'status': 'ok', 'message': 'WechatZepp API is running'}

    # 导入所有模型以确保表被创建
    from models.user import User
    from models.zepp_account import ZeppAccount
    from models.step_record import StepRecord
    from models.invite_record import InviteRecord
    from models.card_key import CardKey
    from models.donation import DonationConfig, DonationOrder
    from models.system_setting import SystemSetting

    # 创建数据库表
    with app.app_context():
        try:
            # 强制创建所有表
            db.create_all()
            print("数据库表创建完成")

            # 检查关键表是否存在
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()

            required_tables = ['card_keys', 'donation_configs', 'donation_orders', 'system_settings']
            for table in required_tables:
                if table in tables:
                    print(f"{table}表创建成功")
                else:
                    print(f"警告: {table}表未创建")

        except Exception as e:
            print(f"创建数据库表时出错: {e}")

    return app

# 创建应用实例供gunicorn使用
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5520, debug=True)