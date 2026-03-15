#!/usr/bin/env python3
import socket
import ssl
import os
from dotenv import load_dotenv
load_dotenv()

url = os.environ.get('SUPABASE_URL').replace('https://', '')
print(f'Supabase URL: {url}')
print(f'SSL版本: {ssl.OPENSSL_VERSION}')

# 创建socket连接
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)

# 连接到Supabase
try:
    print('\n=== 测试SSL socket连接 ===')
    sock.connect((url, 443))
    print('Socket连接成功')
    
    # 创建SSL上下文
    context = ssl.create_default_context()
    context.min_version = ssl.TLSVersion.TLSv1_2
    context.max_version = ssl.TLSVersion.TLSv1_3
    
    # 包装socket
    secure_sock = context.wrap_socket(sock, server_hostname=url)
    print('SSL握手成功')
    print(f'协商的TLS版本: {secure_sock.version()}')
    print(f'协商的加密套件: {secure_sock.cipher()}')
    
    # 发送HTTP请求
    request = f"GET /rest/v1/members HTTP/1.1\r\nHost: {url}\r\n\r\n"
    secure_sock.send(request.encode('utf-8'))
    
    # 接收响应
    response = secure_sock.recv(4096)
    print(f"\n响应: {response.decode('utf-8')}")
    
    secure_sock.close()
except Exception as e:
    print(f'连接失败: {e}')
    import traceback
    traceback.print_exc()
finally:
    sock.close()
