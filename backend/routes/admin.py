from flask import Blueprint, session, jsonify, request
from models.system_setting import SystemSetting
from database import db
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """管理员权限装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        openid = session.get('openid')
        if not openid:
            return jsonify({'error': '未登录'}), 401

        # 简单的管理员检查（实际应该查询管理员表）
        # 这里暂时允许所有用户访问，实际项目中应该有管理员表
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/status')
def admin_status():
    """管理员状态检查"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401

    # 简单的管理员检查（实际应该查询管理员表）
    return jsonify({
        'is_admin': True,  # 暂时允许所有用户访问
        'message': '管理员功能正在开发中'
    })

@admin_bp.route('/system-settings/contact-content', methods=['GET'])
def get_contact_content():
    """获取联系客服弹窗内容"""
    try:
        content = SystemSetting.get_setting('contact_content', '')
        return jsonify({
            'success': True,
            'content': content
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/system-settings/contact-content', methods=['POST'])
@admin_required
def set_contact_content():
    """设置联系客服弹窗内容"""
    try:
        data = request.get_json()
        content = data.get('content', '')

        SystemSetting.set_setting(
            'contact_content',
            content,
            '联系客服弹窗显示内容'
        )

        return jsonify({
            'success': True,
            'message': '联系客服内容设置成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/system-settings/home-announcement', methods=['GET'])
def get_home_announcement():
    """获取首页公告内容"""
    try:
        content = SystemSetting.get_setting('home_announcement', '')
        return jsonify({
            'success': True,
            'content': content
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/system-settings/home-announcement', methods=['POST'])
@admin_required
def set_home_announcement():
    """设置首页公告内容"""
    try:
        data = request.get_json()
        content = data.get('content', '')

        SystemSetting.set_setting(
            'home_announcement',
            content,
            '首页公告内容'
        )

        return jsonify({
            'success': True,
            'message': '首页公告内容设置成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/system-settings', methods=['GET'])
@admin_required
def get_system_settings():
    """获取所有系统设置"""
    try:
        settings = SystemSetting.query.all()
        return jsonify({
            'success': True,
            'settings': [setting.to_dict() for setting in settings]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500