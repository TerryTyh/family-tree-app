#!/usr/bin/env python3
"""
修复app.html中的认证头部
"""
import re

file_path = '/Users/tianyuehua/应用/family-tree-app/web/app.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换 headers: { 'Content-Type': 'application/json' } 为 headers: getAuthHeaders()
# 但要保留getAuthHeaders函数定义不变

# 先找到getAuthHeaders函数的位置，保护它
pattern = r"(// 获取认证头部\n    function getAuthHeaders\(\) \{[^}]+\})"
match = re.search(pattern, content)
if match:
    auth_func = match.group(1)
    # 临时替换保护
    content = content.replace(auth_func, '___AUTH_FUNC_PLACEHOLDER___')

# 替换其他地方的headers
content = re.sub(
    r"headers:\s*\{\s*'Content-Type':\s*'application/json'\s*\}",
    "headers: getAuthHeaders()",
    content
)

# 恢复保护的内容
content = content.replace('___AUTH_FUNC_PLACEHOLDER___', auth_func)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ 已修复认证头部")
