#!/usr/bin/env python3
import os
import ssl
import requests
from dotenv import load_dotenv
load_dotenv()

url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')

print(f'Supabase URL: {url}')
print(f'SSL版本: {ssl.OPENSSL_VERSION}')

# 创建自定义SSL上下文
context = ssl.create_default_context()
context.min_version = ssl.TLSVersion.TLSv1_2
context.max_version = ssl.TLSVersion.TLSv1_3
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# 创建requests会话
session = requests.Session()
session.verify = False
session.mount('https://', requests.adapters.HTTPAdapter(
    pool_connections=100,
    pool_maxsize=100,
    max_retries=3
))

# 测试连接
try:
    print('\n=== 测试requests会话 ===')
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}'
    }
    response = session.get(f'{url}/rest/v1/members', headers=headers, timeout=10)
    print('连接成功!')
    print(f'Status code: {response.status_code}')
    print(f'Response: {response.json()}')
except Exception as e:
    print(f'连接失败: {e}')
    import traceback
    traceback.print_exc()
