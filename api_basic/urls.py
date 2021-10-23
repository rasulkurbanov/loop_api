from django.urls import path
from . import views


urlpatterns = [
  path('article/', views.ArticleListView.as_view(), name='articles'),
  path('article/<int:pk>', views.ArticleDetailView.as_view(), name='article'),
  path('gen-article', views.GenericListView.as_view(), name='generic-list'),
  path('gen-article/<int:pk>', views.GenericListView.as_view(), name='generiv-view')
]




