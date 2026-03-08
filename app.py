#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import sys
import os
import json
import bcrypt
import jwt
from functools import wraps

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from bazi_calculator import calculate_bazi
from lunar_python import Solar

# 导入Supabase客户端
from supabase import create_client, Client

app = Flask(__name__)
CORS(app, origins=['https://terrytyh.github.io', 'http://localhost:8000'], supports_credentials=True)

# Supabase配置
import os
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError('Supabase配置缺失，请设置环境变量SUPABASE_URL和SUPABASE_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# JWT配置
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-here')
JWT_EXPIRATION_DAYS = 7

# 初始化数据库
def init_db():
    # Supabase数据库初始化由Supabase Dashboard处理
    # 这里只做简单的连接测试
    try:
        # 测试连接
        response = supabase.table('members').select('*').limit(1).execute()
        print('Supabase连接成功')
    except Exception as e:
        print(f'Supabase连接失败: {e}')

# 初始化数据库
init_db()

# JWT认证辅助函数
def generate_token(user_id):
    """生成JWT token"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=JWT_EXPIRATION_DAYS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def verify_token(token):
    """验证JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_current_user():
    """从请求中获取当前用户ID"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    try:
        token = auth_header.split(' ')[1]  # Bearer <token>
        return verify_token(token)
    except IndexError:
        return None

def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_current_user()
        if not user_id:
            return jsonify({'error': '请先登录'}), 401
        return f(*args, **kwargs)
    return decorated_function

# ==================== 用户认证API ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        username = data.get('username', '').strip()
        
        # 验证必填字段
        if not email:
            return jsonify({'error': '请输入邮箱'}), 400
        if not password:
            return jsonify({'error': '请输入密码'}), 400
        if len(password) < 6:
            return jsonify({'error': '密码长度至少6位'}), 400
        
        # 检查邮箱是否已存在
        existing_user = supabase.table('users').select('*').eq('email', email).execute()
        if existing_user.data:
            return jsonify({'error': '该邮箱已被注册'}), 409
        
        # 哈希密码
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # 创建用户
        user_data = {
            'email': email,
            'password_hash': password_hash,
            'username': username or email.split('@')[0]
        }
        
        result = supabase.table('users').insert(user_data).execute()
        user = result.data[0]
        
        # 生成token
        token = generate_token(user['id'])
        
        return jsonify({
            'message': '注册成功',
            'token': token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'username': user['username']
            }
        }), 201
        
    except Exception as e:
        print(f'注册失败: {str(e)}')
        return jsonify({'error': '注册失败，请稍后重试'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # 验证必填字段
        if not email:
            return jsonify({'error': '请输入邮箱'}), 400
        if not password:
            return jsonify({'error': '请输入密码'}), 400
        
        # 查找用户
        result = supabase.table('users').select('*').eq('email', email).execute()
        if not result.data:
            return jsonify({'error': '邮箱或密码错误'}), 401
        
        user = result.data[0]
        
        # 验证密码
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({'error': '邮箱或密码错误'}), 401
        
        # 生成token
        token = generate_token(user['id'])
        
        return jsonify({
            'message': '登录成功',
            'token': token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'username': user['username']
            }
        })
        
    except Exception as e:
        print(f'登录失败: {str(e)}')
        return jsonify({'error': '登录失败，请稍后重试'}), 500

@app.route('/api/auth/me', methods=['GET'])
@login_required
def get_current_user_info():
    """获取当前用户信息"""
    try:
        user_id = get_current_user()
        result = supabase.table('users').select('id,email,username,created_at').eq('id', user_id).execute()
        
        if not result.data:
            return jsonify({'error': '用户不存在'}), 404
        
        return jsonify({
            'user': result.data[0]
        })
        
    except Exception as e:
        print(f'获取用户信息失败: {str(e)}')
        return jsonify({'error': '获取用户信息失败'}), 500

# ==================== 八字计算API ====================

@app.route('/api/calculate-bazi', methods=['POST'])
def api_calculate_bazi():
    try:
        data = request.json
        if not data or 'birthTime' not in data:
            return jsonify({'error': '缺少必要参数'}), 400
        
        # 解析出生时间
        birth_time_str = data['birthTime']
        longitude = data.get('longitude', 120.0)
        
        try:
            # 尝试解析不同格式的时间字符串
            if 'T' in birth_time_str:
                # ISO格式: 2024-02-04T16:26:00
                birth_time = datetime.fromisoformat(birth_time_str)
            elif ' ' in birth_time_str:
                # 空格分隔格式: 2024-02-04 16:26:00
                birth_time = datetime.strptime(birth_time_str, '%Y-%m-%d %H:%M:%S')
            else:
                # 仅日期格式: 2024-02-04
                birth_time = datetime.strptime(birth_time_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': '时间格式错误，请使用YYYY-MM-DD HH:MM:SS格式'}), 400
        
        # 计算生辰八字
        bazi = calculate_bazi(birth_time, longitude)
        
        # 解析八字为四柱
        year = bazi[0:2]
        month = bazi[2:4]
        day = bazi[4:6]
        time = bazi[6:8]
        
        return jsonify({
            'year': year,
            'month': month,
            'day': day,
            'time': time,
            'full': bazi
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/members', methods=['GET'])
@login_required
def get_members():
    try:
        # 获取当前用户ID
        user_id = get_current_user()
        
        # 从Supabase获取当前用户的成员
        members_response = supabase.table('members').select('*').eq('user_id', user_id).execute()
        members_data = members_response.data
        
        # 从Supabase获取当前用户的配偶关系
        spouses_response = supabase.table('spouses').select('*').eq('user_id', user_id).execute()
        spouses_data = spouses_response.data
        
        # 从Supabase获取当前用户的子女关系
        children_response = supabase.table('children').select('*').eq('user_id', user_id).execute()
        children_data = children_response.data
        
        members = []
        for member in members_data:
            # 处理baZi数据，转换为对象格式
            ba_zi_str = member.get('ba_zi')
            if ba_zi_str:
                # 尝试解析八字为四柱
                try:
                    if isinstance(ba_zi_str, str) and len(ba_zi_str) >= 8:
                        member['baZi'] = {
                            'year': ba_zi_str[0:2],
                            'month': ba_zi_str[2:4],
                            'day': ba_zi_str[4:6],
                            'time': ba_zi_str[6:8],
                            'full': ba_zi_str
                        }
                    else:
                        member['baZi'] = {
                            'full': ba_zi_str
                        }
                except Exception:
                    member['baZi'] = {
                        'full': ba_zi_str
                    }
            else:
                member['baZi'] = None
            # 移除数据库字段，使用前端期望的字段名
            if 'ba_zi' in member:
                del member['ba_zi']
            if 'birth_date' in member:
                member['birthDate'] = member['birth_date']
                del member['birth_date']
            if 'birth_time' in member:
                member['birthTime'] = member['birth_time']
                del member['birth_time']
            if 'lunar_birth_date' in member:
                member['lunarBirthDate'] = member['lunar_birth_date']
                del member['lunar_birth_date']
            if 'death_date' in member:
                member['deathDate'] = member['death_date']
                del member['death_date']
            # 构建关系字典
            member_relations = {
                'fatherId': member.get('father_id'),
                'motherId': member.get('mother_id'),
                'spouseIds': [],
                'childrenIds': []
            }
            
            # 处理配偶关系
            for spouse in spouses_data:
                if spouse['member_id'] == member['id']:
                    member_relations['spouseIds'].append(spouse['spouse_id'])
            
            # 处理子女关系
            for child in children_data:
                if child['parent_id'] == member['id']:
                    member_relations['childrenIds'].append(child['child_id'])
            
            # 合并关系到成员数据
            member.update(member_relations)
            # 移除不需要的字段
            if 'father_id' in member:
                del member['father_id']
            if 'mother_id' in member:
                del member['mother_id']
            members.append(member)
        
        # 打印返回的数据，用于调试
        print(f'返回成员数据数量: {len(members)}')
        return jsonify({'members': members})
    except Exception as e:
        print(f'获取成员数据失败: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/members', methods=['POST'])
@login_required
def create_member():
    try:
        # 获取当前用户ID
        user_id = get_current_user()
        
        data = request.json
        if not data or 'name' not in data or 'gender' not in data:
            return jsonify({'error': '缺少必要参数'}), 400
        
        # 处理baZi数据
        ba_zi_data = data.get('baZi')
        ba_zi_str = ba_zi_data.get('full') if isinstance(ba_zi_data, dict) else str(ba_zi_data) if ba_zi_data else None
        
        # 如果没有baZi数据，尝试根据出生日期和时间计算
        if not ba_zi_str and data.get('birthDate'):
            try:
                # 构建完整的出生日期时间字符串
                birth_date = data.get('birthDate')
                birth_time = data.get('birthTime', '12:00:00')
                birth_time_str = f"{birth_date} {birth_time}"
                
                # 解析出生时间
                if ' ' in birth_time_str:
                    birth_time_obj = datetime.strptime(birth_time_str, '%Y-%m-%d %H:%M:%S')
                else:
                    birth_time_obj = datetime.strptime(birth_time_str, '%Y-%m-%d')
                
                # 计算生辰八字
                ba_zi_str = calculate_bazi(birth_time_obj, 120.0)
                print(f'自动计算生辰八字: {ba_zi_str}')
            except Exception as e:
                print(f'自动计算生辰八字失败: {str(e)}')
        
        # 计算农历生日
        lunar_birth_date = None
        birth_date = data.get('birthDate')
        if birth_date:
            try:
                solar = Solar.fromYmd(int(birth_date.split('-')[0]), int(birth_date.split('-')[1]), int(birth_date.split('-')[2]))
                lunar = solar.getLunar()
                lunar_birth_date = f"{lunar.getYear()}年{lunar.getMonth()}月{lunar.getDay()}"
            except Exception:
                pass
        
        # 插入成员数据到Supabase
        member_data = {
            'id': data.get('id'),
            'name': data.get('name'),
            'gender': data.get('gender'),
            'birth_date': data.get('birthDate'),
            'birth_time': data.get('birthTime'),
            'ba_zi': ba_zi_str,
            'lunar_birth_date': lunar_birth_date,
            'death_date': data.get('deathDate'),
            'photo': data.get('photo'),
            'bio': data.get('bio'),
            'father_id': data.get('fatherId'),
            'mother_id': data.get('motherId'),
            'user_id': user_id  # 关联当前用户
        }
        
        # 插入成员
        supabase.table('members').insert(member_data).execute()
        
        # 处理配偶关系
        if 'spouseIds' in data and data['spouseIds']:
            for spouse_id in data['spouseIds']:
                # 插入配偶关系
                supabase.table('spouses').insert({
                    'member_id': data.get('id'),
                    'spouse_id': spouse_id,
                    'user_id': user_id
                }).execute()
                
                # 插入反向配偶关系
                supabase.table('spouses').insert({
                    'member_id': spouse_id,
                    'spouse_id': data.get('id'),
                    'user_id': user_id
                }).execute()
        
        # 处理子女关系 - 这里需要在前端或其他地方处理
        
        return jsonify({'message': '成员创建成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/members/<member_id>', methods=['PUT'])
@login_required
def update_member(member_id):
    try:
        # 获取当前用户ID
        user_id = get_current_user()
        
        # 验证成员是否属于当前用户
        member_check = supabase.table('members').select('id').eq('id', member_id).eq('user_id', user_id).execute()
        if not member_check.data:
            return jsonify({'error': '无权修改此成员'}), 403
        
        data = request.json
        if not data:
            return jsonify({'error': '缺少必要参数'}), 400
        
        # 处理baZi数据
        ba_zi_data = data.get('baZi')
        ba_zi_str = ba_zi_data.get('full') if isinstance(ba_zi_data, dict) else str(ba_zi_data) if ba_zi_data else None
        
        # 如果没有baZi数据，尝试根据出生日期和时间计算
        if not ba_zi_str and data.get('birthDate'):
            try:
                # 构建完整的出生日期时间字符串
                birth_date = data.get('birthDate')
                birth_time = data.get('birthTime', '12:00:00')
                birth_time_str = f"{birth_date} {birth_time}"
                
                # 解析出生时间
                if ' ' in birth_time_str:
                    birth_time_obj = datetime.strptime(birth_time_str, '%Y-%m-%d %H:%M:%S')
                else:
                    birth_time_obj = datetime.strptime(birth_time_str, '%Y-%m-%d')
                
                # 计算生辰八字
                ba_zi_str = calculate_bazi(birth_time_obj, 120.0)
                print(f'自动计算生辰八字: {ba_zi_str}')
            except Exception as e:
                print(f'自动计算生辰八字失败: {str(e)}')
        
        # 计算农历生日
        lunar_birth_date = None
        birth_date = data.get('birthDate')
        if birth_date:
            try:
                solar = Solar.fromYmd(int(birth_date.split('-')[0]), int(birth_date.split('-')[1]), int(birth_date.split('-')[2]))
                lunar = solar.getLunar()
                lunar_birth_date = f"{lunar.getYear()}年{lunar.getMonth()}月{lunar.getDay()}"
            except Exception:
                pass
        
        # 更新成员数据到Supabase
        member_data = {
            'name': data.get('name'),
            'gender': data.get('gender'),
            'birth_date': data.get('birthDate'),
            'birth_time': data.get('birthTime'),
            'ba_zi': ba_zi_str,
            'lunar_birth_date': lunar_birth_date,
            'death_date': data.get('deathDate'),
            'photo': data.get('photo'),
            'bio': data.get('bio'),
            'father_id': data.get('fatherId'),
            'mother_id': data.get('motherId')
        }
        
        # 更新成员
        supabase.table('members').update(member_data).eq('id', member_id).execute()
        
        # 删除旧配偶关系
        supabase.table('spouses').delete().eq('member_id', member_id).execute()
        
        # 处理新配偶关系
        if 'spouseIds' in data and data['spouseIds']:
            for spouse_id in data['spouseIds']:
                # 插入配偶关系
                supabase.table('spouses').insert({
                    'member_id': member_id,
                    'spouse_id': spouse_id,
                    'user_id': user_id
                }).execute()
                
                # 确保反向配偶关系存在
                # 先删除旧的反向关系
                supabase.table('spouses').delete().eq('member_id', spouse_id).eq('spouse_id', member_id).execute()
                # 插入新的反向配偶关系
                supabase.table('spouses').insert({
                    'member_id': spouse_id,
                    'spouse_id': member_id,
                    'user_id': user_id
                }).execute()
        
        return jsonify({'message': '成员更新成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/members/<member_id>', methods=['DELETE'])
@login_required
def delete_member(member_id):
    try:
        # 获取当前用户ID
        user_id = get_current_user()
        
        # 验证成员是否属于当前用户
        member_check = supabase.table('members').select('id').eq('id', member_id).eq('user_id', user_id).execute()
        if not member_check.data:
            return jsonify({'error': '无权删除此成员'}), 403
        
        # 删除相关的配偶关系
        # 删除以该成员为member_id的配偶关系
        supabase.table('spouses').delete().eq('member_id', member_id).execute()
        # 删除以该成员为spouse_id的配偶关系
        supabase.table('spouses').delete().eq('spouse_id', member_id).execute()
        
        # 删除相关的子女关系
        # 删除以该成员为parent_id的子女关系
        supabase.table('children').delete().eq('parent_id', member_id).execute()
        # 删除以该成员为child_id的子女关系
        supabase.table('children').delete().eq('child_id', member_id).execute()
        
        # 删除成员
        supabase.table('members').delete().eq('id', member_id).execute()
        
        return jsonify({'message': '成员删除成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return "八字计算器API服务正在运行"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
