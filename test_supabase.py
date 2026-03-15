#!/usr/bin/env python3
import os
from dotenv import load_dotenv
load_dotenv()

from supabase import create_client

url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')

print(f'Supabase URL: {url}')
print(f'Supabase Key: {key[:20]}...')

try:
    supabase = create_client(url, key)
    response = supabase.table('members').select('*').limit(1).execute()
    print('Supabase连接成功')
    print(f'返回数据: {response.data}')
except Exception as e:
    print(f'Supabase连接失败: {e}')
