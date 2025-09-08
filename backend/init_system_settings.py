#!/usr/bin/env python3
"""
系统设置初始化脚本
用于在数据库中插入默认的系统设置数据
"""

from app import create_app, db
from models.system_setting import SystemSetting

def init_system_settings():
    """初始化系统设置"""
    app = create_app()
    
    with app.app_context():
        try:
            # 检查是否已经存在联系客服内容设置
            existing_contact_setting = SystemSetting.query.filter_by(key='contact_content').first()

            if not existing_contact_setting:
                # 创建默认的联系客服内容
                default_contact_content = """如需帮助，请通过以下方式联系我们：

📧 邮箱：support@example.com
💬 微信：zepp_support
⏰ 服务时间：9:00-18:00

我们会尽快为您解答！"""

                contact_setting = SystemSetting(
                    key='contact_content',
                    value=default_contact_content,
                    description='联系客服弹窗显示内容'
                )

                db.session.add(contact_setting)
                print("✅ 默认联系客服内容已创建")
            else:
                print("ℹ️  联系客服内容设置已存在，跳过创建")

            # 检查是否已经存在首页公告设置
            existing_announcement_setting = SystemSetting.query.filter_by(key='home_announcement').first()

            if not existing_announcement_setting:
                # 创建默认的首页公告内容
                default_announcement = "欢迎使用Zepp步数修改工具！本工具完全免费，支持微信运动步数同步。如有问题请联系客服。祝您使用愉快！"

                announcement_setting = SystemSetting(
                    key='home_announcement',
                    value=default_announcement,
                    description='首页公告内容'
                )

                db.session.add(announcement_setting)
                print("✅ 默认首页公告内容已创建")
            else:
                print("ℹ️  首页公告内容设置已存在，跳过创建")

            db.session.commit()
                
        except Exception as e:
            print(f"❌ 初始化系统设置失败: {e}")
            db.session.rollback()

if __name__ == '__main__':
    init_system_settings()
