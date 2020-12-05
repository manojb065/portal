import requests
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404,redirect
from .models import Comments
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post,gitrep
from users.models import Profile
from django.urls import reverse_lazy
from django.contrib.staticfiles.views import serve

from django.db.models import Q


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def search(request):
    template='blog/home.html'

    query=request.GET.get('q')

    result=Post.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query))
    paginate_by=6
    context={ 'posts':result }
    return render(request,template,context)

def gitsearch(request):
    query = request.GET.get('q')
    projects=gitrep.objects.filter(Q(respo__icontains=query) | Q(profile__user__username__icontains=query))
    alist = []
    for i in range(0, len(projects) - 1, 2):
        alist.append([projects[i], projects[i + 1]])
    if len(projects) % 2 != 0:
        alist.append([projects[len(projects) - 1], None])
    paginator = Paginator(alist, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    res = page_obj.paginator.count
    context = {"page_obj": page_obj,'qu':True,'q':query}
    return render(request, 'blog/about.html', context)
   


def getfile(request):
   return serve(request, 'File')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    # context_object_name = 'posts'
    paginate_by = 6

    # def get_queryset(self):
    #     user = get_object_or_404(User, username=self.kwargs.get('username'))
    #     return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['posts']=Post.objects.filter(author=user).order_by('-date_posted')
        u=Profile.objects.filter(user=user).first()
        context['git']=gitrep.objects.filter(profile=u)
        context['author']=user.username
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    # queryset = Comments.objects.filter(post=Post.objects.filter(id=DetailView.request.get['pk']))


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False




def AddComments(request,pk):
    if  request.GET['com']:
        postc=Post.objects.filter(id=pk)
        c=Comments(usr=request.user,post=postc[0],com=request.GET['com'])
        c.save()
    return redirect('post-detail', pk=pk)

def about(request):
    projects=gitrep.objects.all()
    alist = []
    for i in range(0, len(projects) - 1, 2):
        alist.append([projects[i], projects[i + 1]])
    if len(projects) % 2 != 0:
        alist.append([projects[len(projects) - 1], None])
    paginator = Paginator(alist, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    res = page_obj.paginator.count
    context = {"page_obj": page_obj}
    return render(request, 'blog/about.html', context)

def gitDetails(request,id):
    detail=gitrep.objects.filter(rpid=id).first()
    yet=requests.get(detail.files)
    det=yet.json()
    for i in det['tree']:
        print(i)
    context={'del':det['tree'],'det':detail}
    return render(request,'blog/list.html',context)