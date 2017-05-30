from django.contrib.auth import get_user_model
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post

User = get_user_model()

def post_list(request):
    # posts 변수에 ORM을 이용해서 전체 Post의 리스트(쿼리셋를 대입
    posts = Post.objects.order_by('-created_date')
    # posts = Post.objects.filter(published_date__lte = timezone.now())
    context = {
        'title': 'PostList from post_list view',
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context=context, )

def post_detail(request, pk):
    post=Post.objects.get(id=pk)
    context = {
        'post':post,
    }
    return render(request, 'blog/post_detail.html',context=context)

def post_create(request):
    if request.method == 'GET':
        context = {
        }
        return render(request, 'blog/post_create.html',context=context)
    elif request.method == 'POST':
        data = request.POST
        title = data['title']
        text = data['text']
        user = User.objects.first()
        post = Post.objects.create(
            author=user,
            title=title,
            text=text
        )
        return redirect('post_detail', pk=post.id)