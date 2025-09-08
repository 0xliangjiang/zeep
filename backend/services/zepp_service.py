import requests
from flask import current_app

class ZeppService:
    """Zepp相关服务"""
    
    @staticmethod
    def get_qr_code_url(userid):
        """
        获取Zepp账号的二维码URL
        
        Args:
            userid: Zepp账户的userid
            
        Returns:
            二维码URL字符串，失败返回None
        """
        try:
            # 构建API URL
            api_url = "https://weixin.amazfit.com/v1/bind/qrcode.json"
            params = {
                'wxname': 'md',
                'brandName': 'amazfit',
                'userid': userid
            }
            
            # 发送请求
            response = requests.get(api_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # 检查响应格式
                if data.get('code') == 1 and 'data' in data:
                    ticket = data['data'].get('ticket')
                    if ticket:
                        print(f"成功获取userid {userid} 的二维码URL: {ticket}")
                        return ticket
                    else:
                        print(f"响应中没有ticket字段: {data}")
                        return None
                else:
                    print(f"API返回错误: {data}")
                    return None
            else:
                print(f"HTTP请求失败，状态码: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            print(f"获取二维码URL网络请求失败: {e}")
            return None
        except Exception as e:
            print(f"获取二维码URL异常: {e}")
            return None
    
    @staticmethod
    def check_bind_status(userid):
        """
        检查Zepp账号绑定状态

        Args:
            userid: Zepp账户的userid

        Returns:
            True表示已绑定，False表示未绑定
        """
        try:
            print(f"开始检查绑定状态 - userid: {userid}")

            # 构建API URL
            api_url = "https://weixin.amazfit.com/v1/info/users.json"
            params = {
                'wxname': 'md',
                'userid': userid
            }

            print(f"请求URL: {api_url}, 参数: {params}")

            # 发送请求
            response = requests.get(api_url, params=params, timeout=10)

            print(f"绑定状态检查响应 - 状态码: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"绑定状态检查响应数据: {data}")

                # 检查响应格式
                if data.get('code') == 1 and 'data' in data:
                    isbind = data['data'].get('isbind', 0)
                    print(f"isbind值: {isbind}, 类型: {type(isbind)}")

                    is_bound = isbind == 1
                    print(f"最终绑定状态判断: {is_bound}")
                    return is_bound
                else:
                    print(f"检查绑定状态API返回错误: {data}")
                    return False
            else:
                print(f"检查绑定状态HTTP请求失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                return False

        except requests.RequestException as e:
            print(f"检查绑定状态网络请求失败: {e}")
            return False
        except Exception as e:
            print(f"检查绑定状态异常: {e}")
            return False
