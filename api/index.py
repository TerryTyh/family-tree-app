#!/usr/bin/env python3
import os
import sys

# 将当前目录添加到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from app import app

# Vercel需要从环境变量中获取端口
port = int(os.environ.get('PORT', 5001))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)
