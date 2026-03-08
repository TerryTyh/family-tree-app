-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    username VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- 修改members表，添加user_id字段
ALTER TABLE members 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id);

CREATE INDEX IF NOT EXISTS idx_members_user_id ON members(user_id);

-- 修改spouses表，添加user_id字段
ALTER TABLE spouses 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id);

CREATE INDEX IF NOT EXISTS idx_spouses_user_id ON spouses(user_id);

-- 修改children表，添加user_id字段
ALTER TABLE children 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id);

CREATE INDEX IF NOT EXISTS idx_children_user_id ON children(user_id);

-- 为现有数据设置默认用户（可选，如果需要迁移现有数据）
-- UPDATE members SET user_id = '默认用户ID' WHERE user_id IS NULL;
-- UPDATE spouses SET user_id = '默认用户ID' WHERE user_id IS NULL;
-- UPDATE children SET user_id = '默认用户ID' WHERE user_id IS NULL;