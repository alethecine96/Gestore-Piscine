from django.urls import path
from .views import PiscinaListView, MiaPiscinaListView, HomeView
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('mia_piscina/<str:username>/<int:n_piscina>/grafici', views.line_chart, name='line-chart'),
    path('mia_piscina/', HomeView.as_view(), name='blog-home2'),
    path('piscina_request/', views.piscina_request, name='piscina_request'),
    path('mia_piscina/<str:username>/<int:n_piscina>', MiaPiscinaListView.as_view(), name='blog-mia_piscina'),
    path('', views.logged_in , name='blog-home'),
    path('create_pool', views.create_pool, name='create_pool')
]
