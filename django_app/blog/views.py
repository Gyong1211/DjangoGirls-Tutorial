from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render
from .models import Post


def post_list(request):
    # posts 변수에 ORM을 이용해서 전체 Post의 리스트(쿼리셋를 대입
    posts = Post.objects.filter(published_date__lte = timezone.now())
    context = {
        'title': 'PostList from post_list view',
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context=context, )
