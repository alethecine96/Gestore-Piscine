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
from django.contrib.auth import authenticate, login
from django.contrib import messages

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
            if (int(request.POST.get('temperature')) < -20 or int(request.POST.get('temperature')) > 40 
                or int(request.POST.get('ph')) < 0 or int(request.POST.get('ph')) > 14):
                messages.warning(request, 'I dati inseriti non sono corretti!')
                return redirect('blog-home')
            if (request.user.is_authenticated):
                form.instance.user = request.user
            elif (User.objects.filter(username=request.POST.get('user')).first().check_password(request.POST.get('password'))):
                form.instance.user = User.objects.filter(username=request.POST.get('user')).first()
            values = form.save()
            values.save()
            messages.success(request, f'Dati aggiornati correttamente!')
            return redirect('blog-home')
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