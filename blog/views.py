from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.db.models import Count
from .models import Post

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})



from django.views.generic import CreateView
from .models import Post  # Import your Post model
from django.urls import reverse_lazy  # To redirect after form submission

class PostCreateView(CreateView):
    model = Post
    template_name = 'post_form.html'  # This is the template for the form
    fields = ['title', 'content', 'tags']  # Adjust fields based on your Post model
    success_url = reverse_lazy('post_list')  # Redirect to post list after creating a post

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-published_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__name=tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Post.tags.most_common()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'



from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity

def post_search(request):
    query = request.GET.get('query', '')
    search_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B') 
    search_query = SearchQuery(query)
    results = Post.objects.annotate(
        rank=SearchRank(search_vector, search_query),
        similarity=TrigramSimilarity('title', query),
    ).filter(rank__gte=0.3).order_by('-rank')
    return render(request, 'search_results.html', {'results': results, 'query': query})


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment

@login_required
def profile(request):
    user = request.user  # Get the currently logged-in user
    
    return render(request, 'profile.html', {'user': user})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        text = request.POST.get('text')
        Comment.objects.create(post=post, author=request.user, text=text)
    return redirect('post_detail', pk=pk)

# @login_required
# def like_comment(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     if request.user in comment.likes.all():
#         comment.likes.remove(request.user)
#     else:
#         comment.likes.add(request.user)
#     return redirect('post_detail', pk=comment.post.pk)

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk  # Ensure the post ID is available
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('post_detail', pk=post_pk)



from django.core.mail import send_mail
from django.conf import settings

def share_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        email = request.POST.get('email')
        send_mail(
            f"Check out this post: {post.title}",
            f"Read {post.title} at {request.build_absolute_uri(post.get_absolute_url())}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return redirect('post_detail', pk=pk)
    return render(request, 'share_post.html', {'post': post})

from django.contrib.auth import logout
def user_logout(request):
    logout(request)
    return redirect('login')


from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_form.html'  # Reusing the same form template
    fields = ['title', 'content', 'tags']  # Adjust fields based on your Post model

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author to the logged-in user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Ensure the user is the author of the post

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})  # Redirect to the post detail after updating

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'delete.html'  # A specific template for confirming deletion
    success_url = reverse_lazy('post_list')  # Redirect to the post list after deletion

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Ensure only the author can delete the post
