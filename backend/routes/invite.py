from flask import Blueprint, request, session, jsonify
from models.user import User
from models.invite_record import InviteRecord

invite_bp = Blueprint('invite', __name__)

@invite_bp.route('/code')
def get_invite_code():
    """获取用户的邀请码"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401

    user = User.query.filter_by(openid=openid).first()
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    return jsonify({
        'invite_code': user.invite_code,
        'invite_url': f"{request.host_url}invite/{user.invite_code}"
    })

@invite_bp.route('/history')
def get_invite_history():
    """获取邀请历史"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401

    records = InviteRecord.get_inviter_records(openid)

    return jsonify({
        'records': [record.to_dict() for record in records],
        'total_count': len(records),
        'total_reward_days': sum(record.reward_days for record in records)
    })