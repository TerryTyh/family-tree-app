#!/usr/bin/env python3
import os
import ssl
import socket
from dotenv import load_dotenv
load_dotenv()

url = os.environ.get('SUPABASE_URL').replace('https://', '')
print(f'Supabase URL: {url}')
print(f'SSL版本: {ssl.OPENSSL_VERSION}')

# 测试不同的SSL配置
ssl_configs = [
    ('默认上下文', ssl.create_default_context()),
    ('TLSv1_2上下文', ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)),
    ('宽松上下文', ssl.create_default_context()),
]

# 配置宽松上下文
ssl_configs[2][1].check_hostname = False
ssl_configs[2][1].verify_mode = ssl.CERT_NONE

for name, context in ssl_configs:
    print(f'\n=== 测试 {name} ===')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    
    try:
        # 连接到Supabase
        sock.connect((url, 443))
        print('Socket连接成功')
        
        # 包装socket
        secure_sock = context.wrap_socket(sock, server_hostname=url)
        print('SSL握手成功')
        print(f'协商的TLS版本: {secure_sock.version()}')
        print(f'协商的加密套件: {secure_sock.cipher()}')
        
        secure_sock.close()
    except Exception as e:
        print(f'连接失败: {e}')
    finally:
        sock.close()
