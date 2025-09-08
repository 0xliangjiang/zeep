from datetime import datetime
from database import db

class ZeppAccount(db.Model):
    """Zepp账号模型"""
    __tablename__ = 'zepp_accounts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True, comment='Zepp账号用户名')
    password = db.Column(db.String(100), nullable=False, comment='Zepp账号密码')
    userid = db.Column(db.String(100), nullable=False, comment='Zepp账户userid')
    qr_code_url = db.Column(db.Text, comment='绑定微信的二维码链接(ticket)')
    bound_openid = db.Column(db.String(100), unique=True, index=True, comment='绑定的微信openid')
    is_active = db.Column(db.Boolean, default=True, comment='账号是否可用')
    bind_status = db.Column(db.Boolean, default=False, comment='绑定状态：False未绑定，True已绑定')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, username, password, userid, qr_code_url=None):
        self.username = username
        self.password = password
        self.userid = userid
        self.qr_code_url = qr_code_url

    def bind_to_user(self, openid):
        """分配给用户（但还未完成绑定）"""
        self.bound_openid = openid
        self.bind_status = False  # 分配后仍需要用户扫码绑定

    def complete_bind(self):
        """完成绑定"""
        self.bind_status = True

    def unbind(self):
        """解绑"""
        self.bound_openid = None
        self.bind_status = False

    def update_qr_code_url(self, qr_code_url):
        """更新二维码URL"""
        self.qr_code_url = qr_code_url
        self.updated_at = datetime.utcnow()

    def is_available(self):
        """检查账号是否可用（未分配给用户或未完成绑定且激活）"""
        return self.is_active and (not self.bound_openid or not self.bind_status)

    def to_dict(self, include_sensitive=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'username': self.username,
            'userid': self.userid,
            'qr_code_url': self.qr_code_url,
            'bound_openid': self.bound_openid,
            'is_active': self.is_active,
            'bind_status': self.bind_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_sensitive:
            data['password'] = self.password

        return data

    @classmethod
    def get_available_account(cls):
        """获取一个可用的账号（优先选择完全未分配的，其次选择已分配但未绑定的）"""
        # 优先选择完全未分配的账号
        account = cls.query.filter_by(is_active=True, bound_openid=None).first()
        if account:
            return account

        # 如果没有完全未分配的，选择已分配但未完成绑定的账号
        account = cls.query.filter_by(is_active=True, bind_status=False).first()
        return account

    @classmethod
    def get_user_account(cls, openid):
        """获取用户绑定的账号"""
        return cls.query.filter_by(bound_openid=openid).first()

    def __repr__(self):
        return f'<ZeppAccount {self.username}>'