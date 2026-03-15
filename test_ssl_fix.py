#!/usr/bin/env python3
import os
import ssl
import urllib.request
from dotenv import load_dotenv
load_dotenv()

url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')

print(f'Supabase URL: {url}')
print(f'SSL版本: {ssl.OPENSSL_VERSION}')

# 创建更宽松的SSL上下文
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
context.min_version = ssl.TLSVersion.TLSv1_2

try:
    print('\n=== 测试宽松SSL上下文 ===')
    req = urllib.request.Request(f'{url}/rest/v1/members', headers={
        'apikey': key,
        'Authorization': f'Bearer {key}'
    })
    response = urllib.request.urlopen(req, context=context, timeout=10)
    print('连接成功!')
    print(f'Status code: {response.getcode()}')
except Exception as e:
    print(f'连接失败: {e}')
    import traceback
    traceback.print_exc()
