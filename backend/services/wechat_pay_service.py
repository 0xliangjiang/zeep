import hashlib
import time
import random
import string
import xml.etree.ElementTree as ET
import requests
from flask import current_app, request


class WechatPayService:
    """微信支付服务类"""
    
    @staticmethod
    def generate_nonce_str(length=32):
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def generate_sign(params, api_key):
        """生成签名"""
        # 过滤空值并排序
        filtered_params = {k: v for k, v in params.items() if v != '' and k != 'sign'}
        sorted_params = sorted(filtered_params.items())
        
        # 构建签名字符串
        sign_str = '&'.join([f'{k}={v}' for k, v in sorted_params])
        sign_str += f'&key={api_key}'
        
        # MD5签名并转大写
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()
    
    @staticmethod
    def dict_to_xml(data):
        """字典转XML"""
        xml_str = '<xml>'
        for k, v in data.items():
            xml_str += f'<{k}><![CDATA[{v}]]></{k}>'
        xml_str += '</xml>'
        return xml_str
    
    @staticmethod
    def xml_to_dict(xml_str):
        """XML转字典"""
        root = ET.fromstring(xml_str)
        result = {}
        for child in root:
            result[child.tag] = child.text
        return result
    
    @classmethod
    def create_jsapi_order(cls, order_no, amount, description, openid):
        """创建JSAPI支付订单"""
        try:
            # 构建请求参数
            params = {
                'appid': current_app.config['WECHAT_APPID'],
                'mch_id': current_app.config['WECHAT_PAY_MCHID'],
                'nonce_str': cls.generate_nonce_str(),
                'body': description,
                'out_trade_no': order_no,
                'total_fee': int(amount * 100),  # 转换为分
                'spbill_create_ip': cls.get_client_ip(),
                'notify_url': current_app.config['WECHAT_PAY_NOTIFY_URL'],
                'trade_type': 'JSAPI',
                'openid': openid
            }
            
            # 生成签名
            params['sign'] = cls.generate_sign(params, current_app.config['WECHAT_PAY_API_KEY'])
            
            # 转换为XML
            xml_data = cls.dict_to_xml(params)
            
            # 发送请求
            print(f"发送微信支付请求: {xml_data}")
            response = requests.post(
                'https://api.mch.weixin.qq.com/pay/unifiedorder',
                data=xml_data.encode('utf-8'),
                headers={'Content-Type': 'application/xml'},
                timeout=30
            )

            print(f"微信支付响应状态码: {response.status_code}")
            print(f"微信支付响应内容: {response.text}")

            if response.status_code == 200:
                result = cls.xml_to_dict(response.text)
                print(f"解析后的响应数据: {result}")

                if result.get('return_code') == 'SUCCESS' and result.get('result_code') == 'SUCCESS':
                    # 构建前端支付参数
                    prepay_id = result.get('prepay_id')
                    timestamp = str(int(time.time()))
                    nonce_str = cls.generate_nonce_str()
                    
                    pay_params = {
                        'appId': current_app.config['WECHAT_APPID'],
                        'timeStamp': timestamp,
                        'nonceStr': nonce_str,
                        'package': f'prepay_id={prepay_id}',
                        'signType': 'MD5'
                    }
                    
                    # 生成支付签名
                    pay_params['paySign'] = cls.generate_sign(pay_params, current_app.config['WECHAT_PAY_API_KEY'])
                    
                    return {
                        'success': True,
                        'prepay_id': prepay_id,
                        'pay_params': pay_params
                    }
                else:
                    error_msg = result.get('err_code_des', result.get('return_msg', '创建订单失败'))
                    print(f"微信支付订单创建失败: {error_msg}")
                    return {
                        'success': False,
                        'error': error_msg
                    }
            else:
                return {
                    'success': False,
                    'error': f'请求失败，状态码: {response.status_code}'
                }
                
        except Exception as e:
            print(f"创建微信支付订单失败: {e}")
            return {
                'success': False,
                'error': '创建订单异常'
            }
    
    @classmethod
    def verify_callback(cls, xml_data):
        """验证支付回调"""
        try:
            # 解析XML
            data = cls.xml_to_dict(xml_data)
            
            # 提取签名
            received_sign = data.pop('sign', '')
            
            # 生成签名进行验证
            calculated_sign = cls.generate_sign(data, current_app.config['WECHAT_PAY_API_KEY'])
            
            if received_sign != calculated_sign:
                return {
                    'success': False,
                    'error': '签名验证失败'
                }
            
            # 检查支付结果
            if data.get('return_code') == 'SUCCESS' and data.get('result_code') == 'SUCCESS':
                return {
                    'success': True,
                    'order_no': data.get('out_trade_no'),
                    'transaction_id': data.get('transaction_id'),
                    'total_fee': int(data.get('total_fee', 0)) / 100  # 转换为元
                }
            else:
                return {
                    'success': False,
                    'error': data.get('err_code_des', '支付失败')
                }
                
        except Exception as e:
            print(f"验证支付回调失败: {e}")
            return {
                'success': False,
                'error': '回调验证异常'
            }
    
    @staticmethod
    def create_success_response():
        """创建成功响应XML"""
        return '<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>'
    
    @staticmethod
    def create_fail_response(msg='FAIL'):
        """创建失败响应XML"""
        return f'<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[{msg}]]></return_msg></xml>'

    @staticmethod
    def get_client_ip():
        """获取客户端真实IP"""
        if request.environ.get('HTTP_X_FORWARDED_FOR'):
            return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
        elif request.environ.get('HTTP_X_REAL_IP'):
            return request.environ['HTTP_X_REAL_IP']
        else:
            return request.environ.get('REMOTE_ADDR', '127.0.0.1')
