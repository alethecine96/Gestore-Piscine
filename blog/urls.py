from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PiscinaListView,
    MiaPiscinaListView
    )
from . import views

urlpatterns = [
    path('post', PostListView.as_view(), name='blog-post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('', PiscinaListView.as_view(), name='blog-home'),
    path('piscina_request/', views.piscina_request, name='piscina_request'),
    path('mia_piscina/<str:username>', MiaPiscinaListView.as_view(), name='blog-mia_piscina')
]
