#!/usr/bin/env python3
import os
import ssl
import http.client
from dotenv import load_dotenv
load_dotenv()

url = os.environ.get('SUPABASE_URL').replace('https://', '')
key = os.environ.get('SUPABASE_KEY')

print(f'Supabase URL: {url}')
print(f'SSL版本: {ssl.OPENSSL_VERSION}')

# 创建SSL上下文
context = ssl.create_default_context()
context.min_version = ssl.TLSVersion.TLSv1_2
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# 测试连接
try:
    print('\n=== 测试http.client ===')
    conn = http.client.HTTPSConnection(url, 443, context=context)
    conn.set_debuglevel(1)
    
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}'
    }
    
    conn.request('GET', '/rest/v1/members', headers=headers)
    response = conn.getresponse()
    
    print(f'连接成功!')
    print(f'Status code: {response.status}')
    print(f"Response: {response.read().decode('utf-8')}")
    
    conn.close()
except Exception as e:
    print(f'连接失败: {e}')
    import traceback
    traceback.print_exc()
