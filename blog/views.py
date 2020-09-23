from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.views.generic import ListView
from .models import Value, Piscina
from .forms import PiscinaForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.formats import localize
from django.contrib.auth.decorators import login_required

def home(request):
    context = {
        'values': Value.objects.all(),
        'piscine': Piscina.objects.all()
    }
    return render(request, 'blog/home.html', context)


class HomeView(ListView):
    model = Piscina
    context_object_name = 'piscine'
    template_name = 'blog/home.html'
    
    
def logged_in(request):
    if request.user.is_authenticated:
        return redirect('blog-home2')
    else:
        messages.warning(request, 'Non hai effettuato l\'accesso')
        return redirect('login')

    
@login_required
def create_pool(request):
    piscina = Piscina()
    piscina.user = request.user
    p = Piscina.objects.filter(user = request.user)
    n = p.last().n_piscina + 1
    piscina.n_piscina = n
    piscina.save()
    messages.success(request, f'Piscina creata correttamente')
    return redirect('blog-home2')

 
class PiscinaListView(ListView):
    model = Value
    template_name = 'blog/piscina.html'
    context_object_name = 'values'
    form_class = PiscinaForm
    ordering = ['-date']
    paginate_by = 10


class MiaPiscinaListView(ListView):
    model = Value
    template_name = 'blog/mia_piscina.html'
    context_object_name = 'values'
    form_class = PiscinaForm
    paginate_by = 10
    
    def get_queryset(self):
        usr = get_object_or_404(User, username=self.kwargs.get('username'))
        queryset = Piscina.objects.filter(user=usr)
        id = queryset.get(n_piscina = self.kwargs.get('n_piscina'))
        return Value.objects.filter(piscina=id).order_by('-date') 
    
    
@csrf_exempt
def piscina_request(request):
    if request.method == 'POST':
        form = PiscinaForm(request.POST)
        if form.is_valid():
            if (float(request.POST.get('temperature')) < -20 or float(request.POST.get('temperature')) > 40 
                or float(request.POST.get('ph')) < 0 or float(request.POST.get('ph')) > 14):
                messages.warning(request, 'I dati inseriti non sono corretti!')
                return redirect('blog-home')    
            if (request.user.is_authenticated):
                queryset = Piscina.objects.filter(user=request.user)
                form.instance.piscina = queryset.get(n_piscina=request.POST.get('n_piscina'))
                #form.instance.piscina.user = request.user
            elif (User.objects.filter(username=request.POST.get('user')).first().check_password(request.POST.get('password'))):
                form.instance.piscina = Piscina.objects.first()
                #queryset = Piscina.objects.filter(user=User.objects.filter(username=request.POST.get('user')).first())
                #form.instance.piscina = queryset.get(n_piscina=request.POST.get('n_piscina'))
                #form.instance.piscina.user = User.objects.filter(username=request.POST.get('user')).first()
            values = form.save()
            values.save()
            print(values.piscina.id)
            print(values.piscina.user)
            print(values.piscina.n_piscina)
            messages.success(request, f'Dati aggiornati correttamente!')
            return HttpResponse("<h1>SI!</h1>")
        return redirect('blog-home2')
    return HttpResponse("Failed POST")
    

def line_chart(request, username, n_piscina):
    if(request.user.is_authenticated):
        data = []
        temperature = []
        ph = []

        queryset = Value.objects.order_by('-date')
        for values in queryset:
            if(values.piscina.user == request.user):
                if(values.piscina.n_piscina == n_piscina):
                    data.append(str(localize(values.date)))
                    temperature.append(values.temperature)
                    ph.append(values.ph)
        return render(request, 'blog/graph.html', {
            'temperature': temperature,
            'data': data,
            'ph': ph,
        })
    else:
        messages.warning(request, 'Non hai effettuato l\'accesso')
        return redirect('login')