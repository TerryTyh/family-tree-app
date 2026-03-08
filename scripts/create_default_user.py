#!/usr/bin/env python3
"""
创建默认用户并迁移现有数据
"""
import os
import sys
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

# 默认用户信息
DEFAULT_USER_ID = '00000000-0000-0000-0000-000000000001'
DEFAULT_EMAIL = 'tianyh2017@gmail.com'
DEFAULT_PASSWORD_HASH = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiAYMyzJ/I1K'
DEFAULT_USERNAME = '系统管理员'

def create_default_user():
    """创建默认用户"""
    try:
        # 检查用户是否已存在
        response = supabase.table('users').select('*').eq('email', DEFAULT_EMAIL).execute()
        
        if response.data:
            print(f"用户 {DEFAULT_EMAIL} 已存在，跳过创建")
            return DEFAULT_USER_ID
        
        # 创建用户
        user_data = {
            'id': DEFAULT_USER_ID,
            'email': DEFAULT_EMAIL,
            'password_hash': DEFAULT_PASSWORD_HASH,
            'username': DEFAULT_USERNAME
        }
        
        response = supabase.table('users').insert(user_data).execute()
        print(f"✓ 成功创建用户: {DEFAULT_EMAIL}")
        return DEFAULT_USER_ID
        
    except Exception as e:
        print(f"✗ 创建用户失败: {str(e)}")
        raise

def migrate_existing_data(user_id):
    """迁移现有数据到默认用户"""
    try:
        # 迁移members表
        members_response = supabase.table('members').update({'user_id': user_id}).is_('user_id', 'null').execute()
        members_count = len(members_response.data) if members_response.data else 0
        print(f"✓ 迁移 {members_count} 条成员数据")
        
        # 迁移spouses表
        spouses_response = supabase.table('spouses').update({'user_id': user_id}).is_('user_id', 'null').execute()
        spouses_count = len(spouses_response.data) if spouses_response.data else 0
        print(f"✓ 迁移 {spouses_count} 条配偶关系数据")
        
        # 迁移children表
        children_response = supabase.table('children').update({'user_id': user_id}).is_('user_id', 'null').execute()
        children_count = len(children_response.data) if children_response.data else 0
        print(f"✓ 迁移 {children_count} 条子女关系数据")
        
        return {
            'members': members_count,
            'spouses': spouses_count,
            'children': children_count
        }
        
    except Exception as e:
        print(f"✗ 迁移数据失败: {str(e)}")
        raise

def verify_migration(user_id):
    """验证迁移结果"""
    try:
        members_count = supabase.table('members').select('*', count='exact').eq('user_id', user_id).execute().count
        spouses_count = supabase.table('spouses').select('*', count='exact').eq('user_id', user_id).execute().count
        children_count = supabase.table('children').select('*', count='exact').eq('user_id', user_id).execute().count
        
        print("\n=== 迁移验证 ===")
        print(f"Members: {members_count}")
        print(f"Spouses: {spouses_count}")
        print(f"Children: {children_count}")
        
    except Exception as e:
        print(f"✗ 验证失败: {str(e)}")

if __name__ == '__main__':
    print("=== 开始创建默认用户并迁移数据 ===\n")
    
    try:
        # 创建默认用户
        user_id = create_default_user()
        
        # 迁移现有数据
        migrate_existing_data(user_id)
        
        # 验证迁移结果
        verify_migration(user_id)
        
        print("\n=== 完成 ===")
        print(f"默认用户: {DEFAULT_EMAIL}")
        print(f"密码: Tyh123456")
        
    except Exception as e:
        print(f"\n✗ 执行失败: {str(e)}")
        sys.exit(1)