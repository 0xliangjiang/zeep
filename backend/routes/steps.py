import requests
import random
from flask import Blueprint, request, session, jsonify, current_app
from models.user import User
from models.zepp_account import ZeppAccount
from models.step_record import StepRecord
from services.qrcode_service import QRCodeService
from services.zepp_service import ZeppService
from services.bind_session_service import BindSessionService
from database import db

steps_bp = Blueprint('steps', __name__)

# 预设步数列表
PRESET_STEPS = [15485, 18569, 21586, 25841, 31054, 88888, 98800]

@steps_bp.route('/presets')
def get_presets():
    """获取预设步数列表"""
    return jsonify({
        'presets': PRESET_STEPS,
        'min_steps': current_app.config['MIN_STEPS'],
        'max_steps': current_app.config['MAX_STEPS']
    })

@steps_bp.route('/modify', methods=['POST'])
def modify_steps():
    """修改步数"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401

    # 获取用户信息
    user = User.query.filter_by(openid=openid).first()
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    # 检查用户授权是否有效
    if user.is_expired():
        return jsonify({'error': '授权已过期，请续费或邀请好友获取体验时间'}), 403

    # 获取步数参数
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求数据格式错误'}), 400

    steps = data.get('steps')
    if not steps:
        return jsonify({'error': '请输入步数'}), 400

    try:
        steps = int(steps)
    except ValueError:
        return jsonify({'error': '步数必须是数字'}), 400

    # 验证步数范围
    if steps < current_app.config['MIN_STEPS'] or steps > current_app.config['MAX_STEPS']:
        return jsonify({
            'error': f'步数必须在{current_app.config["MIN_STEPS"]}-{current_app.config["MAX_STEPS"]}之间'
        }), 400

    # 获取用户绑定的Zepp账号
    zepp_account = ZeppAccount.get_user_account(openid)

    # 如果没有绑定账号，分配一个可用账号
    if not zepp_account:
        available_account = ZeppAccount.get_available_account()
        if not available_account:
            return jsonify({'error': '暂无可用的Zepp账号，请稍后重试'}), 503

        zepp_account = available_account

    # 检查绑定状态
    print(f"检查Zepp账户绑定状态 - userid: {zepp_account.userid}, 数据库bind_status: {zepp_account.bind_status}")

    if not zepp_account.bind_status:
        # 先检查真实绑定状态
        print(f"数据库显示未绑定，开始检查真实绑定状态...")
        is_bound = ZeppService.check_bind_status(zepp_account.userid)
        print(f"真实绑定状态检查结果: {is_bound}")

        if is_bound:
            # 如果实际已绑定，更新数据库状态
            print(f"检测到账户实际已绑定，更新数据库状态: userid={zepp_account.userid}")
            zepp_account.complete_bind()
            if not zepp_account.bound_openid:
                zepp_account.bind_to_user(openid)
            db.session.commit()
            print(f"数据库状态已更新为已绑定")
        else:
            # 未绑定，需要显示二维码
            # 获取二维码URL（如果数据库中没有）
            qr_code_url = zepp_account.qr_code_url
            if not qr_code_url:
                print(f"正在获取userid {zepp_account.userid} 的二维码URL...")
                qr_code_url = ZeppService.get_qr_code_url(zepp_account.userid)
                if qr_code_url:
                    # 保存到数据库
                    zepp_account.update_qr_code_url(qr_code_url)
                    db.session.commit()
                    print(f"已保存二维码URL到数据库: {qr_code_url}")
                else:
                    print(f"获取userid {zepp_account.userid} 的二维码URL失败")

            # 立即写入bound_openid进行"占位"，防止其他用户使用同一账号
            if not zepp_account.bound_openid:
                zepp_account.bind_to_user(openid)
                db.session.commit()

            # 开始绑定会话（120秒超时）
            BindSessionService.start_bind_session(openid, zepp_account.id, 120)

            # 生成二维码图片
            if qr_code_url:
                qr_code_image = QRCodeService.generate_qr_code_url(qr_code_url)
            else:
                qr_code_image = None

            return jsonify({
                'need_bind': True,
                'qr_code_url': qr_code_image or 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==',
                'message': '请扫描二维码完成Zepp账号绑定',
                'timeout': 120
            })

    try:
        print(f"开始调用Zepp API修改步数: username={zepp_account.username}, steps={steps}")

        # 调用Zepp API修改步数
        zepp_response = requests.post(
            current_app.config['ZEPP_API_URL'],
            json={
                'username': zepp_account.username,
                'password': zepp_account.password,
                'steps': steps
            },
            headers={'Content-Type': 'application/json'},
            timeout=30
        )

        print(f"Zepp API响应状态码: {zepp_response.status_code}")
        zepp_data = zepp_response.json()
        print(f"Zepp API响应数据: {zepp_data}")

        # 记录修改结果
        step_record = StepRecord(
            openid=openid,
            steps=steps,
            status=zepp_data.get('status', 'unknown'),
            error_message=zepp_data.get('reason') if zepp_data.get('status') == 'failure' else None,
            zepp_username=zepp_account.username
        )
        db.session.add(step_record)
        db.session.commit()

        if zepp_data.get('status') == 'success':
            return jsonify({
                'success': True,
                'message': f'步数修改成功！已设置为 {steps} 步',
                'steps': steps
            })
        else:
            error_msg = zepp_data.get('reason', '修改失败')
            return jsonify({
                'success': False,
                'error': error_msg,
                'message': f'步数修改失败：{error_msg}'
            }), 400

    except requests.RequestException as e:
        print(f"Zepp API网络请求异常: {str(e)}")

        # 记录网络错误
        step_record = StepRecord(
            openid=openid,
            steps=steps,
            status='network_error',
            error_message=str(e),
            zepp_username=zepp_account.username
        )
        db.session.add(step_record)
        db.session.commit()

        return jsonify({
            'success': False,
            'error': '网络请求失败',
            'message': '网络连接异常，请稍后重试'
        }), 500
    except Exception as e:
        print(f"步数修改系统异常: {str(e)}")
        import traceback
        print(f"异常堆栈: {traceback.format_exc()}")

        # 记录系统错误
        try:
            step_record = StepRecord(
                openid=openid,
                steps=steps,
                status='system_error',
                error_message=str(e),
                zepp_username=zepp_account.username if 'zepp_account' in locals() else 'unknown'
            )
            db.session.add(step_record)
            db.session.commit()
        except Exception as db_error:
            print(f"记录错误到数据库失败: {str(db_error)}")
            pass  # 避免记录错误时再次出错

        return jsonify({
            'success': False,
            'error': '系统错误',
            'message': '系统异常，请联系客服'
        }), 500

@steps_bp.route('/random')
def get_random_steps():
    """获取随机步数"""
    min_steps = current_app.config['MIN_STEPS']
    max_steps = current_app.config['MAX_STEPS']
    random_steps = random.randint(min_steps, max_steps)

    return jsonify({
        'steps': random_steps,
        'min_steps': min_steps,
        'max_steps': max_steps
    })

@steps_bp.route('/history')
def get_history():
    """获取步数修改历史"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401

    try:
        records = StepRecord.query.filter_by(openid=openid)\
            .order_by(StepRecord.created_at.desc())\
            .limit(50).all()

        return jsonify({
            'records': [record.to_dict() for record in records]
        })
    except Exception as e:
        return jsonify({'error': '获取历史记录失败'}), 500

