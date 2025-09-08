-- 创建卡密表
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='卡密表';
