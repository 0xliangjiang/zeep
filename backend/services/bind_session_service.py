import threading
import time
from datetime import datetime, timedelta
from models.zepp_account import ZeppAccount
from database import db

class BindSessionService:
    """绑定会话管理服务"""
    
    # 存储绑定会话 {openid: {'zepp_account_id': xxx, 'timer': xxx, 'start_time': xxx}}
    _sessions = {}
    _lock = threading.Lock()
    
    @classmethod
    def start_bind_session(cls, openid, zepp_account_id, timeout=120):
        """
        开始绑定会话
        
        Args:
            openid: 用户openid
            zepp_account_id: Zepp账户ID
            timeout: 超时时间（秒），默认120秒
        """
        with cls._lock:
            # 如果已有会话，先清理
            if openid in cls._sessions:
                cls.cancel_bind_session(openid)
            
            # 创建定时器
            timer = threading.Timer(timeout, cls._timeout_callback, args=[openid, zepp_account_id])
            
            # 保存会话信息
            cls._sessions[openid] = {
                'zepp_account_id': zepp_account_id,
                'timer': timer,
                'start_time': datetime.utcnow(),
                'timeout': timeout
            }
            
            # 启动定时器
            timer.start()
            
            print(f"开始绑定会话: openid={openid}, zepp_account_id={zepp_account_id}, timeout={timeout}秒")
    
    @classmethod
    def complete_bind_session(cls, openid):
        """
        完成绑定会话
        
        Args:
            openid: 用户openid
            
        Returns:
            绑定的Zepp账户ID，如果没有会话返回None
        """
        with cls._lock:
            if openid not in cls._sessions:
                return None
            
            session_info = cls._sessions[openid]
            zepp_account_id = session_info['zepp_account_id']
            
            # 取消定时器
            session_info['timer'].cancel()
            
            # 移除会话
            del cls._sessions[openid]
            
            # 正式完成绑定（bound_openid已经在显示二维码时写入）
            try:
                zepp_account = ZeppAccount.query.get(zepp_account_id)
                if zepp_account and zepp_account.bound_openid == openid:
                    zepp_account.complete_bind()  # 只标记为已绑定，不重复写入bound_openid
                    db.session.commit()
                    print(f"绑定会话完成: openid={openid}, zepp_account_id={zepp_account_id}")
                    return zepp_account_id
            except Exception as e:
                print(f"完成绑定时出错: {e}")
                db.session.rollback()
            
            return None
    
    @classmethod
    def cancel_bind_session(cls, openid):
        """
        取消绑定会话

        Args:
            openid: 用户openid
        """
        with cls._lock:
            if openid in cls._sessions:
                session_info = cls._sessions[openid]
                zepp_account_id = session_info['zepp_account_id']

                # 取消定时器
                session_info['timer'].cancel()

                # 移除会话
                del cls._sessions[openid]

                # 清除Zepp账户的bound_openid，释放账户
                try:
                    zepp_account = ZeppAccount.query.get(zepp_account_id)
                    if zepp_account and zepp_account.bound_openid == openid:
                        zepp_account.bound_openid = None
                        zepp_account.bind_status = False
                        db.session.commit()
                        print(f"已清除取消绑定账户的bound_openid: zepp_account_id={zepp_account_id}")
                except Exception as e:
                    print(f"清除取消绑定账户bound_openid时出错: {e}")
                    db.session.rollback()

                print(f"绑定会话已取消: openid={openid}")
    
    @classmethod
    def get_session_info(cls, openid):
        """
        获取会话信息
        
        Args:
            openid: 用户openid
            
        Returns:
            会话信息字典，如果没有会话返回None
        """
        with cls._lock:
            if openid in cls._sessions:
                session_info = cls._sessions[openid]
                elapsed = (datetime.utcnow() - session_info['start_time']).total_seconds()
                remaining = max(0, session_info['timeout'] - elapsed)
                
                return {
                    'zepp_account_id': session_info['zepp_account_id'],
                    'remaining_time': int(remaining),
                    'start_time': session_info['start_time']
                }
            return None
    
    @classmethod
    def _timeout_callback(cls, openid, zepp_account_id):
        """
        超时回调函数

        Args:
            openid: 用户openid
            zepp_account_id: Zepp账户ID
        """
        with cls._lock:
            # 移除会话
            if openid in cls._sessions:
                del cls._sessions[openid]

            print(f"绑定会话超时: openid={openid}, zepp_account_id={zepp_account_id}")

            # 清除Zepp账户的bound_openid，释放账户供其他用户使用
            try:
                zepp_account = ZeppAccount.query.get(zepp_account_id)
                if zepp_account and zepp_account.bound_openid == openid:
                    zepp_account.bound_openid = None
                    zepp_account.bind_status = False
                    db.session.commit()
                    print(f"已清除超时账户的bound_openid: zepp_account_id={zepp_account_id}")
            except Exception as e:
                print(f"清除超时账户bound_openid时出错: {e}")
                db.session.rollback()
