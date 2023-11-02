from django.urls import path
from . import views
	
urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('vinyls/', views.vinyls_index, name='index'),
  path('vinyls/<int:vinyl_id>/', views.vinyls_detail, name='detail'),
  path('vinyls/create/', views.VinylCreate.as_view(), name='vinyls_create'),
  path('vinyls/<int:pk>/update/', views.VinylUpdate.as_view(), name='vinyls_update'),
  path('vinyls/<int:pk>/delete/', views.VinylDelete.as_view(), name='vinyls_delete'),
  path('vinyls/<int:vinyl_id>/add_listens/', views.add_listens, name='add_listens'),
  path('vinyls/<int:vinyl_id>/add_photo/', views.add_photo, name='add_photo'),
  path('vinyls/<int:vinyl_id>/assoc_vinyl/<int:turntable_id>/', views.assoc_turntable, name='assoc_turntable'),
  path('vinyls/<int:vinyl_id>/unassoc_turnable/<int:turntable_id>/', views.unassoc_turntable, name='unassoc_turntable'),
  path('turntables/', views.TurntableList.as_view(), name='turntables_index'),
  path('turntables/<int:pk>/', views.TurntableDetail.as_view(), name='turntables_detail'),
  path('turntables/create/', views.TurntableCreate.as_view(), name='turntables_create'),
  path('turntables/<int:pk>/update/', views.TurntableUpdate.as_view(), name='turntables_update'),
  path('turntables/<int:pk>/delete/', views.TurntableDelete.as_view(), name='turntables_delete'),
]


