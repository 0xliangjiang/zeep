from flask import Blueprint, request, session, jsonify, current_app
from datetime import datetime
from models.donation import DonationConfig, DonationOrder
from models.user import User
from services.wechat_pay_service import WechatPayService
from database import db
import time

donation_bp = Blueprint('donation', __name__)

# 管理员openid列表
ADMIN_OPENIDS = [
    'oANc3vuHflVjbW9RRKLhBpSdr62I'
]

def is_admin(openid):
    """检查是否为管理员"""
    return openid in ADMIN_OPENIDS

@donation_bp.route('/check-admin', methods=['GET'])
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

@donation_bp.route('/configs', methods=['GET'])
def get_donation_configs():
    """获取捐赠配置列表"""
    try:
        configs = DonationConfig.query.filter_by(is_active=True).order_by(DonationConfig.price.asc()).all()
        return jsonify({
            'success': True,
            'configs': [config.to_dict() for config in configs]
        })
    except Exception as e:
        print(f"获取捐赠配置失败: {e}")
        return jsonify({'error': '获取配置失败'}), 500

@donation_bp.route('/configs', methods=['POST'])
def save_donation_configs():
    """保存捐赠配置"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录', 'need_login': True}), 401
    
    if not is_admin(openid):
        return jsonify({'error': '权限不足', 'need_logout': True}), 403
    
    try:
        data = request.get_json()
        configs = data.get('configs', [])
        
        if len(configs) != 3:
            return jsonify({'error': '必须设置3个捐赠配置'}), 400
        
        # 验证配置数据
        for i, config in enumerate(configs):
            price = config.get('price')
            days = config.get('days')
            
            if not price or price <= 0:
                return jsonify({'error': f'第{i+1}个配置的价格无效'}), 400
            
            if not days or days <= 0:
                return jsonify({'error': f'第{i+1}个配置的天数无效'}), 400
        
        # 删除现有配置
        DonationConfig.query.delete()
        
        # 创建新配置
        for i, config in enumerate(configs):
            donation_config = DonationConfig(
                name=f'捐赠方案{i+1}',
                price=config['price'],
                days=config['days'],
                created_by=openid
            )
            db.session.add(donation_config)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '捐赠配置保存成功'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"保存捐赠配置失败: {e}")
        return jsonify({'error': '保存配置失败'}), 500

@donation_bp.route('/create-order', methods=['POST'])
def create_donation_order():
    """创建捐赠订单"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401

    print(f"创建捐赠订单，用户openid: {openid}")
    
    try:
        data = request.get_json()
        config_id = data.get('config_id')
        
        if not config_id:
            return jsonify({'error': '请选择捐赠方案'}), 400
        
        # 获取捐赠配置
        config = DonationConfig.query.filter_by(id=config_id, is_active=True).first()
        if not config:
            return jsonify({'error': '捐赠方案不存在'}), 404
        
        # 获取用户信息
        user = User.query.filter_by(openid=openid).first()
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        # 创建订单
        order = DonationOrder(
            order_no=DonationOrder.generate_order_no(),
            user_openid=openid,
            user_nickname=user.nickname,
            amount=config.price,
            days=config.days,
            description=f'捐赠{config.price}元获得{config.days}天体验时间'
        )
        
        db.session.add(order)
        db.session.commit()

        # 检查微信支付配置
        print(f"微信支付配置检查:")
        print(f"APPID: {current_app.config['WECHAT_APPID']}")
        print(f"MCHID: {current_app.config['WECHAT_PAY_MCHID']}")
        print(f"API_KEY: {'*' * len(current_app.config['WECHAT_PAY_API_KEY'])}")

        # 使用真实微信支付模式
        print("使用真实微信支付模式")
        pay_result = WechatPayService.create_jsapi_order(
            order_no=order.order_no,
            amount=order.amount,
            description=order.description,
            openid=openid
        )

        print(f"微信支付结果: {pay_result}")

        if pay_result['success']:
            # 更新订单的prepay_id
            order.prepay_id = pay_result['prepay_id']
            db.session.commit()

            return jsonify({
                'success': True,
                'order_no': order.order_no,
                'amount': order.amount,
                'days': order.days,
                'payment_params': pay_result['pay_params']
            })
        else:
            # 支付订单创建失败，标记订单为失败
            order.mark_as_failed()
            db.session.commit()

            return jsonify({
                'success': False,
                'error': f'创建支付订单失败: {pay_result["error"]}'
            }), 400
        
    except Exception as e:
        db.session.rollback()
        print(f"创建捐赠订单失败: {e}")
        return jsonify({'error': '创建订单失败'}), 500

@donation_bp.route('/payment-callback', methods=['POST'])
def payment_callback():
    """微信支付回调"""
    try:
        # 获取回调数据
        xml_data = request.data.decode('utf-8')
        print(f"收到微信支付回调: {xml_data}")

        # 验证回调签名和数据
        verify_result = WechatPayService.verify_callback(xml_data)

        if not verify_result['success']:
            print(f"回调验证失败: {verify_result['error']}")
            return WechatPayService.create_fail_response(verify_result['error'])

        order_no = verify_result['order_no']
        transaction_id = verify_result['transaction_id']

        # 查找订单
        order = DonationOrder.query.filter_by(order_no=order_no).first()
        if not order:
            print(f"订单不存在: {order_no}")
            return WechatPayService.create_fail_response('订单不存在')

        # 检查订单是否已经处理过
        if order.status == 'paid':
            print(f"订单已处理: {order_no}")
            return WechatPayService.create_success_response()

        # 支付成功，更新订单状态
        order.mark_as_paid(transaction_id)

        # 给用户增加天数
        user = User.query.filter_by(openid=order.user_openid).first()
        if user:
            user.extend_days(order.days)
            print(f"用户 {user.nickname} 通过捐赠获得 {order.days} 天体验时间")

        db.session.commit()

        return WechatPayService.create_success_response()

    except Exception as e:
        print(f"处理支付回调失败: {e}")
        return WechatPayService.create_fail_response('系统错误')



@donation_bp.route('/test-config', methods=['GET'])
def test_wechat_pay_config():
    """测试微信支付配置"""
    openid = session.get('openid')
    if not openid or not is_admin(openid):
        return jsonify({'error': '权限不足'}), 403

    try:
        config_status = {
            'appid': current_app.config.get('WECHAT_APPID', '未配置'),
            'mchid': current_app.config.get('WECHAT_PAY_MCHID', '未配置'),
            'api_key_length': len(current_app.config.get('WECHAT_PAY_API_KEY', '')),
            'notify_url': current_app.config.get('WECHAT_PAY_NOTIFY_URL', '未配置')
        }

        return jsonify({
            'success': True,
            'config': config_status
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
