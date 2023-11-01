from django.urls import path
from . import views
	
urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('vinyl/', views.vinyl_index, name='index'),
  path('vinyl/<int:vinyl_id>/', views.vinyl_detail, name='detail'),
  path('vinyl/create/', views.VinylCreate.as_view(), name='vinyl_create'),
  path('vinyl/<int:pk>/update/', views.VinylUpdate.as_view(), name='vinyl_update'),
  path('vinyl/<int:pk>/delete/', views.VinylDelete.as_view(), name='vinyl_delete'),
  path('vinyl/<int:vinyl_id>/add_listens/', views.add_listens, name='add_listens')
]

