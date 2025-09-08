-- 添加系统设置表
CREATE TABLE IF NOT EXISTS system_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value TEXT,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_system_settings_key ON system_settings(key);

-- 插入默认系统设置
INSERT OR IGNORE INTO system_settings (key, value, description) VALUES 
('contact_content', '如需帮助，请通过以下方式联系我们：

📧 邮箱：support@example.com
💬 微信：zepp_support
⏰ 服务时间：9:00-18:00

我们会尽快为您解答！', '联系客服弹窗显示内容');
