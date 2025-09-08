from flask import Blueprint, request, session, jsonify, current_app
from datetime import datetime, timedelta
from models.card_key import CardKey
from models.user import User
from database import db

card_bp = Blueprint('card', __name__)

# 管理员openid列表
ADMIN_OPENIDS = [
    'oANc3vuHflVjbW9RRKLhBpSdr62I'
]

def is_admin(openid):
    """检查是否为管理员"""
    return openid in ADMIN_OPENIDS

@card_bp.route('/check-admin', methods=['GET'])
def check_admin():
    """检查当前用户是否为管理员"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401

    is_admin_user = is_admin(openid)

    return jsonify({
        'is_admin': is_admin_user,
        'openid': openid if is_admin_user else None
    })

@card_bp.route('/generate', methods=['POST'])
def generate_card_keys():
    """生成卡密"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录', 'need_login': True}), 401

    if not is_admin(openid):
        return jsonify({'error': '权限不足', 'need_logout': True}), 403

    try:
        data = request.get_json()

        # 验证参数
        length = data.get('length', 12)
        if not (6 <= length <= 32):
            return jsonify({'error': '卡密长度必须在6-32位之间'}), 400

        count = data.get('count', 1)
        if not (1 <= count <= 1000):
            return jsonify({'error': '生成个数必须在1-1000之间'}), 400

        days = data.get('days', 1)
        if not (1 <= days <= 3650):
            return jsonify({'error': '天数必须在1-3650之间'}), 400

        # 字符类型设置
        include_numbers = data.get('include_numbers', True)
        include_lowercase = data.get('include_lowercase', True)
        include_uppercase = data.get('include_uppercase', False)
        include_symbols = data.get('include_symbols', False)

        # 至少选择一种字符类型
        if not any([include_numbers, include_lowercase, include_uppercase, include_symbols]):
            return jsonify({'error': '至少选择一种字符类型'}), 400

        # 有效期设置
        expires_at = None
        expire_type = data.get('expire_type')  # minutes, hours, days, weeks, months, years, permanent
        expire_value = data.get('expire_value', 1)

        if expire_type and expire_type != 'permanent':
            now = datetime.utcnow()
            if expire_type == 'minutes':
                expires_at = now + timedelta(minutes=expire_value)
            elif expire_type == 'hours':
                expires_at = now + timedelta(hours=expire_value)
            elif expire_type == 'days':
                expires_at = now + timedelta(days=expire_value)
            elif expire_type == 'weeks':
                expires_at = now + timedelta(weeks=expire_value)
            elif expire_type == 'months':
                expires_at = now + timedelta(days=expire_value * 30)
            elif expire_type == 'years':
                expires_at = now + timedelta(days=expire_value * 365)

        # 批量生成卡密
        keys = CardKey.create_batch(
            count=count,
            days=days,
            length=length,
            include_numbers=include_numbers,
            include_lowercase=include_lowercase,
            include_uppercase=include_uppercase,
            include_symbols=include_symbols,
            expires_at=expires_at,
            created_by=openid
        )

        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'成功生成{count}个卡密',
            'keys': [key.key_code for key in keys],
            'count': len(keys)
        })

    except Exception as e:
        db.session.rollback()
        print(f"生成卡密失败: {e}")
        return jsonify({'error': '生成卡密失败'}), 500

@card_bp.route('/redeem', methods=['POST'])
def redeem_card():
    """兑换卡密"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401

    try:
        data = request.get_json()
        key_code = data.get('card_key', '').strip()

        if not key_code:
            return jsonify({'error': '请输入卡密'}), 400

        # 查找卡密
        card_key = CardKey.query.filter_by(key_code=key_code).first()
        if not card_key:
            return jsonify({'error': '卡密不存在'}), 404

        # 检查卡密状态
        if not card_key.can_use():
            if card_key.is_used:
                return jsonify({'error': '卡密已被使用'}), 400
            elif card_key.is_expired():
                return jsonify({'error': '卡密已过期'}), 400
            else:
                return jsonify({'error': '卡密无效'}), 400

        # 获取用户信息
        user = User.query.filter_by(openid=openid).first()
        if not user:
            return jsonify({'error': '用户不存在'}), 404

        # 使用卡密
        if card_key.use_by(openid, user.nickname):
            # 给用户增加天数
            user.extend_days(card_key.days)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': f'卡密兑换成功，获得{card_key.days}天体验时间',
                'days_added': card_key.days,
                'new_total_days': user.total_days,
                'remaining_days': user.remaining_days()
            })
        else:
            return jsonify({'error': '卡密使用失败'}), 400

    except Exception as e:
        db.session.rollback()
        print(f"兑换卡密失败: {e}")
        return jsonify({'error': '兑换失败'}), 500

@card_bp.route('/list')
def list_card_keys():
    """获取卡密列表"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录', 'need_login': True}), 401

    if not is_admin(openid):
        return jsonify({'error': '权限不足', 'need_logout': True}), 403

    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', 'all')  # all, used, unused, expired

        query = CardKey.query

        # 状态筛选
        if status == 'used':
            query = query.filter(CardKey.is_used == True)
        elif status == 'unused':
            query = query.filter(CardKey.is_used == False)
        elif status == 'expired':
            query = query.filter(CardKey.expires_at < datetime.utcnow())

        # 分页
        pagination = query.order_by(CardKey.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            'keys': [key.to_dict() for key in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page
        })

    except Exception as e:
        print(f"获取卡密列表失败: {e}")
        return jsonify({'error': '获取卡密列表失败'}), 500

@card_bp.route('/stats')
def get_stats():
    """获取卡密统计信息"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录', 'need_login': True}), 401

    if not is_admin(openid):
        return jsonify({'error': '权限不足', 'need_logout': True}), 403

    try:
        total = CardKey.query.count()
        used = CardKey.query.filter(CardKey.is_used == True).count()
        unused = CardKey.query.filter(CardKey.is_used == False).count()
        expired = CardKey.query.filter(CardKey.expires_at < datetime.utcnow()).count()

        return jsonify({
            'total': total,
            'used': used,
            'unused': unused,
            'expired': expired
        })

    except Exception as e:
        print(f"获取统计信息失败: {e}")
        return jsonify({'error': '获取统计信息失败'}), 500