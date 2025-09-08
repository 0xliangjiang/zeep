from datetime import datetime
from database import db

class StepRecord(db.Model):
    """步数修改记录模型"""
    __tablename__ = 'step_records'

    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(100), nullable=False, index=True, comment='用户openid')
    steps = db.Column(db.Integer, nullable=False, comment='修改的步数')
    status = db.Column(db.String(20), nullable=False, comment='修改状态：success/failure/network_error')
    error_message = db.Column(db.Text, comment='错误信息')
    zepp_username = db.Column(db.String(100), comment='使用的Zepp账号')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __init__(self, openid, steps, status, error_message=None, zepp_username=None):
        self.openid = openid
        self.steps = steps
        self.status = status
        self.error_message = error_message
        self.zepp_username = zepp_username

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'openid': self.openid,
            'steps': self.steps,
            'status': self.status,
            'error_message': self.error_message,
            'zepp_username': self.zepp_username,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def get_user_records(cls, openid, limit=50):
        """获取用户的步数修改记录"""
        return cls.query.filter_by(openid=openid)\
            .order_by(cls.created_at.desc())\
            .limit(limit).all()

    def __repr__(self):
        return f'<StepRecord {self.openid} - {self.steps} steps - {self.status}>'