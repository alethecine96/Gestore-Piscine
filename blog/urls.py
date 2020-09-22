from django.urls import path
from .views import PiscinaListView, MiaPiscinaListView
from . import views

urlpatterns = [
    path('mia_piscina/grafici', views.line_chart, name='line-chart'),
    path('', PiscinaListView.as_view(), name='blog-home'),
    path('piscina_request/', views.piscina_request, name='piscina_request'),
    path('mia_piscina/<str:username>', MiaPiscinaListView.as_view(), name='blog-mia_piscina')
]
