from flask import Blueprint, session, jsonify
from models.user import User
from models.zepp_account import ZeppAccount

zepp_bp = Blueprint('zepp', __name__)

@zepp_bp.route('/bind-status')
def check_bind_status():
    """检查Zepp账号绑定状态"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401

    # 获取用户绑定的Zepp账号
    zepp_account = ZeppAccount.get_user_account(openid)

    if zepp_account and zepp_account.bind_status:
        return jsonify({
            'bind_status': True,
            'username': zepp_account.username,
            'message': '已绑定Zepp账号'
        })
    else:
        return jsonify({
            'bind_status': False,
            'message': '未绑定Zepp账号'
        })

@zepp_bp.route('/qrcode')
def get_qr_code():
    """获取绑定二维码"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401

    # 检查是否已经绑定
    zepp_account = ZeppAccount.get_user_account(openid)
    if zepp_account and zepp_account.bind_status:
        return jsonify({
            'error': '已绑定Zepp账号',
            'bind_status': True
        }), 400

    # 获取可用的Zepp账号
    if not zepp_account:
        available_account = ZeppAccount.get_available_account()
        if not available_account:
            return jsonify({
                'error': '暂无可用的Zepp账号，请稍后重试'
            }), 503

        # 分配账号给用户
        available_account.bind_to_user(openid)
        from database import db
        db.session.commit()
        zepp_account = available_account

    return jsonify({
        'qr_code_url': zepp_account.qr_code_url or 'https://via.placeholder.com/200x200?text=QR+Code',
        'username': zepp_account.username,
        'message': '请扫描二维码完成绑定'
    })