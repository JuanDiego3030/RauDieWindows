from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('panel_control/', views.control, name='panel_control'),
    path('panel_seguimiento/', views.seguimiento, name='panel_seguimiento'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('cliente_login/', views.cliente_login, name='cliente_login'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('cliente_register/', views.cliente_register, name='cliente_register'),
    path('logout/', views.logout, name='logout'),

]
