from django.db import models
from mdeditor.fields import MDTextField


# Create your models here.


class RC_Article_Type(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='文章分类', max_length=255)
    count = models.IntegerField(verbose_name='数量', default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = models.CharField(verbose_name='说明', max_length=500)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'RC_ARTICLE_TYPE'
        ordering = ['id']
        verbose_name = '文章分类'
        verbose_name_plural = '文章分类'


class RC_Article_Tag(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名', max_length=255)
    count = models.IntegerField(verbose_name='数量', default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'RC_ARTICLE_TAG'
        ordering = ['id']
        verbose_name = '文章标签'
        verbose_name_plural = '文章标签'


class RC_Article(models.Model):
    tagSelect = (('1', '分享'), ('2', '原创'))
    typeSelect = (('1', 'Python'), ('2', 'Django'), ('3', 'Java'), ('4', 'Linux'))
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='文章名', max_length=255)
    content = models.TextField(verbose_name='说明描述')
    md_content = MDTextField(verbose_name='文章内容')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    update_times = models.IntegerField(verbose_name='更新次数', default=0)
    type_id = models.CharField(verbose_name='分类', choices=typeSelect, max_length=50)
    tag_id = models.CharField(verbose_name='标签', choices=tagSelect, max_length=50)  # id1,id2
    visits = models.IntegerField(verbose_name='访问量', default=0)
    ups = models.IntegerField(verbose_name='点赞数', default=0)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'RC_ARTICLE'
        ordering = ['id']
        verbose_name = '文章'
        verbose_name_plural = '文章'


class RC_Comments(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(verbose_name='邮箱', max_length=50)
    user_name = models.CharField(verbose_name='昵称', max_length=50)
    article_id = models.CharField(verbose_name='文章ID', max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    number = models.IntegerField(verbose_name='序号', null=True, default=0)
    replied_user = models.CharField(verbose_name='被回复的用户', max_length=10, null=True, blank=True)
    parents_id = models.CharField(verbose_name='主评论ID', max_length=10, null=True, blank=True)
    content = models.CharField(verbose_name='内容', max_length=500)
    count = models.IntegerField(verbose_name='回复数', default=0)
    ups = models.IntegerField(verbose_name='点赞数', default=0)

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = 'RC_COMMENTS'
        ordering = ['id']
        verbose_name = '评论'
        verbose_name_plural = '评论'
