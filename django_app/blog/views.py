from django.contrib.auth import get_user_model
# from django.utils import timezone
# from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post
from .forms import PostCreateForm, PostModifyForm

User = get_user_model()


def post_list(request):
    # posts 변수에 ORM을 이용해서 전체 Post의 리스트(쿼리셋를 대입
    posts = Post.objects.order_by('-created_date')
    # posts = Post.objects.filter(published_date__lte = timezone.now())
    context = {
        'title': 'PostList',
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context=context, )


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context=context)


def post_create(request):
    if request.method == 'GET':
        form = PostCreateForm()
        context = {
            'form': form,
        }
        return render(request, 'blog/post_create.html', context=context)

    elif request.method == 'POST':
        # Form 클래스의 생성자에 POST 데이터를 전달하여 Form 인스턴스를 생성
        form = PostCreateForm(request.POST)
        # Form 인스턴스의 유효성을 검사하는 is_valid 메서드
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            user = User.objects.first()
            post = Post.objects.create(
                author=user,
                title=title,
                text=text
            )
            return redirect('post_detail', pk=post.id)
        else:
            context = {
                'form': form,
            }
            return render(request, 'blog/post_create.html', context=context)


def post_modify(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        form = PostModifyForm(request.POST)
        # POST 요청request)가 올 경우 전달받은 데이터의 title, text값을 사용해서
        # 해당하는 Post 인스턴스 (post)의 title, text 속성값에 덮어씌우고
        # DB에 업데이트하는 save() 메서드 실행
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            post.title = title
            post.text = text
            post.save()
            # 기존 post인스턴스를 업데이트 한 후, 다시 글 상세화면으로 이동
            return redirect('post_detail', pk=post.id)
        else:
            context = {
                'form': form,
                'post': post,
            }
            return render(request, 'blog/post_modify.html', context=context)

    elif request.method == 'GET':
        # pk에 해당하는 Post 인스턴스를 전달
        form = PostModifyForm(initial={'title': post.title, 'text': post.text})
        context = {
            'form': form,
            'post': post,
        }
        return render(request, 'blog/post_modify.html', context=context)


def post_delete(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list', )

    elif request.method == 'GET':
        context = {
            'post': post,
        }
        return render(request, 'blog/post_delete.html', context=context)
