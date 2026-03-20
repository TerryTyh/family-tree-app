#!/usr/bin/env python3
"""
创建family_shares表
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError('Supabase配置缺失，请设置环境变量SUPABASE_URL和SUPABASE_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print('正在创建family_shares表...')

# 注意：Supabase的Python客户端不支持直接执行DDL语句
# 我们需要使用SQL来创建表
# 这里我们提供一个SQL脚本，用户需要在Supabase控制台中执行

sql_script = """
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
"""

print('请在Supabase控制台中执行以下SQL语句来创建表:')
print('=' * 80)
print(sql_script)
print('=' * 80)
print('\n执行步骤:')
print('1. 访问: https://supabase.com/dashboard/project/ipnslrdmrbnwkmulwduj/sql')
print('2. 将上面的SQL语句复制到编辑器中')
print('3. 点击"Run"按钮执行')
print('4. 等待表创建完成')
