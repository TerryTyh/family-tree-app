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

# 测试不同的SSL上下文配置
contexts = [
    ('默认上下文', ssl.create_default_context()),
    ('TLSv1_2上下文', ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)),
    ('宽松上下文', ssl.create_default_context()),
]

# 配置宽松上下文
contexts[2][1].check_hostname = False
contexts[2][1].verify_mode = ssl.CERT_NONE
contexts[2][1].min_version = ssl.TLSVersion.TLSv1_2

for name, context in contexts:
    print(f'\n=== 测试 {name} ===')
    try:
        req = urllib.request.Request(f'{url}/rest/v1/members', headers={
            'apikey': key,
            'Authorization': f'Bearer {key}'
        })
        response = urllib.request.urlopen(req, context=context, timeout=10)
        print('连接成功!')
        print(f'Status code: {response.getcode()}')
    except Exception as e:
        print(f'连接失败: {e}')
