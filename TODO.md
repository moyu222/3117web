# 项目待办事项

## 安全改进

### HTTPS 传输安全
- [ ] **实现 HTTPS 传输加密**
  - 配置 SSL/TLS 证书
  - 在 `settings.py` 中启用 HTTPS 相关配置
    - `SECURE_SSL_REDIRECT = True` - 强制 HTTPS 重定向
    - `SESSION_COOKIE_SECURE = True` - Session cookie 只在 HTTPS 下传输
    - `CSRF_COOKIE_SECURE = True` - CSRF cookie 只在 HTTPS 下传输
  - 配置生产环境部署（Nginx + SSL 证书）
  - 测试 HTTPS 连接和证书有效性
  - **优先级**：高（生产环境必须）
  - **说明**：当前密码以明文传输，虽然数据库使用 PBKDF2 哈希存储，但传输过程需要 HTTPS 保护

---

## 功能开发

### 验证码功能
- [ ] 实现登录和注册页面的图形验证码
  - 详细计划见 `users/todo_verification_code.md`
  - **优先级**：中

---

## 其他改进

- [ ] 添加登录失败次数限制（防止暴力破解）
- [ ] 实现 Session 过期检查中间件（见 3117.md）
- [ ] 添加密码强度验证（字母+数字+特殊字符）
