import os
import logging
import markdown
from django.views import View
from django.shortcuts import render, redirect
from homepage.models import RC_Article_Type, RC_Article_Tag, RC_Article, RC_Comments

# Django自带分页[数据分页]
from django.core.paginator import Paginator

from django.conf import settings
from functools import wraps
from django.db.models import Q

base = logging.getLogger("django").debug
error = logging.getLogger("error").error
info = logging.getLogger("info").info


# Create your views here.


def logformat(func):
    wraps(func)

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error(e.__class__.__name__, e)
    return inner


class CategoryView(View):
    """文章分类处理"""

    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass


class TagView(View):
    """标签处理"""

    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass


class CommentsView(View):
    """评论处理"""

    def get(self):
        pass

    def post(self, request):
        blog_id = int(request.POST.get('blog-id', 0))
        to_index = int(request.POST.get('todo', 0))
        if to_index == 1:
            # 新增评论
            try:
                name = request.POST.get('name', '')
                email = request.POST.get('email', '')
                content = request.POST.get('comment', '')
                if name == '' or content == '':
                    error('Add comment error, value is None!')
                    return redirect('/show-blog/' + str(blog_id) + '#down')
                if email is not None and email != '':
                    try:
                        email_check = RC_Comments.objects.get(email=email)
                        if email_check is not None:
                            name = email_check.user_name
                    except Exception as e:
                        pass

                log = 'blog_id: {}, name: {}, email: {}; content: {}'.format(str(blog_id), name, email, content)
                parents_id = int(request.POST.get('comment-id', 0))
                if parents_id == 0:
                    log = '新增评论' + log
                    comment = RC_Comments(
                        email=email, article_id=blog_id, user_name=name,
                        content=content
                    )
                    comment.save()
                else:
                    # 将回复评论 回复回复评论的评论 分到同一个组下并给予不同序号
                    main_comment = RC_Comments.objects.get(id=parents_id)
                    no = int(main_comment.count if main_comment.count is not None else 0) + 1  # 回复评论序号
                    reply_name = request.POST.get('reply_name', main_comment.user_name)

                    log += '\n新增评论回复: 回复评论id={}, 序号={}, 回复评论的昵称={}'.format(
                        str(main_comment.parents_id), str(no), reply_name)

                    comment = RC_Comments(
                        email=email, article_id=blog_id, user_name=name, replied_user=reply_name,
                        parents_id=parents_id, content=content, number=no
                    )
                    # 更新回复数
                    comment.save()
                    main_comment.count = no
                    main_comment.save()
                info(log)
            except Exception as e:
                log = 'save comment error!\n' + log
                error(log + '\n' + e.__class__.__name__ + ':' + str(e))
        return redirect('/show-blog/' + str(blog_id) + '#down')


class ArticleView(View):
    """文章处理"""

    def __init__(self):
        self.blog_id = None
        self.comment_page = 1

    def getBlogInfo(self):
        blog = RC_Article.objects.get(id=self.blog_id)
        RC_Article.objects.filter(id=self.blog_id).update(visits=blog.visits + 1)
        if blog:
            md = markdown.Markdown(
                extensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
                    'markdown.extensions.toc',
                ]
            )
            blog.md_content = md.convert(blog.md_content)
            comments = all_info.getComments(self.blog_id)
            data = all_info.getBaseInfo()

            data['blog'] = blog
            data['toc'] = md.toc
            data['comments'] = comments
            data['pages'] = all_info.makePages(comments, 1, self.comment_page)

            return data
        else:
            return None

    def get(self, request, blog_id):
        self.blog_id = blog_id
        data = self.getBlogInfo()
        if data is not None:
            return render(request, 'home/show-blog.html', data)
        else:
            return redirect(reversed('index'))

    def post(self, request):
        pass

    def delete(self):
        pass


# 首页加载
def index(request):
    all_info.updateData()
    type_id = int(request.GET.get('type_id', 0))
    if type_id is not None:
        all_info.setTypeId(type_id)

    page = int(request.GET.get('page_mp', 1))
    all_info.article_info = all_info.getArticlesInfo()
    # 分页信息/分页博客信息
    all_info.article_page_info, all_info.article_info = all_info.makePages(all_info.article_info, 9, page)
    # all_info.getPages(page)
    data = all_info.getBaseInfo()
    data['pages'] = all_info.article_page_info
    return render(request, 'home/index.html', data)


# 关于我
def about(request):
    with open((settings.BASE_DIR + '\\templates\\about.md').replace('\\', '/'), 'r', encoding='utf-8') as aboutFile:
        text = aboutFile.read()
        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        mdtext = md.convert(text)

        data = all_info.getBaseInfo()
        data['toc'] = md.toc
        data['about'] = mdtext

        return render(request, 'home/about.html', data)


