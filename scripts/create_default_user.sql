-- 创建默认用户（用于关联现有数据）
-- 密码: Tyh123456（使用bcrypt哈希）
INSERT INTO users (id, email, password_hash, username, created_at, updated_at)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'tianyh2017@gmail.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiAYMyzJ/I1K',
    '系统管理员',
    NOW(),
    NOW()
)
ON CONFLICT (email) DO NOTHING;

-- 将现有数据关联到默认用户
UPDATE members SET user_id = '00000000-0000-0000-0000-000000000001' WHERE user_id IS NULL;
UPDATE spouses SET user_id = '00000000-0000-0000-0000-000000000001' WHERE user_id IS NULL;
UPDATE children SET user_id = '00000000-0000-0000-0000-000000000001' WHERE user_id IS NULL;

-- 验证数据
SELECT 'Members count' as table_name, COUNT(*) as count FROM members WHERE user_id = '00000000-0000-0000-0000-000000000001'
UNION ALL
SELECT 'Spouses count', COUNT(*) FROM spouses WHERE user_id = '00000000-0000-0000-0000-000000000001'
UNION ALL
SELECT 'Children count', COUNT(*) FROM children WHERE user_id = '00000000-0000-0000-0000-000000000001';