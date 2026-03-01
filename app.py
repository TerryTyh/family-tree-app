#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sys
import os
import sqlite3

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from bazi_calculator import calculate_bazi
from lunar_python import Solar

app = Flask(__name__)
CORS(app)

# 数据库连接函数
def get_db_connection():
    conn = sqlite3.connect('data/members.db')
    conn.row_factory = sqlite3.Row
    return conn

# 初始化数据库
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # 创建成员表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            birth_date TEXT,
            birth_time TEXT,
            ba_zi TEXT,
            lunar_birth_date TEXT,
            death_date TEXT,
            photo TEXT,
            bio TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # 创建关系表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id TEXT NOT NULL,
            relation_type TEXT NOT NULL,
            related_member_id TEXT NOT NULL,
            FOREIGN KEY (member_id) REFERENCES members(id),
            FOREIGN KEY (related_member_id) REFERENCES members(id)
        )
    ''')
    conn.commit()
    conn.close()

# 初始化数据库
init_db()

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
def get_members():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取所有成员
        cursor.execute('SELECT * FROM members')
        members = []
        for row in cursor.fetchall():
            member = dict(row)
            # 处理baZi数据，转换为对象格式
            ba_zi_str = member.get('ba_zi')
            if ba_zi_str:
                # 尝试解析八字为四柱
                try:
                    if len(ba_zi_str) >= 8:
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
            # 获取成员的关系
            cursor.execute('SELECT relation_type, related_member_id FROM relations WHERE member_id = ?', (member['id'],))
            relations = cursor.fetchall()
            
            # 构建关系字典
            member_relations = {
                'fatherId': None,
                'motherId': None,
                'spouseIds': [],
                'childrenIds': []
            }
            
            for rel in relations:
                if rel['relation_type'] == 'father':
                    member_relations['fatherId'] = rel['related_member_id']
                elif rel['relation_type'] == 'mother':
                    member_relations['motherId'] = rel['related_member_id']
                elif rel['relation_type'] == 'spouse':
                    member_relations['spouseIds'].append(rel['related_member_id'])
                elif rel['relation_type'] == 'child':
                    member_relations['childrenIds'].append(rel['related_member_id'])
            
            # 合并关系到成员数据
            member.update(member_relations)
            members.append(member)
        
        conn.close()
        return jsonify({'members': members})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/members', methods=['POST'])
def create_member():
    try:
        data = request.json
        if not data or 'name' not in data or 'gender' not in data:
            return jsonify({'error': '缺少必要参数'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 处理baZi数据
        ba_zi_data = data.get('baZi')
        ba_zi_str = ba_zi_data.get('full') if isinstance(ba_zi_data, dict) else str(ba_zi_data) if ba_zi_data else None
        
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
        
        # 插入成员数据
        cursor.execute('''
            INSERT INTO members (id, name, gender, birth_date, birth_time, ba_zi, lunar_birth_date, death_date, photo, bio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('id'),
            data.get('name'),
            data.get('gender'),
            data.get('birthDate'),
            data.get('birthTime'),
            ba_zi_str,
            lunar_birth_date,
            data.get('deathDate'),
            data.get('photo'),
            data.get('bio')
        ))
        
        # 处理关系数据
        if 'fatherId' in data and data['fatherId']:
            cursor.execute('''
                INSERT INTO relations (member_id, relation_type, related_member_id)
                VALUES (?, ?, ?)
            ''', (data.get('id'), 'father', data['fatherId']))
        
        if 'motherId' in data and data['motherId']:
            cursor.execute('''
                INSERT INTO relations (member_id, relation_type, related_member_id)
                VALUES (?, ?, ?)
            ''', (data.get('id'), 'mother', data['motherId']))
        
        if 'spouseIds' in data and data['spouseIds']:
            for spouse_id in data['spouseIds']:
                cursor.execute('''
                    INSERT INTO relations (member_id, relation_type, related_member_id)
                    VALUES (?, ?, ?)
                ''', (data.get('id'), 'spouse', spouse_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': '成员创建成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/members/<member_id>', methods=['PUT'])
def update_member(member_id):
    try:
        data = request.json
        if not data:
            return jsonify({'error': '缺少必要参数'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 处理baZi数据
        ba_zi_data = data.get('baZi')
        ba_zi_str = ba_zi_data.get('full') if isinstance(ba_zi_data, dict) else str(ba_zi_data) if ba_zi_data else None
        
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
        
        # 更新成员数据
        cursor.execute('''
            UPDATE members
            SET name = ?, gender = ?, birth_date = ?, birth_time = ?, ba_zi = ?, lunar_birth_date = ?, death_date = ?, photo = ?, bio = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data.get('name'),
            data.get('gender'),
            data.get('birthDate'),
            data.get('birthTime'),
            ba_zi_str,
            lunar_birth_date,
            data.get('deathDate'),
            data.get('photo'),
            data.get('bio'),
            member_id
        ))
        
        # 删除旧关系
        cursor.execute('DELETE FROM relations WHERE member_id = ?', (member_id,))
        
        # 处理新关系数据
        if 'fatherId' in data and data['fatherId']:
            cursor.execute('''
                INSERT INTO relations (member_id, relation_type, related_member_id)
                VALUES (?, ?, ?)
            ''', (member_id, 'father', data['fatherId']))
        
        if 'motherId' in data and data['motherId']:
            cursor.execute('''
                INSERT INTO relations (member_id, relation_type, related_member_id)
                VALUES (?, ?, ?)
            ''', (member_id, 'mother', data['motherId']))
        
        if 'spouseIds' in data and data['spouseIds']:
            for spouse_id in data['spouseIds']:
                cursor.execute('''
                    INSERT INTO relations (member_id, relation_type, related_member_id)
                    VALUES (?, ?, ?)
                ''', (member_id, 'spouse', spouse_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': '成员更新成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/members/<member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 删除相关关系
        cursor.execute('DELETE FROM relations WHERE member_id = ? OR related_member_id = ?', (member_id, member_id))
        
        # 删除成员
        cursor.execute('DELETE FROM members WHERE id = ?', (member_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': '成员删除成功'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return "八字计算器API服务正在运行"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
