import requests
import json

# Supabase项目信息
project_id = "ipnslrdmrbnwkmulwduj"
service_role_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlwbnNscmRtcmJud2ttdWx3ZHVqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MjM2OTMyNiwiZXhwIjoyMDg3OTQ1MzI2fQ.RJdNGIhHFy8HjFfKM_fKI99xY983st3JyMkl7EksQpk"

# API端点
api_url = f"https://{project_id}.supabase.co/rest/v1"
headers = {
    "apikey": service_role_key,
    "Authorization": f"Bearer {service_role_key}",
    "Content-Type": "application/json"
}

# 创建表的函数
def create_table(table_name, columns):
    print(f"正在创建表 {table_name}...")
    # 构建SQL语句
    columns_sql = ", ".join([f"{name} {type} {constraints}" for name, type, constraints in columns])
    sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"
    
    # 执行SQL
    response = requests.post(
        f"{api_url}/rpc/execute",
        headers=headers,
        json={"query": sql}
    )
    
    if response.status_code == 200:
        print(f"表 {table_name} 创建成功！")
    else:
        print(f"表 {table_name} 创建失败：{response.text}")

# 创建members表
def create_members_table():
    columns = [
        ("id", "UUID", "PRIMARY KEY DEFAULT gen_random_uuid()"),
        ("name", "VARCHAR(255)", "NOT NULL"),
        ("gender", "VARCHAR(10)", ""),
        ("birthDate", "DATE", ""),
        ("birthTime", "TIME", ""),
        ("deathDate", "DATE", ""),
        ("bio", "TEXT", ""),
        ("fatherId", "UUID", "REFERENCES members(id)"),
        ("motherId", "UUID", "REFERENCES members(id)"),
        ("photo", "TEXT", ""),
        ("created_at", "TIMESTAMP", "DEFAULT NOW()"),
        ("updated_at", "TIMESTAMP", "DEFAULT NOW()")
    ]
    create_table("members", columns)

# 创建spouses表
def create_spouses_table():
    columns = [
        ("id", "UUID", "PRIMARY KEY DEFAULT gen_random_uuid()"),
        ("memberId", "UUID", "REFERENCES members(id) NOT NULL"),
        ("spouseId", "UUID", "REFERENCES members(id) NOT NULL"),
        ("created_at", "TIMESTAMP", "DEFAULT NOW()")
    ]
    create_table("spouses", columns)

# 创建children表
def create_children_table():
    columns = [
        ("id", "UUID", "PRIMARY KEY DEFAULT gen_random_uuid()"),
        ("parentId", "UUID", "REFERENCES members(id) NOT NULL"),
        ("childId", "UUID", "REFERENCES members(id) NOT NULL"),
        ("created_at", "TIMESTAMP", "DEFAULT NOW()")
    ]
    create_table("children", columns)

# 主函数
def main():
    print("开始创建Supabase数据库表结构...")
    create_members_table()
    create_spouses_table()
    create_children_table()
    print("数据库表结构创建完成！")

if __name__ == "__main__":
    main()
