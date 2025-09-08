#!/usr/bin/env python3
"""
数据库表创建脚本
用于手动创建所有数据库表
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

# 导入所有模型
from models.user import User
from models.zepp_account import ZeppAccount
from models.step_record import StepRecord
from models.invite_record import InviteRecord
from models.card_key import CardKey

def create_tables():
    """创建所有数据库表"""
    app = create_app()
    
    with app.app_context():
        print("开始创建数据库表...")
        
        # 创建所有表
        db.create_all()
        
        print("数据库表创建完成！")
        
        # 检查表是否创建成功
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"当前数据库中的表: {tables}")
        
        # 检查card_keys表的列
        if 'card_keys' in tables:
            columns = inspector.get_columns('card_keys')
            print(f"card_keys表的列: {[col['name'] for col in columns]}")
        else:
            print("警告: card_keys表未创建成功")

if __name__ == '__main__':
    create_tables()
