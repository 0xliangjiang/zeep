from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from datetime import datetime
from database import db

class DonationConfig(db.Model):
    """捐赠配置模型"""
    __tablename__ = 'donation_configs'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, comment='配置名称')
    price = Column(Float, nullable=False, comment='捐赠价格（元）')
    days = Column(Integer, nullable=False, comment='获得天数')
    is_active = Column(Boolean, default=True, comment='是否启用')
    
    # 创建信息
    created_by = Column(String(100), nullable=False, comment='创建者openid')
    created_at = Column(DateTime, default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment='更新时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'days': self.days,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class DonationOrder(db.Model):
    """捐赠订单模型"""
    __tablename__ = 'donation_orders'
    
    id = Column(Integer, primary_key=True)
    order_no = Column(String(32), unique=True, nullable=False, comment='订单号')
    
    # 用户信息
    user_openid = Column(String(100), nullable=False, comment='用户openid')
    user_nickname = Column(String(100), nullable=False, comment='用户昵称')
    
    # 订单信息
    amount = Column(Float, nullable=False, comment='捐赠金额（元）')
    days = Column(Integer, nullable=False, comment='获得天数')
    description = Column(String(200), nullable=False, comment='订单描述')
    
    # 支付信息
    prepay_id = Column(String(100), nullable=True, comment='微信预支付ID')
    transaction_id = Column(String(100), nullable=True, comment='微信交易号')
    
    # 订单状态
    status = Column(String(20), default='pending', comment='订单状态：pending/paid/failed/cancelled')
    
    # 时间信息
    created_at = Column(DateTime, default=func.now(), comment='创建时间')
    paid_at = Column(DateTime, nullable=True, comment='支付时间')
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment='更新时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'order_no': self.order_no,
            'user_openid': self.user_openid,
            'user_nickname': self.user_nickname,
            'amount': self.amount,
            'days': self.days,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None
        }
    
    @classmethod
    def generate_order_no(cls):
        """生成订单号"""
        import time
        import random
        timestamp = str(int(time.time()))
        random_str = ''.join(random.choices('0123456789', k=6))
        return f"DN{timestamp}{random_str}"
    
    def mark_as_paid(self, transaction_id):
        """标记为已支付"""
        self.status = 'paid'
        self.transaction_id = transaction_id
        self.paid_at = datetime.utcnow()
    
    def mark_as_failed(self):
        """标记为失败"""
        self.status = 'failed'
    
    def mark_as_cancelled(self):
        """标记为取消"""
        self.status = 'cancelled'
