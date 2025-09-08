from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from database import db

class CardKey(db.Model):
    """卡密模型"""
    __tablename__ = 'card_keys'
    
    id = Column(Integer, primary_key=True)
    key_code = Column(String(32), unique=True, nullable=False, comment='卡密码')
    days = Column(Integer, nullable=False, comment='增加天数')
    
    # 卡密状态
    is_used = Column(Boolean, default=False, comment='是否已使用')
    is_active = Column(Boolean, default=True, comment='是否有效')
    
    # 使用信息
    used_by_openid = Column(String(100), nullable=True, comment='使用者openid')
    used_by_nickname = Column(String(100), nullable=True, comment='使用者昵称')
    used_at = Column(DateTime, nullable=True, comment='使用时间')
    
    # 有效期
    expires_at = Column(DateTime, nullable=True, comment='过期时间，NULL表示永久有效')
    
    # 创建信息
    created_by = Column(String(100), nullable=False, comment='创建者openid')
    created_at = Column(DateTime, default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment='更新时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'key_code': self.key_code,
            'days': self.days,
            'is_used': self.is_used,
            'is_active': self.is_active,
            'used_by_openid': self.used_by_openid,
            'used_by_nickname': self.used_by_nickname,
            'used_at': self.used_at.isoformat() if self.used_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_expired': self.is_expired()
        }
    
    def is_expired(self):
        """检查是否过期"""
        if not self.expires_at:
            return False  # 永久有效
        return datetime.utcnow() > self.expires_at
    
    def can_use(self):
        """检查是否可以使用"""
        return self.is_active and not self.is_used and not self.is_expired()
    
    def use_by(self, openid, nickname):
        """使用卡密"""
        if not self.can_use():
            return False
        
        self.is_used = True
        self.used_by_openid = openid
        self.used_by_nickname = nickname
        self.used_at = datetime.utcnow()
        return True
    
    @classmethod
    def generate_key_code(cls, length=12, include_numbers=True, include_lowercase=True, 
                         include_uppercase=True, include_symbols=False):
        """生成卡密码"""
        import random
        import string
        
        chars = ''
        if include_numbers:
            chars += string.digits
        if include_lowercase:
            chars += string.ascii_lowercase
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_symbols:
            chars += '!@#$%^&*'
        
        if not chars:
            chars = string.ascii_letters + string.digits
        
        # 生成唯一的卡密码
        while True:
            key_code = ''.join(random.choice(chars) for _ in range(length))
            if not cls.query.filter_by(key_code=key_code).first():
                return key_code
    
    @classmethod
    def create_batch(cls, count, days, length=12, include_numbers=True, 
                    include_lowercase=True, include_uppercase=True, 
                    include_symbols=False, expires_at=None, created_by=None):
        """批量创建卡密"""
        keys = []
        for _ in range(count):
            key_code = cls.generate_key_code(
                length=length,
                include_numbers=include_numbers,
                include_lowercase=include_lowercase,
                include_uppercase=include_uppercase,
                include_symbols=include_symbols
            )
            
            card_key = cls(
                key_code=key_code,
                days=days,
                expires_at=expires_at,
                created_by=created_by
            )
            keys.append(card_key)
            db.session.add(card_key)
        
        return keys
