# GitHub Pages 部署详细指南

本指南将帮助您使用 GitHub Pages 部署家族树应用，使其可以在互联网上被访问。

## 准备工作

- 您已经有 GitHub 账号：tianyh2017@gmail.com
- 您需要在电脑上安装 Git（如果还没有安装）

## 步骤 1：安装 Git

如果您还没有安装 Git，请按照以下步骤安装：

### Windows 用户：
1. 访问 https://git-scm.com/download/win
2. 下载并运行安装程序
3. 按照安装向导的提示完成安装

### macOS 用户：
1. 打开终端
2. 运行命令：`xcode-select --install`
3. 按照提示安装命令行工具

### Linux 用户：
1. 打开终端
2. 运行命令：`sudo apt-get install git`（Ubuntu/Debian）或 `sudo yum install git`（CentOS/RHEL）

## 步骤 2：创建 GitHub 仓库

1. 打开浏览器，访问 https://github.com
2. 使用您的账号（tianyh2017@gmail.com）登录
3. 点击右上角的「+」按钮，选择「New repository」
4. 在「Repository name」字段中输入一个名称，例如 `family-tree-app`
5. 在「Description」字段中输入一个简短的描述，例如「家族树应用 - 记录家族历史与传承」
6. 选择「Public」（公开）
7. 不要勾选「Initialize this repository with a README」
8. 点击「Create repository」按钮

## 步骤 3：将应用文件推送到 GitHub

### Windows 用户：
1. 打开 Git Bash（在开始菜单中搜索）
2. 导航到家族树应用的文件夹：
   ```bash
   cd /c/Users/tianyuehua/应用/family-tree-app
   ```
3. 初始化 Git 仓库：
   ```bash
   git init
   ```
4. 添加所有文件：
   ```bash
   git add .
   ```
5. 提交文件：
   ```bash
   git commit -m "Initial commit"
   ```
6. 连接到 GitHub 仓库（将 `<your-username>` 替换为您的 GitHub 用户名）：
   ```bash
   git remote add origin https://github.com/<your-username>/family-tree-app.git
   ```
7. 推送到 GitHub：
   ```bash
   git push -u origin master
   ```
8. 当提示输入用户名和密码时，输入您的 GitHub 账号信息

### macOS/Linux 用户：
1. 打开终端
2. 导航到家族树应用的文件夹：
   ```bash
   cd /Users/tianyuehua/应用/family-tree-app
   ```
3. 初始化 Git 仓库：
   ```bash
   git init
   ```
4. 添加所有文件：
   ```bash
   git add .
   ```
5. 提交文件：
   ```bash
   git commit -m "Initial commit"
   ```
6. 连接到 GitHub 仓库（将 `<your-username>` 替换为您的 GitHub 用户名）：
   ```bash
   git remote add origin https://github.com/<your-username>/family-tree-app.git
   ```
7. 推送到 GitHub：
   ```bash
   git push -u origin master
   ```
8. 当提示输入用户名和密码时，输入您的 GitHub 账号信息

## 步骤 4：启用 GitHub Pages

1. 打开浏览器，访问您的 GitHub 仓库页面
2. 点击「Settings」标签
3. 向下滚动到「GitHub Pages」部分
4. 在「Source」下拉菜单中选择「master branch」
5. 点击「Save」按钮
6. 等待几分钟，然后刷新页面
7. 在「GitHub Pages」部分，您将看到一个 URL，例如 `https://<your-username>.github.io/family-tree-app/`
8. 您的家族树应用现在已经可以通过这个 URL 访问了！

## 步骤 5：测试部署

1. 打开浏览器，访问 GitHub Pages 提供的 URL
2. 确认应用能够正常加载
3. 测试添加和编辑家族成员的功能
4. 确认家族树能够正确显示
5. 测试数据保存和加载功能

## 注意事项

- 数据存储在用户的浏览器中，不会被其他用户看到
- 每个用户的浏览器中都有自己独立的数据库
- 如果您希望在多用户之间共享数据，需要添加后端服务器和数据库
- 部署完成后，任何对应用的修改都需要重新推送到 GitHub 才能生效

## 常见问题

### 推送失败
- 检查您的 GitHub 账号信息是否正确
- 确保您的网络连接正常
- 检查仓库名称是否正确

### 应用无法访问
- 确保您已经启用了 GitHub Pages
- 等待几分钟，GitHub Pages 需要时间来部署您的应用
- 检查 URL 是否正确

### 应用功能异常
- 确保所有文件都已正确推送到 GitHub
- 检查浏览器控制台是否有错误信息
- 尝试清除浏览器缓存

如果您在部署过程中遇到任何问题，请随时告诉我，我会为您提供进一步的帮助。