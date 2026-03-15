#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv
load_dotenv()

url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')

print(f'Supabase URL: {url}')

# 配置requests使用自定义SSL设置
session = requests.Session()

# 测试连接
try:
    print('\n=== 测试 requests 库 ===')
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}'
    }
    response = session.get(f'{url}/rest/v1/members', headers=headers, timeout=10, verify=False)
    print('连接成功!')
    print(f'Status code: {response.status_code}')
    print(f'Response: {response.json()}')
except Exception as e:
    print(f'连接失败: {e}')
    import traceback
    traceback.print_exc()
