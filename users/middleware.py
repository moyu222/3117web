from django.shortcuts import redirect
from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sessions.models import Session
from django.utils import timezone
from .models import User


class SessionExpiryMiddleware(MiddlewareMixin):
    """Session 过期检查中间件 - 优先判断是否登录，防止用户正在访问时过期"""
    
    # 排除的路径（不需要检查过期）
    EXCLUDED_PATHS = [
        '/',
        '/home/',
        '/users/login/',
        '/users/register/',
        '/users/logout/',
        '/static/',
        '/media/',
        '/admin/',
    ]
    
    def process_request(self, request):
        """处理请求前检查 session 是否过期"""
        path = request.path
        
        # 排除的路径直接通过
        if any(path.startswith(excluded) for excluded in self.EXCLUDED_PATHS):
            return None
        
        # 优先判断是否登录（防止用户正在访问时过期）
        user_id = request.session.get('user_id')
        if not user_id:
            # 未登录，不需要检查过期
            return None
        
        # 已登录，检查 session 是否过期
        try:
            # 获取 session 过期时间
            expiry_date = request.session.get_expiry_date()
            if expiry_date and timezone.now() > expiry_date:
                # Session 已过期，清除 session 数据
                request.session.flush()
                messages.warning(request, '您的登录已过期，请重新登录。')
                return redirect('users:login')
        except Exception:
            # 如果获取过期时间失败，尝试从数据库查询
            try:
                session_key = request.session.session_key
                if session_key:
                    session = Session.objects.get(session_key=session_key)
                    if session.expire_date and timezone.now() > session.expire_date:
                        request.session.flush()
                        messages.warning(request, '您的登录已过期，请重新登录。')
                        return redirect('users:login')
            except (Session.DoesNotExist, Exception):
                # Session 不存在或查询失败，清除 session
                request.session.flush()
                return redirect('users:login')
        
        return None


class UserAuthMiddleware(MiddlewareMixin):
    """用户认证和权限检查中间件"""
    
    # 完全排除的路径（不需要任何检查）
    EXCLUDED_PATHS = [
        '/',
        '/home/',
        '/users/login/',
        '/users/register/',
        '/users/logout/',
        '/static/',
        '/media/',
        '/admin/',
    ]
    
    # 需要登录的路径（精确匹配）
    LOGIN_REQUIRED_PATHS = [
        '/jobs/create/',
        '/jobs/',  # 职位列表的创建/更新/删除操作需要登录
        '/company/',
    ]
    
    # 需要公司用户的路径（精确匹配）
    COMPANY_REQUIRED_PATHS = [
        '/jobs/create/',
        '/jobs/',  # 职位列表的创建/更新/删除需要公司用户
        '/company/',
    ]
    
    def is_excluded_path(self, path):
        """判断路径是否被排除"""
        # 精确匹配排除路径
        if path in self.EXCLUDED_PATHS:
            return True
        # 静态文件和媒体文件
        if path.startswith('/static/') or path.startswith('/media/'):
            return True
        return False
    
    def is_login_required_path(self, path):
        """判断路径是否需要登录"""
        # 职位列表页面本身不需要登录（所有用户可查看）
        if path == '/jobs/':
            return False
        # 职位创建/更新/删除需要登录
        if path.startswith('/jobs/create/') or '/update/' in path or '/delete/' in path:
            return True
        # 公司端功能需要登录
        if path.startswith('/company/'):
            return True
        return False
    
    def is_company_required_path(self, path):
        """判断路径是否需要公司用户"""
        # 职位列表页面本身不需要公司用户（所有用户可查看）
        if path == '/jobs/':
            return False
        # 职位创建/更新/删除需要公司用户
        if path.startswith('/jobs/create/') or '/update/' in path or '/delete/' in path:
            return True
        # 公司端功能需要公司用户
        if path.startswith('/company/'):
            return True
        return False
    
    def process_request(self, request):
        """处理请求前检查用户登录和权限"""
        path = request.path
        
        # 排除的路径直接通过
        if self.is_excluded_path(path):
            return None
        
        # 检查是否需要登录
        needs_login = self.is_login_required_path(path)
        needs_company = self.is_company_required_path(path)
        
        # 获取当前用户
        user_id = request.session.get('user_id')
        if not user_id:
            if needs_login:
                messages.warning(request, '请先登录。')
                return redirect('users:login')
            return None
        
        # 已登录，获取用户对象
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            # 用户不存在，清除 session
            request.session.flush()
            messages.warning(request, '用户不存在，请重新登录。')
            return redirect('users:login')
        
        # 将用户对象附加到 request（供视图使用）
        request.user_obj = user
        
        # 检查是否需要公司用户权限
        if needs_company and not user.is_company():
            messages.warning(request, '只有公司用户可以访问此功能。')
            return redirect('jobs:list')
        
        return None
