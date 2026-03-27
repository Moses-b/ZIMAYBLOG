from django.http import Http404
from django.shortcuts import render

from .content import POSTS


def blog_list(request):
    return render(request, "blog/list.html", {"posts": POSTS})


def blog_detail(request, pk):
    post = next((item for item in POSTS if item["id"] == pk), None)
    if not post:
        raise Http404("Article not found")
    return render(request, "blog/detail.html", {"post": post})
