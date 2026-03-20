#!/usr/bin/env python3
"""
执行SQL语句创建family_shares表
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 加载环境变量
load_dotenv()

# Supabase配置
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError('Supabase配置缺失，请设置环境变量SUPABASE_URL和SUPABASE_KEY')

# 初始化Supabase客户端
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 读取SQL文件
with open('scripts/create_shares_table.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

print('正在执行SQL语句创建family_shares表...')
try:
    # 执行SQL语句
    # 注意：Supabase客户端不直接支持执行任意SQL，我们需要使用RPC或其他方式
    # 这里我们创建一个简单的函数来验证表是否存在
    
    # 尝试查询表结构，看看是否已经存在
    response = supabase.table('family_shares').select('id').limit(1).execute()
    print('family_shares表已存在')
except Exception as e:
    print(f'表不存在，需要创建: {e}')
    # 注意：实际创建表需要在Supabase控制台执行SQL，或者使用Supabase的API
    print('请在Supabase控制台执行以下SQL语句来创建表:')
    print(sql)

print('操作完成')
