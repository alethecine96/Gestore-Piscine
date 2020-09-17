from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from .models import Post, Value
from .forms import PiscinaForm
import json
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
    
"""
def piscina(request):
    print(request.POST)
    form = PiscinaForm(request.POST)
    if form.is_valid():
        t = form.save(commit=false)  
        t.save()
"""

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


@csrf_exempt
def piscina_request(request):
    if request.method == 'POST':
        form = PiscinaForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['temperature']
            text += "---"
            text += str(form.fields.values())
            return HttpResponse(text)
        return HttpResponse(form.errors)
    return HttpResponse("Failed")
    
"""
@csrf_exempt
def piscina(request):
    if request.POST:
        return render(request, 'blog/about.html', {'title': 'About'})
    return render(request, 'blog/piscina.html', {'title': 'Piscina'})
"""