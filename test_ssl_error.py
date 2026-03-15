#!/usr/bin/env python3
import os
import ssl
import urllib.request
from dotenv import load_dotenv
load_dotenv()

url = os.environ.get('SUPABASE_URL')
print(f'Supabase URL: {url}')

# 测试SSL连接
try:
    print('\n=== 测试SSL连接 ===')
    print(f'SSL版本: {ssl.OPENSSL_VERSION}')
    
    # 创建SSL上下文
    context = ssl.create_default_context()
    print(f'SSL上下文协议: {context.protocol}')
    
    # 测试连接
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req, context=context, timeout=10)
    print('SSL连接成功!')
    print(f'Status code: {response.getcode()}')
except Exception as e:
    print(f'SSL连接失败: {e}')
    import traceback
    traceback.print_exc()

# 测试Supabase REST API
try:
    print('\n=== 测试Supabase REST API ===')
    key = os.environ.get('SUPABASE_KEY')
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}'
    }
    
    req = urllib.request.Request(f'{url}/rest/v1/members', headers=headers)
    response = urllib.request.urlopen(req, timeout=10)
    print('Supabase API调用成功!')
    print(f'Status code: {response.getcode()}')
except Exception as e:
    print(f'Supabase API调用失败: {e}')
    import traceback
    traceback.print_exc()
