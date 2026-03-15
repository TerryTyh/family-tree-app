#!/usr/bin/env python3
"""
验证并修复用户密码
"""
import os
import sys
import bcrypt
from supabase import create_client, Client
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Supabase配置
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("错误：请设置环境变量SUPABASE_URL和SUPABASE_KEY")
    sys.exit(1)

# 创建Supabase客户端
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 用户信息
EMAIL = 'tianyh2017@gmail.com'
PASSWORD = 'Tyh123456'

def verify_and_fix_password():
    """验证并修复密码"""
    try:
        # 查找用户
        result = supabase.table('users').select('*').eq('email', EMAIL).execute()
        
        if not result.data:
            print(f"用户 {EMAIL} 不存在")
            return
        
        user = result.data[0]
        stored_hash = user['password_hash']
        
        print(f"找到用户: {EMAIL}")
        print(f"存储的密码哈希: {stored_hash}")
        
        # 尝试验证密码
        if bcrypt.checkpw(PASSWORD.encode('utf-8'), stored_hash.encode('utf-8')):
            print(f"✓ 密码 '{PASSWORD}' 验证成功！")
        else:
            print(f"✗ 密码 '{PASSWORD}' 验证失败")
            
            # 生成新的密码哈希
            new_hash = bcrypt.hashpw(PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            print(f"生成新的密码哈希: {new_hash}")
            
            # 更新密码
            supabase.table('users').update({'password_hash': new_hash}).eq('email', EMAIL).execute()
            print(f"✓ 已更新用户 {EMAIL} 的密码")
            
            # 验证新密码
            result = supabase.table('users').select('*').eq('email', EMAIL).execute()
            user = result.data[0]
            if bcrypt.checkpw(PASSWORD.encode('utf-8'), user['password_hash'].encode('utf-8')):
                print(f"✓ 新密码验证成功！")
    
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    verify_and_fix_password()
