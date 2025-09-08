from flask import Blueprint, request, session, jsonify
from models.zepp_account import ZeppAccount
from database import db
import requests
import time

zepp_manage_bp = Blueprint('zepp_manage', __name__)

# 管理员openid列表
ADMIN_OPENIDS = [
    'oANc3vuHflVjbW9RRKLhBpSdr62I'
]

def is_admin(openid):
    """检查是否为管理员"""
    return openid in ADMIN_OPENIDS

@zepp_manage_bp.route('/check-admin', methods=['GET'])
def check_admin():
    """检查当前用户是否为管理员"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录'}), 401
    
    is_admin_user = is_admin(openid)
    
    return jsonify({
        'success': True,
        'is_admin': is_admin_user
    })

@zepp_manage_bp.route('/accounts', methods=['GET'])
def get_zepp_accounts():
    """获取所有Zepp账号列表"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录', 'need_login': True}), 401
    
    if not is_admin(openid):
        return jsonify({'error': '权限不足', 'need_logout': True}), 403
    
    try:
        accounts = ZeppAccount.query.all()
        account_list = []
        
        for account in accounts:
            account_list.append({
                'id': account.id,
                'username': account.username,
                'userid': account.userid,
                'ticket': account.qr_code_url[:50] + '...' if account.qr_code_url and len(account.qr_code_url) > 50 else account.qr_code_url,
                'is_active': account.is_active,
                'bind_status': account.bind_status,
                'bound_openid': account.bound_openid,
                'created_at': account.created_at.strftime('%Y-%m-%d %H:%M:%S') if account.created_at else None,
                'updated_at': account.updated_at.strftime('%Y-%m-%d %H:%M:%S') if account.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'accounts': account_list,
            'total': len(account_list)
        })
        
    except Exception as e:
        print(f"获取Zepp账号列表失败: {e}")
        return jsonify({'error': '获取账号列表失败'}), 500

@zepp_manage_bp.route('/accounts', methods=['POST'])
def add_zepp_accounts():
    """添加Zepp账号"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录', 'need_login': True}), 401
    
    if not is_admin(openid):
        return jsonify({'error': '权限不足', 'need_logout': True}), 403
    
    try:
        data = request.get_json()
        accounts_text = data.get('accounts', '').strip()
        
        if not accounts_text:
            return jsonify({'error': '账号信息不能为空'}), 400
        
        # 解析账号信息
        lines = accounts_text.split('\n')
        accounts_to_add = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if '\t' in line:
                parts = line.split('\t')
            elif ' ' in line:
                parts = line.split(' ', 1)
            else:
                return jsonify({'error': f'账号格式错误: {line}，请使用"用户名 密码"或"用户名\t密码"格式'}), 400

            if len(parts) != 2:
                return jsonify({'error': f'账号格式错误: {line}，请使用"用户名 密码"格式'}), 400

            username, password = parts[0].strip(), parts[1].strip()

            if not username or not password:
                return jsonify({'error': f'用户名或密码不能为空: {line}'}), 400

            # 检查用户名是否已存在
            existing_account = ZeppAccount.query.filter_by(username=username).first()
            if existing_account:
                return jsonify({'error': f'用户名已存在: {username}'}), 400

            accounts_to_add.append({'username': username, 'password': password})
        
        if not accounts_to_add:
            return jsonify({'error': '没有有效的账号信息'}), 400
        
        # 开始批量添加
        results = []
        success_count = 0

        for i, account_info in enumerate(accounts_to_add):
            print(f"正在处理账号 {i+1}/{len(accounts_to_add)}: {account_info['username']}")

            try:
                # 调用外部API获取Zepp信息
                api_response = requests.post(
                    'https://run.233ka.xyz/get-zepp-info',
                    headers={'Content-Type': 'application/json'},
                    json={
                        'username': account_info['username'],
                        'password': account_info['password']
                    },
                    timeout=30
                )
                
                if api_response.status_code == 200:
                    api_data = api_response.json()
                    
                    if api_data.get('status') == 'success' and 'data' in api_data:
                        zepp_data = api_data['data']
                        userid = zepp_data.get('userid')
                        ticket = zepp_data.get('ticket')
                        
                        if userid and ticket:
                            # 创建新的Zepp账号记录
                            new_account = ZeppAccount(
                                username=account_info['username'],
                                password=account_info['password'],
                                userid=userid,
                                qr_code_url=ticket
                            )
                            new_account.is_active = True

                            db.session.add(new_account)
                            db.session.commit()

                            success_count += 1
                            results.append({
                                'username': account_info['username'],
                                'success': True,
                                'message': '添加成功'
                            })
                        else:
                            results.append({
                                'username': account_info['username'],
                                'success': False,
                                'message': 'API返回数据不完整'
                            })
                            break
                    else:
                        error_msg = api_data.get('message', 'API调用失败')
                        results.append({
                            'username': account_info['username'],
                            'success': False,
                            'message': error_msg
                        })
                        break
                else:
                    results.append({
                        'username': account_info['username'],
                        'success': False,
                        'message': f'API请求失败，状态码: {api_response.status_code}'
                    })
                    break
                    
            except requests.RequestException as e:
                results.append({
                    'username': account_info['username'],
                    'success': False,
                    'message': f'网络请求失败: {str(e)}'
                })
                break
            except Exception as e:
                results.append({
                    'username': account_info['username'],
                    'success': False,
                    'message': f'处理失败: {str(e)}'
                })
                break
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(accounts_to_add),
            'success_count': success_count,
            'message': f'成功添加 {success_count}/{len(accounts_to_add)} 个账号'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"添加Zepp账号失败: {e}")
        return jsonify({'error': '添加账号失败'}), 500

@zepp_manage_bp.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_zepp_account(account_id):
    """删除Zepp账号"""
    openid = session.get('openid')
    if not openid:
        return jsonify({'error': '未登录', 'need_login': True}), 401
    
    if not is_admin(openid):
        return jsonify({'error': '权限不足', 'need_logout': True}), 403
    
    try:
        account = ZeppAccount.query.get(account_id)
        if not account:
            return jsonify({'error': '账号不存在'}), 404
        
        username = account.username
        db.session.delete(account)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'账号 {username} 删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"删除Zepp账号失败: {e}")
        return jsonify({'error': '删除账号失败'}), 500
