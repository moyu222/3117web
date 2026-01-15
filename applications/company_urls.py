from django.urls import path
from . import views

# 使用不同的 namespace 避免冲突
app_name = 'company'

urlpatterns = [
    # 以下路由将在后续实现
    # 公司端申请相关路由（通过 /company/ 前缀访问，实际路径为 /company/applications/）
    # path('applications/', views.company_application_list_view, name='application_list'),
    # path('applications/<int:app_id>/', views.company_application_detail_view, name='application_detail'),
    # path('applications/<int:app_id>/download-cv/', views.download_cv_view, name='download_cv'),
]
