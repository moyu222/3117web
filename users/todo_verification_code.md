# 验证码功能 TODO

## 功能需求
在登录和注册页面添加图形验证码功能，防止恶意注册和暴力破解。

## 实现计划

### 1. 验证码生成
- [ ] 使用 `django-simple-captcha` 或 `Pillow` 生成图形验证码
- [ ] 验证码包含 4-6 位随机字符（数字+字母）
- [ ] 验证码图片尺寸：120x40 像素
- [ ] 添加干扰线和噪点，提高识别难度

### 2. 验证码存储
- [ ] 将验证码答案存储到 session 中
- [ ] Session key: `captcha_code_{timestamp}`
- [ ] 设置过期时间：1 分钟（60秒）
- [ ] 每次生成新验证码时，清除旧的验证码

### 3. 验证码显示
- [ ] 在登录页面添加验证码输入框和图片
- [ ] 在注册页面添加验证码输入框和图片
- [ ] 添加"刷新验证码"按钮，点击可重新生成
- [ ] 验证码图片使用 base64 编码或独立URL

### 4. 验证码验证
- [ ] 在登录视图验证验证码
- [ ] 在注册视图验证验证码
- [ ] 验证码不区分大小写
- [ ] 验证码过期后提示用户刷新
- [ ] 验证失败时重新生成验证码

### 5. 技术实现细节

#### 后端实现
```python
# users/utils.py
import random
import string
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.cache import cache
from django.http import HttpResponse

def generate_captcha_code():
    """生成4位随机验证码"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

def generate_captcha_image(code):
    """生成验证码图片"""
    # 创建图片
    img = Image.new('RGB', (120, 40), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 绘制验证码文字
    # ... 实现细节
    
    # 添加干扰线
    # ... 实现细节
    
    return img

def save_captcha_to_session(request, code):
    """保存验证码到session，1分钟过期"""
    request.session['captcha_code'] = code
    request.session['captcha_expire'] = time.time() + 60  # 60秒后过期
```

#### 前端实现
```html
<!-- 验证码输入框 -->
<div class="mb-3">
    <label class="form-label">验证码</label>
    <div class="input-group">
        <input type="text" class="form-control" name="captcha" required>
        <img src="{% url 'users:captcha' %}" id="captcha_img" alt="验证码">
        <button type="button" class="btn btn-outline-secondary" id="refresh_captcha">刷新</button>
    </div>
</div>
```

### 6. URL 路由
- [ ] `GET /users/captcha/` - 生成并返回验证码图片
- [ ] 验证码图片响应类型：`image/png`

### 7. 测试要点
- [ ] 验证码生成是否正确
- [ ] 验证码1分钟后是否过期
- [ ] 验证码验证逻辑是否正确
- [ ] 刷新验证码功能是否正常
- [ ] 大小写不敏感验证

### 8. 注意事项
- 验证码存储使用 session，确保 session 配置正确
- 验证码图片生成要考虑性能，可以使用缓存
- 验证码刷新时，旧的验证码应该失效
- 考虑添加验证码输入错误次数限制（防止暴力破解）

## 优先级
- 高：验证码生成和存储
- 中：验证码显示和刷新
- 低：高级功能（错误次数限制、滑动验证等）
