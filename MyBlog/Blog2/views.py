from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect(instance.get_absolute_url())
    context = {
        "form": form
    }
    return render(request, "post_form.html", context)


def post_detail(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    context = {
        "title": instance.title,
        "instance": instance
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    queryset_list = Post.objects.all().order_by('-timestamp')
    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(
            Q(title__contains=query)|
            Q(content__contains=query)|
            Q(user__first_name__contains=query)|
            Q(user__last_name__contains=query)
        ).distinct()
    paginator = Paginator(queryset_list, 5)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        "title": "List",
        "obj_list": queryset,
    }
    return render(request, "post_list.html", context)


def post_update(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form
    }
    return render(request, "post_form.html", context)


def post_delete(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    return redirect("list")

