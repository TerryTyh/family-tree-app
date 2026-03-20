-- 创建家族分享表
CREATE TABLE IF NOT EXISTS family_shares (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  share_code VARCHAR(20) UNIQUE NOT NULL,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  expires_at TIMESTAMP WITH TIME ZONE
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_family_shares_user_id ON family_shares(user_id);
CREATE INDEX IF NOT EXISTS idx_family_shares_share_code ON family_shares(share_code);
CREATE INDEX IF NOT EXISTS idx_family_shares_is_active ON family_shares(is_active);
