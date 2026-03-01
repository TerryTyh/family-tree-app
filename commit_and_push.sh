#!/bin/bash

# 进入项目目录
cd /Users/tianyuehua/应用/family-tree-app

# 检查状态
echo "检查 Git 状态..."
git status

# 添加所有更改
echo "添加所有更改..."
git add .

# 提交更改
echo "提交更改..."
git commit -m "更新功能：优化导入导出功能和错误处理"

# 推送到 GitHub
echo "推送到 GitHub..."
git push origin main

# 显示结果
echo "操作完成！"
git status
