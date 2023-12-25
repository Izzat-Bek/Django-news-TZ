from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import PostModel, CategoryModel, StarModel, CommentModel
from .bot import send_news
from .forms import AddCommentFormUsername, AddCommentForm
from django.views.generic import CreateView
from django.urls import reverse_lazy


def home_view(request):
    post = PostModel.objects.all()
    name = ''
    categories = CategoryModel.objects.all()
    context = {
        'post': post,
        'categories': categories,
        'name': name
    }

    return render(request, 'nv/home.html', context)


def cotegories_view(request, pk):
    post = PostModel.objects.filter(category=pk)
    categories = CategoryModel.objects.all()
    cat = CategoryModel.objects.get(id=pk)
    name = 'cat'
    context = {
        'post': post,
        'categories': categories,
        'name': name,
        'cat': cat,
    }

    return render(request, 'nv/home.html', context)


def article_detail(request, pk):
    post = PostModel.objects.get(id=pk)
    categories = CategoryModel.objects.all()
    star = StarModel.objects.filter(post=pk)
    count = 0
    ball = 0
    for i in star:
        count += 1
        ball += i.num_star
    
    rating = 0
    if count == 0:
         rating = 0
    else:
        rating = round(ball / count)
    
    comment = CommentModel.objects.filter(post=pk)
    
    
    context = {
        'post': post,
        'categories': categories,
        'count': count,
        'ball': ball,
        'comment': comment,
        'rating': rating,
    }

    return render(request, 'nv/article.html', context)


def add_star(request, id_post, id_user, ball):
    ball = int(ball)
    post = PostModel.objects.get(id=id_post)
    user = User.objects.get(id=id_user)
    if StarModel.objects.filter(post=post, username=user).exists():
        star = StarModel.objects.get(post=post, username=user)
        star.num_star = ball
        star.save()
    else:
        star = StarModel.objects.create(post=post, username=user, num_star=ball)
        star.save()
        
    return redirect('article', pk=post.id)


    
def publish_view(request):
    post = PostModel.objects.last()
    
    send_news(post)
    
    return render(request, 'nv/home.html')



def comment_view(request, id_post, id_user):
    post = PostModel.objects.get(id=id_post)
    if request.method == 'POST':
        form = AddCommentFormUsername(request.POST)
        if form.is_valid():
            username = User.objects.get(id=id_user).username
            content = form.cleaned_data['content']
            comment = CommentModel.objects.create(post=post, username=username, content=content)
            comment.save()
            return redirect('article', pk=post.id)
    else:
        form = AddCommentFormUsername()
    post = PostModel.objects.get(id=id_post)
    return render(request, 'nv/add_comment_username.html', {'form': form, 'post': post})


class AddComment(CreateView):
    model = CommentModel
    form_class = AddCommentForm
    template_name = 'nv/add_comment.html'
        
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['id_post']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = PostModel.objects.get(id=self.kwargs['id_post'])
        return context
    
        
    success_url = reverse_lazy('home')
    