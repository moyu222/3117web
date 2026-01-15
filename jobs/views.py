from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.core.paginator import Paginator
from .models import Job
from .forms import JobForm


def job_list_view(request):
    """职位列表视图"""
    # 从中间件获取用户（如果已登录）
    current_user = getattr(request, 'user_obj', None)
    
    # 如果是公司用户，只显示自己发布的职位；否则显示所有职位
    if current_user and current_user.is_company():
        jobs = Job.objects.filter(company_user=current_user)
    else:
        jobs = Job.objects.all()
    
    # 分页
    paginator = Paginator(jobs, 10)  # 每页10条
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'jobs/list.html', {
        'page_obj': page_obj,
        'is_company': current_user.is_company() if current_user else False
    })


@require_http_methods(["GET", "POST"])
def job_create_view(request):
    """创建职位视图（AJAX）"""
    # 从中间件获取用户（中间件已检查权限）
    current_user = getattr(request, 'user_obj', None)
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company_user = current_user
            job.save()
            return JsonResponse({
                'success': True,
                'message': '职位创建成功！',
                'job': {
                    'id': job.id,
                    'title': job.title,
                    'requirement': job.requirement,
                    'duty': job.duty,
                    'salary': job.salary,
                    'created_at': job.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    
    # GET 请求返回表单 HTML
    form = JobForm()
    return render(request, 'jobs/form_modal.html', {'form': form, 'form_title': '创建职位'})


@require_http_methods(["GET", "POST"])
def job_update_view(request, job_id):
    """更新职位视图（AJAX）"""
    # 从中间件获取用户（中间件已检查权限）
    current_user = getattr(request, 'user_obj', None)
    job = get_object_or_404(Job, id=job_id)
    
    # 检查是否是职位所属公司用户（中间件已检查公司用户，这里只检查所有权）
    if job.company_user != current_user:
        if request.method == 'POST':
            return JsonResponse({'success': False, 'error': '无权修改此职位'}, status=403)
        else:
            return render(request, 'jobs/form_modal.html', {
                'form': JobForm(),
                'form_title': '编辑职位',
                'error': '无权修改此职位'
            })
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': '职位更新成功！',
                'job': {
                    'id': job.id,
                    'title': job.title,
                    'requirement': job.requirement,
                    'duty': job.duty,
                    'salary': job.salary,
                    'updated_at': job.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    
    # GET 请求返回表单 HTML
    form = JobForm(instance=job)
    return render(request, 'jobs/form_modal.html', {
        'form': form,
        'form_title': '编辑职位',
        'job_id': job_id
    })


@require_POST
def job_delete_view(request, job_id):
    """删除职位视图（AJAX）"""
    # 从中间件获取用户（中间件已检查权限）
    current_user = getattr(request, 'user_obj', None)
    job = get_object_or_404(Job, id=job_id)
    
    # 检查是否是职位所属公司用户（中间件已检查公司用户，这里只检查所有权）
    if job.company_user != current_user:
        return JsonResponse({'success': False, 'error': '无权删除此职位'}, status=403)
    
    job_title = job.title
    job.delete()
    
    return JsonResponse({
        'success': True,
        'message': f'职位"{job_title}"已删除！'
    })
