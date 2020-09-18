from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from .models import Post, Value
from .forms import PiscinaForm
from django.http import HttpResponse

def home(request):
    context = {
        'posts': Post.objects.all(),
        'values': Value.objects.all()
    }
    return render(request, 'blog/home.html', context)

    
class PiscinaListView(ListView):
    model = Value
    template_name = 'blog/piscina.html'
    context_object_name = 'values'
    form_class = PiscinaForm
    ordering = ['-date']


class MiaPiscinaListView(ListView):
    model = Value
    template_name = 'blog/mia_piscina.html'
    context_object_name = 'values'
    form_class = PiscinaForm
    
    def get_queryset(self):
        usr = get_object_or_404(User, username=self.kwargs.get('username'))
        return Value.objects.filter(user=usr).order_by('-date') 
    
    
    
@csrf_exempt
def piscina_request(request):
    if request.method == 'POST':
        form = PiscinaForm(request.POST)
        if form.is_valid():
            if(request.user.id == None):
                return HttpResponse("<h1>Non hai effettuato l'accesso al sito!!</h1>")
            form.instance.user = request.user
            values = form.save()
            values.save()
            return redirect('blog-home')
    return HttpResponse("Failed POST")


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_post']
    
    
class PostDetailView(DetailView):
    model = Post
    
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    
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
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    
def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})