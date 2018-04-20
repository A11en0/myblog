from django.shortcuts import render, redirect, HttpResponse,render_to_response
import logging
from django.conf import settings
from blog.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models.aggregates import Count
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from  .forms import *
from django.views.generic import ListView

logger = logging.getLogger('blog.views')

# Create your views here.
def globals_setting(request):
    #站点基本信息
    SITE_NAME =  settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    # 导航栏（分类）数据
    category_list = Category.objects.all()
    # 文章归档数据
    archive_list = Article.objects.distinct_date()
    #广告数据
    #标签数据
    tags = Tag.objects.all()
    #友情链接数据
    links = Links.objects.all()
    #文章排行榜数据
    #浏览排行
    article_click_list = Article.objects.all().order_by("-click_count")
    #评论排行
    comment_count_list = Comment.objects.values("article").annotate(comment_count=Count('article')).order_by('-comment_count')
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]
    #print(article_comment_list)
    #print(Comment.objects.values("article"))
    #站长推荐排行
    article_recommend_list = Article.objects.filter(is_recommend=True).order_by("-click_count")
    return locals()


#主页面
def index(request):
    try:
        # 最新文章数据
        article_list = getPage(request, Article.objects.all())
    except Exception as e:
        logger.error(e)
    return render(request, 'index.html', locals())

def about(request): 
    try: 
        pass
    except Exception as e:
        logger.error(e)
    return render(request, 'about.html', locals())


#归档页面
def archive(request):
    try:
        #先获取客户端提交的信息
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'archive.html', locals())


#分页

def getPage(request, article_list):
    paginator = Paginator(article_list, 5)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(page)
    return article_list

# 文章详情
def article(request):
    try:
        # 获取文章id
        id = request.GET.get('id', None)
        try:
            # 获取文章信息
            article = Article.objects.get(id=id)
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})


        # 评论表单
        comment_form = CommentForm({'article':id})

        # 获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)
        comment_num = len(comment_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'single.html', locals())

def blog(request):
    try:
        article_list = getPage(request, Article.objects.all())
    except Exception as e:
        logger.error(e)
    return render(request, 'blog.html', locals())


# 提交评论
def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # 获取表单信息
            '''
            comment = Comment.objects.create(username=comment_form.cleaned_data["author"],
                                             email=comment_form.cleaned_data["email"],
                                             url=comment_form.cleaned_data["url"],
                                             content=comment_form.cleaned_data["comment"],
                                             article_id=comment_form.cleaned_data["article"],
                                             user=request.user if request.user.is_authenticated() else None)
            '''
            comment = Comment.objects.create(
                content=comment_form.cleaned_data["comment"],
                article_id=comment_form.cleaned_data["article"],
                user=request.user)
            comment.save()
            print("okkkk!")
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        logging.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        logging.error(e)
    return redirect(request.META['HTTP_REFERER'])


# 注册
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                           email=reg_form.cleaned_data["email"],
                                           url=reg_form.cleaned_data["url"],
                                           password=make_password(reg_form.cleaned_data["password"]), )
                user.save()

                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                login(request, user)
                #return redirect(request.POST.get('source_url'))
                return HttpResponse("注册成功！")
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logging.error(e)
    return render(request, 'reg.html', locals())


# 登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logging.error(e)
    return render(request, 'login.html', locals())

def page_not_found(request):
    return render(request,'404.html')

def page_error(request):
    return render(request,'500.html')
