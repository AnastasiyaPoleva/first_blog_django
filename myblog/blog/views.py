from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import Post, Likes
from .form import CommentsForm

class PostView(View):
    """вывод записей"""
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'blog/blog.html', {'post_list': posts})


class PostDetail(View):
    """отдельная страница для постов"""
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        return render(request, 'blog/blog_detail.html', {'post': post})


class AddComments(View):
    """Добавление комментария"""
    def post(self, reguest, pk):
        form = CommentsForm(reguest.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.post_id = pk
            form.save()
        return redirect(f'/{pk}')


def get_client_ip(reguest):
    """получаем ip клиента"""
    x_forwarded_for = reguest.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = reguest.META.get('REMOTE_ADDR')
    return ip


class AddLikes(View):
    """Получение лайков"""
    def get(self, reguest, pk):
        ip_client = get_client_ip(reguest)
        try:
            Likes.objects.get(ip=ip_client, post_id=pk)
            return redirect(f'/{pk}')
        except:
            new_like = Likes()
            new_like.ip = ip_client
            new_like.post_id = int(pk)
            new_like.save()
            return redirect(f'/{pk}')


class DelLike(View):
    """Удаление лайков/Дизлайки"""
    def get(self, reguest, pk):
        ip_client = get_client_ip(reguest)
        try:
            like = Likes.objects.get(ip=ip_client)
            like.delete()
            return redirect(f'/{pk}')
        except:
            return redirect(f'/{pk}')