@steps_bp.route('/refresh-qrcode', methods=['POST'])
def refresh_qr_code():
    """刷新二维码URL（测试接口）"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401

    # 获取用户的Zepp账号
    zepp_account = ZeppAccount.get_user_account(openid)
    if not zepp_account:
        return jsonify({'error': '未分配Zepp账号'}), 404

    try:
        # 强制重新获取二维码URL
        print(f"正在刷新userid {zepp_account.userid} 的二维码URL...")
        qr_code_url = ZeppService.get_qr_code_url(zepp_account.userid)

        if qr_code_url:
            # 保存到数据库
            zepp_account.update_qr_code_url(qr_code_url)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': '二维码URL已刷新',
                'qr_code_url': qr_code_url
            })
        else:
            return jsonify({
                'success': False,
                'message': '获取二维码URL失败'
            })

    except Exception as e:
        print(f"刷新二维码URL异常: {e}")
        return jsonify({'error': '刷新二维码URL失败'}), 500

@steps_bp.route('/check-bind-status', methods=['POST'])
def check_bind_status():
    """检查绑定状态"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401

    print(f"检查绑定状态请求 - openid: {openid}")

    # 检查是否有绑定会话
    session_info = BindSessionService.get_session_info(openid)
    if not session_info:
        print(f"没有找到活跃的绑定会话")
        return jsonify({'bind_status': False, 'error': '没有活跃的绑定会话'})

    zepp_account_id = session_info['zepp_account_id']
    remaining_time = session_info['remaining_time']

    print(f"找到绑定会话 - zepp_account_id: {zepp_account_id}, remaining_time: {remaining_time}")

    # 获取Zepp账号
    zepp_account = ZeppAccount.query.get(zepp_account_id)
    if not zepp_account:
        print(f"Zepp账号不存在: {zepp_account_id}")
        return jsonify({'bind_status': False, 'error': 'Zepp账号不存在'})

    print(f"检查Zepp账号绑定状态 - userid: {zepp_account.userid}")

    # 调用ZeppService检查绑定状态
    try:
        is_bound = ZeppService.check_bind_status(zepp_account.userid)
        print(f"绑定状态检查结果: {is_bound}")

        if is_bound:
            # 绑定成功，完成绑定会话
            print(f"绑定成功，完成绑定会话")
            BindSessionService.complete_bind_session(openid)

            return jsonify({
                'bind_status': True,
                'message': 'Zepp账号已绑定成功'
            })
        else:
            print(f"绑定状态检查：未绑定")
            return jsonify({
                'bind_status': False,
                'remaining_time': remaining_time
            })

    except Exception as e:
        print(f"检查绑定状态异常: {e}")
        return jsonify({'bind_status': False, 'error': '检查绑定状态失败'})

