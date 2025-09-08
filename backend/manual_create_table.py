#!/usr/bin/env python3
"""
手动创建card_keys表的脚本
"""

import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def create_card_keys_table():
    """手动创建card_keys表"""
    try:
        # 数据库连接配置
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'zepp'),
            'charset': 'utf8mb4'
        }
        
        print(f"连接数据库: {config['host']}:{config['port']}/{config['database']}")
        
        # 连接数据库
        connection = pymysql.connect(**config)
        
        with connection.cursor() as cursor:
            # 创建card_keys表的SQL
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS card_keys (
                id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                key_code VARCHAR(32) NOT NULL UNIQUE COMMENT '卡密码',
                days INT NOT NULL COMMENT '增加天数',
                
                -- 卡密状态
                is_used BOOLEAN DEFAULT FALSE COMMENT '是否已使用',
                is_active BOOLEAN DEFAULT TRUE COMMENT '是否有效',
                
                -- 使用信息
                used_by_openid VARCHAR(100) NULL COMMENT '使用者openid',
                used_by_nickname VARCHAR(100) NULL COMMENT '使用者昵称',
                used_at DATETIME NULL COMMENT '使用时间',
                
                -- 有效期
                expires_at DATETIME NULL COMMENT '过期时间，NULL表示永久有效',
                
                -- 创建信息
                created_by VARCHAR(100) NOT NULL COMMENT '创建者openid',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                
                -- 索引
                INDEX idx_key_code (key_code),
                INDEX idx_used_by_openid (used_by_openid),
                INDEX idx_created_by (created_by),
                INDEX idx_created_at (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='卡密表'
            """
            
            print("执行创建表SQL...")
            cursor.execute(create_table_sql)
            
            # 检查表是否创建成功
            cursor.execute("SHOW TABLES LIKE 'card_keys'")
            result = cursor.fetchone()
            
            if result:
                print("✅ card_keys表创建成功")
                
                # 显示表结构
                cursor.execute("DESCRIBE card_keys")
                columns = cursor.fetchall()
                print("\n表结构:")
                for column in columns:
                    print(f"  {column[0]} - {column[1]} - {column[2]}")
            else:
                print("❌ card_keys表创建失败")
        
        connection.commit()
        connection.close()
        print("\n数据库连接已关闭")
        
    except Exception as e:
        print(f"❌ 创建表时出错: {e}")

if __name__ == '__main__':
    create_card_keys_table()
