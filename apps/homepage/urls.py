from django.urls import path, re_path
from homepage import views
from .views import ArticleView, CategoryView, TagView, CommentsView


urlpatterns = [
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('think/', views.think, name='think'),
    re_path(r'show-blog/(?P<blog_id>.*)', ArticleView.as_view(), name='show-blog'),
    re_path(r'type/(?P<type_name>.*)', CategoryView.as_view(), name='type'),
    path('comment/', CommentsView.as_view(), name='comment'),

]