# 吾思
def think(request):
    return render(request, 'home/think.html')


class ArticleQuery:
    """查询的类"""

    def __init__(self):
        # 展示的type类型
        self.type_id = 0
        # 分类信息
        self.all_category = RC_Article_Type.objects.all()
        # 标签信息
        self.all_tag = RC_Article_Tag.objects.all()

        # 博文总数
        self.all_count = RC_Article.objects.all().count()

        # 分页文章列表
        self.article_info = self.getArticlesInfo()
        # 文章分页信息
        self.article_page_info = None

        # 博客推荐信息
        self.top_articles = RC_Article.objects.order_by('-visits')[0:5]
        self.new_articles = RC_Article.objects.order_by('-created')[0:5]

        # 博文评论信息
        self.all_comments = None

    def makePages(self, info_list, limit, page=1):
        """
        分页
        :param info_list: 进行分页处理的数据
        :param limit: 每页展示的个数
        :param page: 显示页面
        :return: 分页信息
        """
        page_list = Paginator(info_list, limit)
        if page_list.num_pages <= 1:
            return '', info_list
        else:
            info_list = page_list.page(page)

            left = []
            right = []
            left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
            right_has_more = False  # 标示最后一页页码前是否需要显示省略号
            first = False  # 标示是否需要显示第 1 页的页码号。
            last = False  # 标示是否需要显示最后一页的页码号。
            total_pages = page_list.num_pages
            page_range = page_list.page_range
            if page == 1:
                right = page_range[page: page + 2]
                if right[-1] < total_pages - 1:
                    right_has_more = True
                if right[-1] < total_pages:
                    last = True
            elif page == total_pages:
                left = page_range[(page - 3) if (page - 3) > 0 else 0:(page - 1)]
                if left[0] > 2:
                    left_has_more = True
                if left[0] > 1:
                    first = True
            else:
                left = page_range[(page - 3) if (page - 3) > 0 else 0:(page - 1)]
                right = page_range[page:page + 2]
                if left[0] > 2:
                    left_has_more = True
                if left[0] > 1:
                    first = True
                if right[-1] < total_pages - 1:
                    right_has_more = True
                if right[-1] < total_pages:
                    last = True
            page_info = {
                'left': left,
                'right': right,
                'left_has_more': left_has_more,
                'right_has_more': right_has_more,
                'first': first,
                'last': last,
                'total_pages': total_pages,
                'page': page
            }
            return page_info, info_list

    def getArticlesInfo(self):
        """获取文章的分类及标签信息"""
        if self.type_id != 0:
            all_article = RC_Article.objects.filter(type_id=self.type_id)
        else:
            all_article = RC_Article.objects.all()
        for item in all_article:
            tags = ''
            for category in self.all_category:
                if int(item.type_id) == category.id:
                    item.type_id = category.title
                    break  # 跳出内循环
            for tag in self.all_tag:
                if str(tag.id) in str(item.tag_id):
                    tags += tag.title
            item.tag_id = tags
        return all_article

    def setTypeId(self, type_id):
        """获取不同类型的博文"""
        self.type_id = type_id
        self.article_info = self.getArticlesInfo()

    def updateData(self):
        """更新博文属性"""
        for category in self.all_category:
            articles = int(RC_Article.objects.filter(type_id=category.id).count())
            RC_Article_Type.objects.filter(id=category.id).update(count=articles)
        for tag in self.all_tag:
            tags = int(RC_Article.objects.filter(tag_id=tag.id).count())
            RC_Article_Tag.objects.filter(id=tag.id).update(count=tags)
        self.top_articles = RC_Article.objects.order_by('-visits')[0:5]
        self.new_articles = RC_Article.objects.order_by('-created')[0:5]
        self.all_category = RC_Article_Type.objects.all()
        self.all_tag = RC_Article_Tag.objects.all()

    def getComments(self, article_id):
        """获取文章的评论信息"""
        self.all_comments = RC_Comments.objects.filter(article_id=article_id, parents_id=None).order_by('-created')
        for comment in self.all_comments:
            reply = RC_Comments.objects.filter(parents_id=comment.id).order_by('number')
            comment.ups = reply
        return self.all_comments

    def getBaseInfo(self):
        """获取博客基础导航信息"""
        data = {
            'articles': all_info.article_info,
            'tops': all_info.top_articles,
            'news': all_info.new_articles,
            'categories': all_info.all_category,
            'tags': all_info.all_tag,
            'article_count': all_info.all_count
        }
        return data


all_info = ArticleQuery()
