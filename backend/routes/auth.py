import urllib.parse
import requests
from flask import Blueprint, request, session, redirect, jsonify, current_app
from models.user import User
from database import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/wechat')
def wechat_auth():
    """微信授权跳转"""
    # 获取邀请码
    invite_code = request.args.get('invite')

    # 构建微信授权URL
    redirect_uri = urllib.parse.quote(f"{current_app.config['WECHAT_CALLBACK_HOST']}/auth/callback")
    scope = 'snsapi_userinfo'
    state = request.args.get('state', 'default')

    # 如果有邀请码，将其添加到state中
    if invite_code:
        state = f"{state}|invite:{invite_code}"

    auth_url = (f"https://open.weixin.qq.com/connect/oauth2/authorize?"
                f"appid={current_app.config['WECHAT_APPID']}&"
                f"redirect_uri={redirect_uri}&"
                f"response_type=code&"
                f"scope={scope}&"
                f"state={state}#wechat_redirect")

    return redirect(auth_url)

@auth_bp.route('/callback')
def wechat_callback():
    """微信授权回调处理"""
    code = request.args.get('code')
    state = request.args.get('state', 'default')

    print(f"微信回调 - code: {code}, state: {state}")

    if not code:
        return jsonify({'error': '授权失败', 'message': '未能获取到授权码'}), 400

    # 从state中提取邀请码
    invite_code = None
    if '|invite:' in state:
        parts = state.split('|invite:')
        if len(parts) > 1:
            invite_code = parts[1]
            print(f"从state中提取到邀请码: {invite_code}")

    try:
        # 第一步：用code换取access_token和openid
        token_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
        token_params = {
            "appid": current_app.config['WECHAT_APPID'],
            "secret": current_app.config['WECHAT_APPSECRET'],
            "code": code,
            "grant_type": "authorization_code"
        }

        token_response = requests.get(token_url, params=token_params, timeout=10)
        token_data = token_response.json()

        if 'errcode' in token_data:
            return jsonify({
                'error': '获取Token失败',
                'message': token_data.get('errmsg', '未知错误')
            }), 400

        access_token = token_data.get('access_token')
        openid = token_data.get('openid')

        # 第二步：使用access_token和openid拉取用户信息
        userinfo_url = "https://api.weixin.qq.com/sns/userinfo"
        userinfo_params = {
            "access_token": access_token,
            "openid": openid,
            "lang": "zh_CN"
        }

        userinfo_response = requests.get(userinfo_url, params=userinfo_params, timeout=10)
        userinfo_response.encoding = 'utf-8'
        userinfo_data = userinfo_response.json()

        if 'errcode' in userinfo_data:
            return jsonify({
                'error': '获取用户信息失败',
                'message': userinfo_data.get('errmsg', '未知错误')
            }), 400

        # 处理用户信息
        openid = userinfo_data.get('openid')
        nickname = userinfo_data.get('nickname')
        headimgurl = userinfo_data.get('headimgurl')

        # 检查用户是否已存在
        user = User.query.filter_by(openid=openid).first()

        if not user:
            # 检查是否通过邀请链接注册（使用从state提取的邀请码）
            print(f"新用户注册 - 邀请码: {invite_code}")
            invited_by = None

            if invite_code:
                inviter = User.query.filter_by(invite_code=invite_code).first()
                print(f"查找邀请人 - 邀请码: {invite_code}, 找到邀请人: {inviter.nickname if inviter else 'None'}")
                if inviter:
                    invited_by = inviter.openid

            # 创建新用户（新用户默认有5天体验时间，不因邀请额外增加）
            user = User(
                openid=openid,
                nickname=nickname,
                headimgurl=headimgurl,
                invited_by=invited_by
            )
            db.session.add(user)

            # 如果是通过邀请注册，只给邀请人奖励，被邀请人不额外增加时间
            if invited_by:
                inviter = User.query.filter_by(openid=invited_by).first()
                if inviter:
                    print(f"给邀请人奖励 - 邀请人: {inviter.nickname}, 被邀请人: {nickname}")
                    # 邀请人增加3天时间
                    inviter.extend_days(3)

                    # 记录邀请关系
                    from models.invite_record import InviteRecord
                    invite_record = InviteRecord(
                        inviter_openid=invited_by,
                        invitee_openid=openid,
                        invitee_nickname=nickname
                    )
                    db.session.add(invite_record)
                    print(f"邀请记录已创建")

            db.session.commit()
        else:
            # 用户已存在，检查是否已被邀请过（使用从state提取的邀请码）
            print(f"老用户登录 - 用户: {nickname}, 邀请码: {invite_code}, 当前invited_by: {user.invited_by}")
            if invite_code and not user.invited_by:
                # 用户之前没有被邀请过，现在通过邀请链接登录
                inviter = User.query.filter_by(invite_code=invite_code).first()
                print(f"查找邀请人 - 邀请码: {invite_code}, 找到邀请人: {inviter.nickname if inviter else 'None'}")
                if inviter and inviter.openid != openid:  # 不能邀请自己
                    print(f"给老用户邀请人奖励 - 邀请人: {inviter.nickname}, 被邀请人: {nickname}")
                    # 更新被邀请人的邀请关系
                    user.invited_by = inviter.openid

                    # 给邀请人奖励
                    inviter.extend_days(3)

                    # 记录邀请关系
                    from models.invite_record import InviteRecord
                    invite_record = InviteRecord(
                        inviter_openid=inviter.openid,
                        invitee_openid=openid,
                        invitee_nickname=nickname
                    )
                    db.session.add(invite_record)
                    print(f"老用户邀请记录已创建")

                    db.session.commit()
            # 更新用户信息
            user.nickname = nickname
            user.headimgurl = headimgurl
            db.session.commit()

        # 存储用户信息到session
        session['openid'] = user.openid
        session['nickname'] = user.nickname
        session['headimgurl'] = user.headimgurl

        # 根据state参数决定跳转
        if state == 'admin':
            return redirect('/admin')
        else:
            return redirect('/')

    except requests.RequestException as e:
        return jsonify({'error': '网络请求失败', 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'error': '系统错误', 'message': str(e)}), 500

@auth_bp.route('/user')
def get_user():
    """获取当前用户信息"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401

    user = User.query.filter_by(openid=openid).first()
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    return jsonify(user.to_dict())

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """用户登出"""
    session.clear()
    return jsonify({'message': '登出成功'})

@auth_bp.route('/debug/invite/<invite_code>')
def debug_invite(invite_code):
    """调试邀请码"""
    user = User.query.filter_by(invite_code=invite_code).first()
    if user:
        return jsonify({
            'found': True,
            'user': {
                'openid': user.openid,
                'nickname': user.nickname,
                'invite_code': user.invite_code,
                'total_days': user.total_days,
                'remaining_days': user.remaining_days()
            }
        })
    else:
        # 列出所有用户的邀请码
        all_users = User.query.all()
        return jsonify({
            'found': False,
            'searched_code': invite_code,
            'all_invite_codes': [{'nickname': u.nickname, 'invite_code': u.invite_code} for u in all_users]
        })