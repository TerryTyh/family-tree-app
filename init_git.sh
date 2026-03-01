#!/bin/bash

# 进入项目目录
cd /Users/tianyuehua/应用/family-tree-app

# 初始化 git 仓库
git init

# 配置 git 用户信息
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 添加远程仓库
git remote add origin https://github.com/your-username/family-tree-app.git

# 添加文件并提交
git add .
git commit -m "初始化项目"

# 推送到 GitHub
git push -u origin main
