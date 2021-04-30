from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Comments
from .forms import PostForm, SearchForm, CommentForm

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def post_search(request):    
    search_text = request.GET.get("search", "")
    form = SearchForm(request.GET)
    posts = set()
    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "title"
        if search_in == "title":
            posts = Post.objects.filter(title__icontains=search)
    return render(request, "blog/search_result.html", {"form":form, "search_text":search_text, "posts":posts})

# class PostListView(generic.ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post_list.html'

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag= None
    if tag_slug:
        tag= get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 4)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    posts = Post.objects.filter(publish__lte=timezone.now()).order_by('publish')
    return render(request, 'blog/post_list.html', {'page': page, 'posts':posts, 'tag':tag})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    comments = Comments.objects.filter(blog=post)
    if request.method == "POST":
        print("post")
        form = CommentForm(request.POST)
        if form.is_valid():
            print("form valid")
            comments = Comments(commentor=form.cleaned_data['commentor'], comment_text=form.cleaned_data['comment_text'], blog=post)
            comments.save()
            return redirect('/blog/')
    else:
        print("else")
        form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    context = {'post':post, 'form':form, 'comments':comments,'similar_posts':similar_posts}
    return render(request, 'blog/post_detail.html', context)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)

    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})