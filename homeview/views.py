from django.shortcuts import render, HttpResponse,get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def homepage(request):
    context={
        'post': Post.objects.all()
    }
    return render(request,'home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'post'
    ordering = ['-date_posted']

"""
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    """
def PostDetailView(request,pk):
    model = Post.objects.get(pk=pk)
    comments=Comment.objects.filter(post=model.id).order_by('-id')
    is_liked = False
    if model.likes.filter(id=request.user.id).exists():
        is_liked=True
    if request.method=='POST':
        comment_form=CommentForm(request.POST or None)
        if comment_form.is_valid():
            content=request.POST.get('content')
            comment=Comment.objects.create(post=model, user=request.user,content=content)
            comment.save()
            return HttpResponseRedirect(model.get_absolute_url())
    else:
        comment_form=CommentForm()
    context = {
        'object':model,
        'is_liked':is_liked,
        'total_likes':model.total_likes(),
        'comments':comments,
        'comment_form':comment_form,
    }
    return render(request,'post_detail.html',context)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title','content','post_img']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title','content']

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
    template_name = 'post_confirm_delete.html'
    success_url = '/'
    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False
    

def aboutpage(request):
    return render(request,'about.html')

def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked=False
    else:
        post.likes.add(request.user)
        is_liked=True
    return HttpResponseRedirect(post.get_absolute_url())