@steps_bp.route('/cancel-bind', methods=['POST'])
def cancel_bind():
    """取消绑定会话"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401

    # 取消绑定会话
    BindSessionService.cancel_bind_session(openid)

    return jsonify({
        'success': True,
        'message': '绑定会话已取消'
    })

@steps_bp.route('/debug/bind-status')
def debug_bind_status():
    """调试绑定状态"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401

    # 获取用户的Zepp账号
    zepp_account = ZeppAccount.get_user_account(openid)
    if not zepp_account:
        return jsonify({
            'error': '未分配Zepp账号',
            'openid': openid
        })

    # 检查真实绑定状态
    real_bind_status = ZeppService.check_bind_status(zepp_account.userid)

    return jsonify({
        'openid': openid,
        'zepp_account': {
            'id': zepp_account.id,
            'userid': zepp_account.userid,
            'username': zepp_account.username,
            'bound_openid': zepp_account.bound_openid,
            'bind_status': zepp_account.bind_status
        },
        'real_bind_status': real_bind_status,
        'status_match': zepp_account.bind_status == real_bind_status
    })

@steps_bp.route('/records')
def get_step_records():
    """获取步数记录（详细版本）"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401

    try:
        records = StepRecord.query.filter_by(openid=openid)\
            .order_by(StepRecord.created_at.desc())\
            .limit(100).all()

        return jsonify({
            'records': [record.to_dict() for record in records]
        })
    except Exception as e:
        return jsonify({'error': '获取步数记录失败'}), 500