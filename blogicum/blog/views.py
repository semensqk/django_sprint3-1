from django.shortcuts import render, get_object_or_404

from datetime import datetime

from .models import Post, Category


def filter_posts():
    post_list = Post.objects.select_related(
        'category'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now()
    )[0:5]

    return post_list


def index(request):
    template_name = 'blog/index.html'
    post_list = filter_posts()

    context = {
        'post_list': post_list
    }
    return render(request, template_name, context)


def post_detail(request, id):
    template_name = 'blog/detail.html'
    user_post = Post.objects.select_related(
        'category'
    ).filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    )
    post = get_object_or_404(user_post, pk=id)

    context = {
        'post': post
    }
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = Post.objects.select_related(
        'category'
    ).filter(
        category=category.pk,
        is_published=True,
        pub_date__lte=datetime.now()
    )

    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template_name, context)
