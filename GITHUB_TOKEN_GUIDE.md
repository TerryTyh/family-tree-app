# GitHub 个人访问令牌生成指南

由于 GitHub 不再支持密码认证，您需要生成一个个人访问令牌来替代密码进行 Git 操作。

## 步骤 1：生成个人访问令牌

1. 打开浏览器，访问 https://github.com
2. 登录您的 GitHub 账号（tianyh2017@gmail.com）
3. 点击右上角的个人头像，选择「Settings」
4. 在左侧菜单中，选择「Developer settings」
5. 在左侧菜单中，选择「Personal access tokens」，然后选择「Tokens (classic)」
6. 点击「Generate new token」按钮，选择「Generate new token (classic)」
7. 填写表单：
   - Note：输入一个描述，例如「family-tree-app 部署」
   - Expiration：选择一个过期时间，例如「30 days」
   - Select scopes：勾选「repo」（这会自动勾选所有 repo 相关的权限）
8. 滚动到页面底部，点击「Generate token」按钮
9. 复制生成的令牌（这是您唯一一次看到完整令牌的机会）

## 步骤 2：使用个人访问令牌进行认证

1. 回到终端
2. 再次运行推送命令：
   ```bash
   git push -u origin main
   ```
3. 当提示输入用户名时，输入您的 GitHub 用户名：`TerryTyh`
4. 当提示输入密码时，粘贴您刚才复制的个人访问令牌
5. 按 Enter 键完成认证

## 步骤 3：启用 GitHub Pages

1. 打开浏览器，访问您的 GitHub 仓库页面：https://github.com/TerryTyh/family-tree-app
2. 点击「Settings」标签
3. 向下滚动到「GitHub Pages」部分
4. 在「Source」下拉菜单中选择「main branch」
5. 点击「Save」按钮
6. 等待几分钟，然后刷新页面
7. 在「GitHub Pages」部分，您将看到一个 URL，例如 `https://TerryTyh.github.io/family-tree-app/`
8. 您的家族树应用现在已经可以通过这个 URL 访问了！

## 注意事项

- 个人访问令牌相当于您的密码，请妥善保管，不要分享给他人
- 如果令牌过期，您需要重新生成一个新的令牌
- 部署完成后，任何对应用的修改都需要重新推送到 GitHub 才能生效

如果您在操作过程中遇到任何问题，请随时告诉我，我会为您提供进一步的帮助。