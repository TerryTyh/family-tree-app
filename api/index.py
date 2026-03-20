#!/usr/bin/env python3
import os
from app import app

# Vercel需要从环境变量中获取端口
port = int(os.environ.get('PORT', 5001))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)
