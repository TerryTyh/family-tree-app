#!/usr/bin/env python3
import os
import ssl
import urllib3
from dotenv import load_dotenv
load_dotenv()

url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')

print(f'Supabase URL: {url}')
print(f'SSL版本: {ssl.OPENSSL_VERSION}')

# 创建自定义的urllib3 PoolManager with SSL context
context = ssl.create_default_context()
context.min_version = ssl.TLSVersion.TLSv1_2
context.max_version = ssl.TLSVersion.TLSv1_3
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# 创建自定义HTTP客户端
http_client = urllib3.PoolManager(
    ssl_context=context,
    cert_reqs='CERT_NONE',
    assert_hostname=False
)

# 测试连接
try:
    print('\n=== 测试自定义HTTP客户端 ===')
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}'
    }
    response = http_client.request('GET', f'{url}/rest/v1/members', headers=headers, timeout=10)
    print('连接成功!')
    print(f'Status code: {response.status}')
    print(f"Response: {response.data.decode('utf-8')}")
except Exception as e:
    print(f'连接失败: {e}')
    import traceback
    traceback.print_exc()
