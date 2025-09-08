#!/usr/bin/env python3
"""
修复card_keys表
强制删除并重新创建正确的表结构
"""

import pymysql

def fix_card_keys_table():
    """修复card_keys表"""
    try:
        # 数据库连接配置（直接使用配置值）
        config = {
            'host': 'localhost',
            'port': 3306,
            'user': 'zeppdb',
            'password': 'mXDbzAXXsakJWHE7',
            'database': 'zeppdb',
            'charset': 'utf8mb4'
        }
        
        print(f"连接数据库: {config['host']}:{config['port']}/{config['database']}")
        
        # 连接数据库
        connection = pymysql.connect(**config)
        
        with connection.cursor() as cursor:
            # 1. 删除现有的card_keys表（如果存在）
            print("1. 删除现有的card_keys表...")
            cursor.execute("DROP TABLE IF EXISTS card_keys")
            print("✅ 旧表已删除")
            
            # 2. 创建新的card_keys表
            print("2. 创建新的card_keys表...")
            create_table_sql = """
            CREATE TABLE card_keys (
                id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
                key_code VARCHAR(32) NOT NULL UNIQUE COMMENT '卡密码',
                days INT NOT NULL COMMENT '增加天数',
                is_used BOOLEAN DEFAULT FALSE COMMENT '是否已使用',
                is_active BOOLEAN DEFAULT TRUE COMMENT '是否有效',
                used_by_openid VARCHAR(100) NULL COMMENT '使用者openid',
                used_by_nickname VARCHAR(100) NULL COMMENT '使用者昵称',
                used_at DATETIME NULL COMMENT '使用时间',
                expires_at DATETIME NULL COMMENT '过期时间，NULL表示永久有效',
                created_by VARCHAR(100) NOT NULL COMMENT '创建者openid',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                INDEX idx_key_code (key_code),
                INDEX idx_used_by_openid (used_by_openid),
                INDEX idx_created_by (created_by),
                INDEX idx_created_at (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='卡密表'
            """
            
            cursor.execute(create_table_sql)
            print("✅ 新表创建成功")
            
            # 3. 验证表结构
            print("3. 验证表结构...")
            cursor.execute("DESCRIBE card_keys")
            columns = cursor.fetchall()
            print("\n新表结构:")
            for column in columns:
                print(f"  {column[0]} - {column[1]}")
            
            # 4. 测试插入一条记录
            print("\n4. 测试插入记录...")
            test_sql = """
            INSERT INTO card_keys (key_code, days, created_by) 
            VALUES ('TEST123456', 7, 'test_admin')
            """
            cursor.execute(test_sql)
            
            # 5. 测试查询
            print("5. 测试查询...")
            cursor.execute("SELECT * FROM card_keys WHERE key_code = 'TEST123456'")
            result = cursor.fetchone()
            if result:
                print(f"✅ 测试记录插入成功: {result}")
                
                # 删除测试记录
                cursor.execute("DELETE FROM card_keys WHERE key_code = 'TEST123456'")
                print("✅ 测试记录已清理")
            else:
                print("❌ 测试记录插入失败")
        
        connection.commit()
        connection.close()
        print("\n🎉 card_keys表修复完成！")
        
    except Exception as e:
        print(f"❌ 修复表时出错: {e}")

if __name__ == '__main__':
    fix_card_keys_table()
