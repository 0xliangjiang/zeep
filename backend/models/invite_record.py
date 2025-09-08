from datetime import datetime
from database import db

class InviteRecord(db.Model):
    """邀请记录模型"""
    __tablename__ = 'invite_records'

    id = db.Column(db.Integer, primary_key=True)
    inviter_openid = db.Column(db.String(100), nullable=False, index=True, comment='邀请人openid')
    invitee_openid = db.Column(db.String(100), nullable=False, index=True, comment='被邀请人openid')
    invitee_nickname = db.Column(db.String(100), comment='被邀请人昵称')
    reward_days = db.Column(db.Integer, default=3, comment='奖励天数')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, inviter_openid, invitee_openid, invitee_nickname=None, reward_days=3):
        self.inviter_openid = inviter_openid
        self.invitee_openid = invitee_openid
        self.invitee_nickname = invitee_nickname
        self.reward_days = reward_days

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'inviter_openid': self.inviter_openid,
            'invitee_openid': self.invitee_openid,
            'invitee_nickname': self.invitee_nickname,
            'reward_days': self.reward_days,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def get_inviter_records(cls, inviter_openid):
        """获取邀请人的所有邀请记录"""
        return cls.query.filter_by(inviter_openid=inviter_openid).order_by(cls.created_at.desc()).all()

    @classmethod
    def get_invite_count(cls, inviter_openid):
        """获取邀请人的邀请数量"""
        return cls.query.filter_by(inviter_openid=inviter_openid).count()

    def __repr__(self):
        return f'<InviteRecord {self.inviter_openid} -> {self.invitee_openid}>'