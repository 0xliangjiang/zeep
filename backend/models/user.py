from datetime import datetime, timedelta
import uuid
import string
import random
from database import db

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(100), unique=True, nullable=False, index=True, comment='微信用户唯一标识')
    nickname = db.Column(db.String(100), nullable=False, comment='微信昵称')
    headimgurl = db.Column(db.Text, comment='微信头像URL')
    expire_time = db.Column(db.DateTime, nullable=False, comment='授权到期时间')
    total_days = db.Column(db.Integer, default=5, comment='总授权天数')
    used_days = db.Column(db.Integer, default=0, comment='已使用天数')
    invite_code = db.Column(db.String(32), unique=True, index=True, comment='用户专属邀请码')
    invited_by = db.Column(db.String(100), index=True, comment='邀请人openid')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, openid, nickname, headimgurl=None, invited_by=None):
        self.openid = openid
        self.nickname = nickname
        self.headimgurl = headimgurl
        self.invited_by = invited_by
        self.expire_time = datetime.utcnow() + timedelta(days=5)  # 默认5天免费体验
        self.invite_code = self.generate_invite_code()

    def generate_invite_code(self):
        """生成唯一邀请码"""
        while True:
            code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            if not User.query.filter_by(invite_code=code).first():
                return code

    def is_expired(self):
        """检查是否已过期"""
        return datetime.utcnow() > self.expire_time

    def remaining_days(self):
        """获取剩余天数"""
        if self.is_expired():
            return 0
        delta = self.expire_time - datetime.utcnow()
        return max(0, delta.days)

    def extend_days(self, days):
        """延长授权天数"""
        if self.is_expired():
            # 如果已过期，从当前时间开始计算
            self.expire_time = datetime.utcnow() + timedelta(days=days)
        else:
            # 如果未过期，在现有时间基础上延长
            self.expire_time += timedelta(days=days)
        self.total_days += days

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'openid': self.openid,
            'nickname': self.nickname,
            'headimgurl': self.headimgurl,
            'expire_time': self.expire_time.isoformat() if self.expire_time else None,
            'total_days': self.total_days,
            'used_days': self.used_days,
            'remaining_days': self.remaining_days(),
            'invite_code': self.invite_code,
            'invited_by': self.invited_by,
            'is_expired': self.is_expired(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<User {self.nickname}({self.openid})>'