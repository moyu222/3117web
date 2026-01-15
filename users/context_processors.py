from .models import User


def current_user(request):
    """上下文处理器：让模板中可以使用 user"""
    # 优先使用中间件附加的用户对象（已检查过期）
    if hasattr(request, 'user_obj'):
        return {'user': request.user_obj}
    
    # 如果没有，从 session 获取（用于排除的路径）
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            return {'user': user}
        except (User.DoesNotExist, ValueError):
            return {'user': None}
    return {'user': None}
